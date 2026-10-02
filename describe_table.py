"""Write PAY 4.2 descriptions onto a table's columns, addressed by name.

Do not patch `/columns/N/description`. JSON Patch addresses arrays positionally, and the
array an agent reads back from the MCP `get_entity_details` tool is not the stored one -
it is paginated and trimmed for context. Index 17 in that response is not index 17 in the
entity, so a correct description lands silently on the wrong column.

A column is its own entity, addressable by name:

    GET /v1/columns/name/{fqn}?entityType=table    read one column
    PUT /v1/columns/name/{fqn}?entityType=table    set description and tags together

PATCH on that resource answers 405 - verified against a live server, and the resource
carries no @PATCH in the source - so documentation showing a JSON patch against a column
does not apply here. PUT takes an UpdateColumn body, where omitting `tags` leaves the
existing ones alone and the server validates every term against the glossary.

This reads the table's columns, pairs each one matching a datapoint in 05-datapoints.csv
with that datapoint, and writes the description and the glossary terms. Context columns
are not touched.

Usage:

    export OM_HOST=https://host/api OM_JWT_TOKEN=...
    uv run describe_table.py SQLSASTest.FIDW_BI.dbo.Y_01_01
    uv run describe_table.py SQLSASTest.FIDW_BI.dbo.Y_01_01 --variant 0010 --commit
"""

import argparse
import csv
import json
import re
from collections import defaultdict
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

from display_names import display_names, table_name

PACK = Path(__file__).parent
DATAPOINTS = PACK / "05-datapoints.csv"
DORA_DATAPOINTS = PACK / "source" / "dpm-dora-1.1.0-datapoints.csv"
DORA_VOCABULARY = PACK / "source" / "dpm-dora-1.1.0-vocabulary.csv"
DORA_GLOSSARY = "DORA_1_1_0"

# Only these are framework columns. Everything else is warehouse context and is left alone.
DATAPOINT_COLUMN = re.compile(r"^[A-Za-z][0-9]{4}_r[0-9]{4}_c[0-9]{4}$")

# The same shape, taken apart. A DORA row is an ordinal and can be any length, which is
# why this is looser than the PAY-only pattern above.
DATAPOINT_COLUMN_PARTS = re.compile(r"^(?P<prefix>[A-Za-z]+[0-9]{4})_r(?P<row>[0-9]+)_c(?P<col>[0-9]{4})$")

# The DPM's sheet axis becomes an open axis in the warehouse: rather than one table per
# variant, one table holds all of them and a context column says which row is which. Its
# values are the variant labels without the code - "Domestic amount of payments" - which
# matches variant_label exactly for all six, verified.
OPEN_AXIS_COLUMN = re.compile(r"^Open_Axis_[0-9]+$", re.IGNORECASE)

GLOSSARY = "PAY_4_2"
DOMAIN_OF_DIMENSION = {
    "Event Type": "Fraud event types",
    "Payment related parties": "Payment related parties",
    "Relationships": "Payment related parties",
    "Type of user": "Payment related parties",
    "Payment transactions geographical breakdown": "Geographical breakdown",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OM_", env_file=".env", extra="ignore")

    host: str = "http://localhost:8585/api"
    jwt_token: str
    ca_bundle: str | None = None
    # Where a Context Center article lives in the UI. The route changed when Knowledge
    # Center became Context Center and is not the same across versions, so it is
    # configured rather than guessed: copy it out of the browser once, with {name} where
    # the page name goes. Unset means the article is named in prose instead of linked.
    page_url: str | None = None


class Datapoint(BaseModel):
    """One row of 05-datapoints.csv. Frozen: read once, then only read from."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    column_name: str
    table_name: str
    datapoint_id: str
    template: str
    template_name: str
    variant: str
    variant_label: str
    metric: str
    geography: str
    row_code: str
    row_label: str
    column_code: str
    column_label: str
    row_dimensions: str
    column_dimensions: str
    unit: str
    sign: str

    @property
    def dimension_members(self) -> list[tuple[str, str]]:
        """Every dimension = member pair on this datapoint, row axis then column axis."""
        pairs = []
        for chunk in (self.row_dimensions, self.column_dimensions):
            for part in filter(None, (p.strip() for p in chunk.split(";"))):
                dimension, _, member = part.partition("=")
                if member:
                    pairs.append((dimension.strip(), member.strip()))
        return pairs

    # The row and column labels are the display name, so they are not repeated here. A
    # description that opened with them said the same thing twice in two adjacent fields.
    # The consequence, accepted deliberately: where a token may not set display names, the
    # labels are not in the catalogue at all - so set the name, or pass keep_labels.
    def description_without_variant(self, axis_column: str, keep_labels: bool = False) -> str:
        """What holds across every variant, for a table that carries all of them.

        No datapoint id and no unit: those differ per variant, and here the variant is a
        property of the row rather than of the table. Naming the axis column is what lets
        a reader get from this description to the specific datapoint.
        """
        members = "; ".join(f"{dim} = {member}" for dim, member in self.dimension_members)
        return (
            (f"{self.row_label} — {self.column_label}. " if keep_labels else "")
            + (f"Dimension members: {members}. " if members else "")
            + f"Template {self.template} (EBA PAY 4.2), row {self.row_code}, column {self.column_code}. "
            f"This table holds every variant; `{axis_column}` on each row gives the metric and "
            "geography, and with it the datapoint id and the unit. Non-negative."
        )

    def description(self, keep_labels: bool = False) -> str:
        unit = "monetary amount" if self.unit != "#" else "count"
        members = "; ".join(f"{dim} = {member}" for dim, member in self.dimension_members)
        return (
            (f"{self.row_label} — {self.column_label}. " if keep_labels else "")
            + f"{self.metric}, {self.geography.lower()}. "
            + (f"Dimension members: {members}. " if members else "")
            + f"Datapoint {self.datapoint_id} of template {self.template} (EBA PAY 4.2), "
            f"row {self.row_code}, column {self.column_code}. Unit: {unit}, {self.sign}."
        )

    def glossary_terms(self) -> list[str]:
        """Term FQNs for this datapoint's members, deduplicated, in order."""
        terms = []
        for dimension, member in self.dimension_members:
            domain = DOMAIN_OF_DIMENSION.get(dimension, "Payment transaction characteristics")
            fqn = f"{GLOSSARY}.Domains.{domain}.{member}"
            if fqn not in terms:
                terms.append(fqn)
        return terms


class DoraDatapoint(BaseModel):
    """One row of the DORA datapoint export. Fewer fields than PAY, and no variants."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    column_name_pattern: str
    table_name: str
    template: str
    template_name: str
    row_code: str
    row_label: str
    column_code: str
    column_label: str
    datapoint_id: str
    row_kind: str

    def description(self, keep_labels: bool = False) -> str:
        """What the column holds, the template, the datapoint id. Nothing is withheld.

        DORA has no variants, so unlike PAY there is no case where the id has to be left
        out. The note about the ordinal is the one thing a reader will otherwise get wrong.
        """
        opening = f"{self.column_label}. " if keep_labels else ""
        if self.row_kind == "open":
            return (
                f"{opening}Column {self.column_code} of template {self.template} "
                f"({self.template_name}) in the DORA register of information. "
                f"Datapoint {self.datapoint_id} (EBA DPM, module DORA 1.1.0). One row per record; "
                "the row number in the column name is an ordinal, not a framework code."
            )
        return (
            f"{opening}Column {self.column_code}, row {self.row_code}"
            + (f" ({self.row_label})" if self.row_label else "")
            + f", of template {self.template} ({self.template_name}) in the DORA register of "
            f"information. Datapoint {self.datapoint_id} (EBA DPM, module DORA 1.1.0)."
        )

    def display_name(self) -> str:
        """The column label, which is the whole of the name - a DORA row says nothing.

        A fixed row is the exception: there the row label is what distinguishes the
        columns of one template from each other.
        """
        if self.row_kind != "open" and self.row_label and self.row_label != self.column_label:
            return f"{self.row_label} - {self.column_label}"
        return self.column_label


def dora_table_description(dora: dict[str, DoraDatapoint], article: str = "") -> str:
    """What the table is, for the table's own description field."""
    first = next(iter(dora.values()))
    rows = sorted({dp.row_code for dp in dora.values()})
    shape = (
        "One row per record; the row number in a column name is an ordinal, not a framework code. "
        if first.row_kind == "open"
        else f"{len(rows)} fixed row(s): {', '.join(rows)}. "
    )
    return (
        f"Template {first.template} ({first.template_name}) of the DORA register of information, "
        f"EBA DPM module DORA 1.1.0. {shape}"
        f"{len(dora)} datapoint column(s), named for their template, row and column, as in "
        f"{min(dora)}. Every other column is warehouse context and carries no framework meaning. " + article
    )


def dora_terms_by_column(rows: list[dict[str, str]]) -> dict[tuple[str, str], list[str]]:
    """Glossary term FQNs per (template, column code), from the DORA vocabulary.

    Two kinds, and both belong on the column. The `property` row is what the column holds -
    one per column, no exceptions in this export. A `member` row is a fixed characteristic
    of the column, the same sense as a PAY dimension member: column 0060 of B_01.02 is the
    LEI code *of the direct parent*, so `Direct parent` in the Related parties domain is a
    fact about that column rather than one of its possible values.

    Pure, so the mapping can be checked without loading the file.
    """
    terms: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in rows:
        key = (row["template"], row["column_code"])
        if row["kind"] == "property":
            fqn = f"{DORA_GLOSSARY}.Properties.{row['name']}"
        elif row["kind"] == "member" and row["domain"]:
            fqn = f"{DORA_GLOSSARY}.Domains.{row['domain']}.{row['name']}"
        else:
            continue
        if fqn not in terms[key]:
            terms[key].append(fqn)
    return dict(terms)


def load_dora_terms() -> dict[tuple[str, str], list[str]]:
    """The vocabulary mapping, or nothing if the export is not in the checkout."""
    if not DORA_VOCABULARY.exists():
        return {}
    with DORA_VOCABULARY.open(encoding="utf-8") as fh:
        return dora_terms_by_column(list(csv.DictReader(fh)))


def load_dora() -> list[DoraDatapoint]:
    """Every DORA datapoint. Small enough that a list beats an index."""
    if not DORA_DATAPOINTS.exists():
        return []
    with DORA_DATAPOINTS.open(encoding="utf-8") as fh:
        return [DoraDatapoint.model_validate(row) for row in csv.DictReader(fh)]


def dora_for_table(table: str, columns: list[str]) -> dict[str, DoraDatapoint]:
    """Match a table's physical columns to DORA datapoints.

    Two rules, because DORA templates come both ways. An open template has one row per
    record, so the ordinal in the column name carries no meaning and the match is on the
    column code alone. A fixed template names its rows, so the column name matches
    exactly - which is what B_99_01 needs.
    """
    datapoints = [dp for dp in load_dora() if dp.table_name == table]
    if not datapoints:
        return {}

    by_exact = {dp.column_name_pattern: dp for dp in datapoints}
    by_code = {dp.column_code: dp for dp in datapoints if dp.row_kind == "open"}

    matched = {}
    for name in columns:
        parts = split_column_name(name)
        if name in by_exact:
            matched[name] = by_exact[name]
        elif parts and parts["col"] in by_code:
            matched[name] = by_code[parts["col"]]
    return matched


def split_column_name(name: str) -> dict[str, str] | None:
    """The row and column codes out of a warehouse column name, or None if it is context."""
    match = DATAPOINT_COLUMN_PARTS.match(name)
    return match.groupdict() if match else None


def pay_table_description(
    datapoints: list[Datapoint], axis_column: str | None, variant: str | None, article: str = ""
) -> str:
    """What the table is, for the table's own description field.

    Says which variant it holds, because that is the one thing about a PAY table that a
    reader cannot work out from the columns - and the thing the column descriptions have
    to stay silent about when nobody knows.
    """
    first = datapoints[0]
    variants = sorted({dp.variant: dp.variant_label for dp in datapoints}.items())
    per_variant = len({dp.column_name for dp in datapoints})

    if axis_column:
        holds = (
            f"This table holds all {len(variants)} variant(s) as rows; `{axis_column}` on each row says "
            "which, and with it the datapoint id and the unit. A column description therefore covers "
            "all of them and states neither."
        )
    elif variant:
        label = dict(variants).get(variant, variant)
        holds = f"This table holds one variant: {label}."
    else:
        holds = (
            f"Which of the {len(variants)} variants this table holds is not recorded here, so the "
            "column descriptions state neither a datapoint id nor a unit."
        )

    return (
        f"Template {first.template} ({first.template_name}) of EBA PAY 4.2, module PSD_FRP 1.1.0. "
        f"{per_variant} datapoint column(s) per variant, {len(variants)} variant(s) - metric crossed "
        f"with geography. {holds} Datapoint columns are named for their template, row and column, as in "
        f"{min(dp.column_name for dp in datapoints)}. Every other column is warehouse context and "
        "carries no framework meaning. " + article
    )


def load_datapoints() -> dict[str, list[Datapoint]]:
    """Datapoints grouped by warehouse column name. One name, up to six variants."""
    grouped: dict[str, list[Datapoint]] = defaultdict(list)
    with DATAPOINTS.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            dp = Datapoint.model_validate(row)
            grouped[dp.column_name].append(dp)
    return grouped


def pick(candidates: list[Datapoint], variant: str | None) -> Datapoint | None:
    """Which of the variants this table holds.

    A column name carries no variant, so without one told to us the only honest choice is
    to describe nothing rather than pick arbitrarily - unless there is only one.
    """
    if variant:
        return next((dp for dp in candidates if dp.variant == variant), None)
    return candidates[0] if len(candidates) == 1 else None


def find_open_axis(table_columns: list[dict]) -> str | None:
    """The context column carrying the variant, if the table has one."""
    return next(
        (
            c["fullyQualifiedName"].rsplit(".", 1)[-1]
            for c in table_columns
            if OPEN_AXIS_COLUMN.match(c["fullyQualifiedName"].rsplit(".", 1)[-1])
        ),
        None,
    )


def columns_to_write(
    table_columns: list[dict],
    by_column: dict[str, list[Datapoint]],
    variant: str | None,
    axis_column: str | None,
) -> tuple[list[tuple[str, Datapoint]], list[str]]:
    """Pair each datapoint column with the datapoint it reports.

    Pure. Context columns and columns with no datapoint are left out rather than
    described from a framework they do not belong to.

    With an open axis the table carries every variant as rows, so any candidate serves:
    the description written from it is the one that holds for all of them.
    """
    write, skipped = [], []
    for column in table_columns:
        fqn = column["fullyQualifiedName"]
        name = fqn.rsplit(".", 1)[-1]
        candidates = by_column.get(name)
        if not DATAPOINT_COLUMN.match(name) or not candidates:
            continue
        chosen = pick(candidates, variant) if axis_column is None else candidates[0]
        if chosen is None:
            skipped.append(f"{name} ({len(candidates)} variants, none chosen)")
            continue
        write.append((fqn, chosen))
    return write, skipped


def check_variant(by_column: dict[str, list[Datapoint]], table: str, variant: str | None) -> None:
    """Fail on a variant that matches nothing, before printing it once per column.

    A typo or a leftover placeholder otherwise reads as "pass --variant to choose" on
    every line, which is the opposite of what happened.
    """
    if variant is None:
        return
    available = sorted({dp.variant for dps in by_column.values() for dp in dps if dp.table_name == table if dp.variant})
    if variant not in available:
        raise SystemExit(
            f"  No variant {variant!r} in {table}. Available: {', '.join(available)}.\n"
            "  They are metric crossed with geography - amount or count, domestic or within "
            "the EEA or outside it."
        )


class CatalogueError(Exception):
    """OpenMetadata would not answer. See StoreError in pay42_lookup for why not SystemExit."""


def fetch_table(http: httpx.Client, table_fqn: str) -> dict:
    """The table with every column, paging until the server stops truncating.

    The table's own displayName and description ride along in the same body, so reading
    the columns and reading what the table itself says is one request, not two.
    """
    merged: dict = {}
    columns: list[dict] = []
    offset = 0
    while True:
        response = http.get(f"/v1/tables/name/{table_fqn}", params={"fields": "columns", "columnOffset": offset})
        if response.status_code >= 400:
            raise CatalogueError(f"Reading {table_fqn} failed: {response.status_code} {response.text[:300]}")
        body = response.json()
        merged = merged or body
        page = body.get("columns") or []
        columns.extend(page)
        if not body.get("columnsTruncated") or not page:
            return merged | {"columns": columns}
        offset += len(page)


def fetch_columns(http: httpx.Client, table_fqn: str) -> list[dict]:
    """Every column of the table. The batch writer wants only these."""
    return fetch_table(http, table_fqn)["columns"]


# OpenMetadata ships ApplicationBotPolicy with a rule that denies EditDisplayName, so a
# bot token may write a description but not a label. Both travel in one request and the
# whole request fails, so a denied label would otherwise take the description with it.
# Seen for real: 403 EditDisplayName denied by role ApplicationBotImpersonationRole.
DISPLAY_NAME_DENIED = re.compile(r"EditDisplayName", re.IGNORECASE)


def denied_display_name(response: httpx.Response) -> bool:
    """Whether this 403 is the server refusing the label rather than the whole write."""
    return response.status_code == 403 and bool(DISPLAY_NAME_DENIED.search(response.text))


def put_column(http: httpx.Client, fqn: str, body: dict[str, Any]) -> tuple[httpx.Response, bool]:
    """PUT one column, retrying without the label if that is what was refused.

    Returns the response and whether the label had to be dropped, so the caller can say
    so once rather than per column. Losing a label is a worse catalogue; losing the
    description along with it would be a worse one still.
    """
    response = http.put(f"/v1/columns/name/{fqn}", params={"entityType": "table"}, json=body)
    if "displayName" in body and denied_display_name(response):
        reduced = {key: value for key, value in body.items() if key != "displayName"}
        if reduced:
            return http.put(f"/v1/columns/name/{fqn}", params={"entityType": "table"}, json=reduced), True
    return response, False


def update_column(
    http: httpx.Client, fqn: str, dp: Datapoint, axis_column: str | None, label: str, keep_labels: bool = False
) -> tuple[httpx.Response, bool]:
    """Set one column's description, display name and glossary terms, addressed by name.

    `PUT /v1/columns/name/{fqn}` rather than a JSON patch on /columns/N: the index is
    positional and the array an agent reads back is paginated and trimmed, so N does not
    mean the same thing on both sides. PATCH on this resource answers 405 - verified -
    so PUT is the path, and it takes all three together.
    """
    return put_column(
        http,
        fqn,
        {
            "description": (
                dp.description_without_variant(axis_column, keep_labels) if axis_column else dp.description(keep_labels)
            ),
            "displayName": label,
            "tags": [{"tagFQN": term, "source": "Glossary"} for term in dp.glossary_terms()],
        },
    )


# --------------------------------------------------------------------------------------
# Agent-facing tools.
#
# The batch writer above generates its own text from the pack. An agent writes its own,
# one column at a time, and needs the other half: what is there now. These are the two
# halves as tool functions, returning JSON-shaped dicts rather than printing.
#
# The safety rail is `expect_current`. A bot token cannot overwrite a non-empty
# description through this endpoint - EntityRepository.updateDescription keeps the
# existing text and answers 200, so a write that did nothing looks exactly like a write
# that worked. Every write is therefore read back and compared, and a column that already
# says something is refused until the caller has read it and passed it back. That makes
# the agent acknowledge what it is replacing, and turns the silent no-op into a reported
# one.
# --------------------------------------------------------------------------------------


def quote_part(part: str) -> str:
    """Quote one FQN part the way the server's FullyQualifiedName does, when it must."""
    return f'"{part}"' if ("." in part or '"' in part) else part


def column_fqn(table_fqn: str, column_name: str) -> str:
    """The column entity's FQN: the table's FQN as the catalogue gives it, then the column.

    Only the column name is quoted here. The table FQN comes from a search result or the
    command line and already carries whatever quoting its own parts need.
    """
    return f"{table_fqn}.{quote_part(column_name)}"


def client(settings: Settings) -> httpx.Client:
    """The one place the HTTP client is configured. Used by the CLI and by the tools."""
    return httpx.Client(
        base_url=settings.host.rstrip("/"),
        headers={"Authorization": f"Bearer {settings.jwt_token}"},
        verify=settings.ca_bundle or True,
        timeout=120.0,
    )


def summarise(column: dict) -> dict[str, Any]:
    """One column as an agent needs to see it, with the empty fields left out.

    Pure. `described` is spelled out rather than left to be inferred from a null, because
    whether a column already says something is the fact that decides what happens next.
    """
    text = (column.get("description") or "").strip()
    terms = [tag["tagFQN"] for tag in column.get("tags") or [] if tag.get("source") == "Glossary"]
    summary: dict[str, Any] = {
        "name": column.get("name"),
        "data_type": column.get("dataType"),
        "described": bool(text),
    }
    if column.get("displayName"):
        summary["display_name"] = column["displayName"]
    if text:
        summary["description"] = text
    if terms:
        summary["terms"] = terms
    return summary


def fetch_column(http: httpx.Client, fqn: str) -> dict:
    """One column entity by name. PUT is the only write; GET is how you check one."""
    response = http.get(f"/v1/columns/name/{fqn}", params={"entityType": "table"})
    if response.status_code == 404:
        return {}
    response.raise_for_status()
    return response.json()


def read_table_metadata(table_fqn: str) -> dict[str, Any]:
    """What the table and every one of its columns says now, in one call.

    One call rather than one per column: an agent about to describe a table wants to know
    which columns are already done, and asking forty times to find out is forty round
    trips and forty chances to lose track.
    """
    try:
        with client(Settings()) as http:  # type: ignore[call-arg]
            table = fetch_table(http, table_fqn)
    except Exception as exc:  # noqa: BLE001 - a tool reports its failures, it does not raise them
        return {"table": table_fqn, "error": f"{type(exc).__name__}: {exc}"}

    columns = [summarise(column) for column in table["columns"]]
    answer: dict[str, Any] = {"table": table_fqn}
    if table.get("displayName"):
        answer["display_name"] = table["displayName"]
    if (table.get("description") or "").strip():
        answer["description"] = table["description"].strip()
    return answer | {
        "total": len(columns),
        "described": sum(1 for column in columns if column["described"]),
        "columns": columns,
    }


def read_column_description(table_fqn: str, column_name: str) -> dict[str, Any]:
    """What one column says now, and the FQN to write it back by."""
    fqn = column_fqn(table_fqn, column_name)
    try:
        with client(Settings()) as http:  # type: ignore[call-arg]
            column = fetch_column(http, fqn)
    except Exception as exc:  # noqa: BLE001
        return {"column_fqn": fqn, "error": f"{type(exc).__name__}: {exc}"}
    if not column:
        return {
            "column_fqn": fqn,
            "found": False,
            "message": (
                "No such column. Check the table FQN and the column name against "
                "read_table_descriptions, which lists the names as the catalogue spells them."
            ),
        }
    return {"column_fqn": fqn, "found": True} | summarise(column)


def write_column_metadata(
    table_fqn: str,
    column_name: str,
    description: str | None = None,
    display_name: str | None = None,
    expect_current: str | None = None,
    terms: list[str] | None = None,
) -> dict[str, Any]:
    """Set one column's description, display name and terms, and prove they landed.

    The guard is on the description only. That is the field someone may have written
    prose into, and the field a bot token is silently refused on; a display name is a
    label, and one passed here replaces whatever is there. Omit what you do not mean to
    change: this endpoint leaves a field alone when the body does not carry it.

    Then it writes, reads back, and compares. This endpoint answers 200 for a write a bot
    token was not allowed to make, so the read-back is the only thing that distinguishes
    written from ignored.
    """
    fqn = column_fqn(table_fqn, column_name)
    wanted = (description or "").strip()
    label = (display_name or "").strip()
    if not wanted and not label:
        return {"column_fqn": fqn, "written": False, "reason": "nothing to set"}

    try:
        with client(Settings()) as http:  # type: ignore[call-arg]
            before = fetch_column(http, fqn)
            if not before:
                return {"column_fqn": fqn, "written": False, "reason": "no such column"}

            current = (before.get("description") or "").strip()
            current_label = (before.get("displayName") or "").strip()
            if (not wanted or current == wanted) and (not label or current_label == label):
                return {
                    "column_fqn": fqn,
                    "written": False,
                    "unchanged": True,
                    "description": current,
                    "display_name": current_label,
                }
            if wanted and current:
                if expect_current is None:
                    return {
                        "column_fqn": fqn,
                        "written": False,
                        "reason": "already described, and nothing says you read it",
                        "current": current,
                        "retry": (
                            "If replacing it is right, call again with expect_current set to the "
                            "text above. If it is someone else's and still correct, leave it."
                        ),
                    }
                if expect_current.strip() != current:
                    return {
                        "column_fqn": fqn,
                        "written": False,
                        "reason": "it says something else now - someone changed it after you read it",
                        "current": current,
                    }

            # Only the fields actually being set go in the body. Sending a field as empty
            # would clear it, which is not the same as not mentioning it.
            body: dict[str, Any] = {}
            if wanted:
                body["description"] = wanted
            if label:
                body["displayName"] = label
            if terms is not None:
                # Omitting tags leaves the existing ones alone; an empty list clears them.
                body["tags"] = [{"tagFQN": term, "source": "Glossary"} for term in terms]
            response, denied_label = put_column(http, fqn, body)
            if response.status_code >= 400:
                return {
                    "column_fqn": fqn,
                    "written": False,
                    "reason": f"{response.status_code} {response.text[:200]}",
                    "hint": (
                        "A 404 here is usually a glossary term that does not exist: the endpoint "
                        "validates every term. Retry without terms to set the description alone."
                    ),
                }
            after = fetch_column(http, fqn)
    except Exception as exc:  # noqa: BLE001
        return {"column_fqn": fqn, "written": False, "reason": f"{type(exc).__name__}: {exc}"}

    kept = [
        field
        for field, value, stored in (
            ("description", wanted, after.get("description")),
            ("display_name", label if not denied_label else "", after.get("displayName")),
        )
        if value and not landed(value, stored)
    ]
    if kept:
        return {
            "column_fqn": fqn,
            "written": False,
            "reason": f"the server answered 200 and kept the old {' and '.join(kept)}",
            "current_description": (after.get("description") or "").strip(),
            "current_display_name": (after.get("displayName") or "").strip(),
            "hint": (
                "A bot token cannot overwrite a non-empty description through this endpoint. "
                "Use a user token, or have a person make the change."
            ),
        }
    answer: dict[str, Any] = {"column_fqn": fqn, "written": True}
    if wanted:
        answer["description"] = wanted
    if label and not denied_label:
        answer["display_name"] = label
    if denied_label:
        # Reported rather than silent: the label is not there, and a later read would make
        # it look as though nobody had tried.
        answer["display_name_refused"] = (
            "this token may not edit display names - OpenMetadata denies EditDisplayName to "
            "application bots by policy. The description was written. Ask for a personal access "
            "token if labels matter, and do not retry this call."
        )
    if terms is not None:
        answer["terms"] = terms
    return answer


def write_table_metadata(
    table_fqn: str,
    description: str | None = None,
    display_name: str | None = None,
    expect_current: str | None = None,
    replace: bool = False,
    terms: list[str] | None = None,
) -> dict[str, Any]:
    """Set the table's own description and display name, and prove they landed.

    A JSON patch, which is right here and wrong for columns: the table's description and
    displayName are scalar fields at known paths, not positions in an array that is
    paginated differently on each side.

    Same guard and same read-back as the column tool, for the same reasons. `replace` skips
    the guard and is not in the tool schema: the batch writer regenerates a description it
    wrote itself, which is not the case the guard is about.
    """
    wanted = (description or "").strip()
    label = (display_name or "").strip()
    if not wanted and not label:
        return {"table": table_fqn, "written": False, "reason": "nothing to set"}

    try:
        with client(Settings()) as http:  # type: ignore[call-arg]
            response = http.get(f"/v1/tables/name/{table_fqn}", params={"fields": "tags"})
            if response.status_code == 404:
                return {"table": table_fqn, "written": False, "reason": "no such table"}
            response.raise_for_status()
            before = response.json()

            current = (before.get("description") or "").strip()
            current_label = (before.get("displayName") or "").strip()
            if (not wanted or current == wanted) and (not label or current_label == label):
                return {
                    "table": table_fqn,
                    "written": False,
                    "unchanged": True,
                    "description": current,
                    "display_name": current_label,
                }
            if wanted and current and not replace:
                if expect_current is None:
                    return {
                        "table": table_fqn,
                        "written": False,
                        "reason": "already described, and nothing says you read it",
                        "current": current,
                        "retry": (
                            "If replacing it is right, call again with expect_current set to the "
                            "text above. If it is someone else's and still correct, leave it."
                        ),
                    }
                if expect_current.strip() != current:
                    return {
                        "table": table_fqn,
                        "written": False,
                        "reason": "it says something else now - someone changed it after you read it",
                        "current": current,
                    }

            # `add` and `replace` are not interchangeable: replace on a field the entity
            # does not carry yet is rejected, which is why the current value decides.
            patch: list[dict[str, Any]] = [
                {"op": "replace" if present else "add", "path": path, "value": value}
                for path, value, present in (
                    ("/description", wanted, bool(current)),
                    ("/displayName", label, bool(current_label)),
                )
                if value
            ]
            # Tags are a whole-array patch, so the existing ones have to be carried over:
            # a table may well have a tier or a PII tag that is nothing to do with us.
            existing = before.get("tags") or []
            if terms and not {tag.get("tagFQN") for tag in existing} >= set(terms):
                keep = [{"tagFQN": tag["tagFQN"], "source": tag.get("source", "Classification")} for tag in existing]
                have = {tag["tagFQN"] for tag in keep}
                keep += [{"tagFQN": term, "source": "Glossary"} for term in terms if term not in have]
                patch.append({"op": "replace" if existing else "add", "path": "/tags", "value": keep})
            headers = {"Content-Type": "application/json-patch+json"}
            response = http.patch(f"/v1/tables/name/{table_fqn}", content=json.dumps(patch), headers=headers)
            denied_label = False
            if denied_display_name(response):
                # Drop the label and keep the description, for the same reason as a column.
                remaining = [op for op in patch if op["path"] != "/displayName"]
                denied_label = True
                if not remaining:
                    return {
                        "table": table_fqn,
                        "written": False,
                        "reason": "this token may not edit display names",
                        "hint": (
                            "OpenMetadata denies EditDisplayName to application bots by policy. Use a "
                            "personal access token to set labels, or set only the description."
                        ),
                    }
                response = http.patch(f"/v1/tables/name/{table_fqn}", content=json.dumps(remaining), headers=headers)
            if response.status_code >= 400:
                return {"table": table_fqn, "written": False, "reason": f"{response.status_code} {response.text[:200]}"}
            after = http.get(f"/v1/tables/name/{table_fqn}").json()
    except Exception as exc:  # noqa: BLE001
        return {"table": table_fqn, "written": False, "reason": f"{type(exc).__name__}: {exc}"}

    kept = [
        field
        for field, value, stored in (
            ("description", wanted, after.get("description")),
            ("display_name", label if not denied_label else "", after.get("displayName")),
        )
        if value and not landed(value, stored)
    ]
    if kept:
        return {
            "table": table_fqn,
            "written": False,
            "reason": f"the server answered 200 and kept the old {' and '.join(kept)}",
            "current_description": (after.get("description") or "").strip(),
            "current_display_name": (after.get("displayName") or "").strip(),
        }
    answer: dict[str, Any] = {"table": table_fqn, "written": True}
    if wanted:
        answer["description"] = wanted
    if label and not denied_label:
        answer["display_name"] = label
    if denied_label:
        answer["display_name_refused"] = "this token may not edit display names"
    return answer


READ_TABLE_METADATA_TOOL_NAME = "read_table_metadata"
READ_TABLE_METADATA_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": READ_TABLE_METADATA_TOOL_NAME,
        "description": (
            "Read a table in OpenMetadata: its own display name and description, then every column "
            "with the display name, description, data type and glossary terms it has now. Call this "
            "before writing anything - it says which columns are already done and spells the column "
            "names the way the catalogue does. Reads only."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "table_fqn": {
                    "type": "string",
                    "description": "Fully qualified table name, e.g. SQLSASTest.FIDW_BI.dbo.Y_01_01",
                },
            },
            "required": ["table_fqn"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

WRITE_COLUMN_METADATA_TOOL_NAME = "write_column_metadata"
WRITE_COLUMN_METADATA_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": WRITE_COLUMN_METADATA_TOOL_NAME,
        "description": (
            "Set one column's description, display name and glossary terms, and verify they landed. "
            "Pass null for anything you do not mean to change. Replacing an existing description is "
            "refused unless expect_current repeats it exactly, so read the column first - the "
            "refusal returns the current text, so one retry is enough. A display name is not "
            "guarded: one passed here replaces whatever is there. A false answer saying the server "
            "kept the old text means the token is not allowed to replace it, not that your text was "
            "wrong - do not rewrite it in response."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "table_fqn": {
                    "type": "string",
                    "description": "Fully qualified table name, e.g. SQLSASTest.FIDW_BI.dbo.Y_01_01",
                },
                "column_name": {
                    "type": "string",
                    "description": "The column's name as the catalogue spells it, e.g. Y0101_r0010_c0010",
                },
                "description": {
                    "type": ["string", "null"],
                    "description": "The description to set, Markdown allowed. Null leaves it alone.",
                },
                "display_name": {
                    "type": ["string", "null"],
                    "description": (
                        "The label the catalogue shows instead of the column name, e.g. "
                        "'Credit transfers - Payment transactions'. Null leaves it alone. Keep the "
                        "variant out of it: the variant belongs to the table or the row, so putting "
                        "it here would make several columns claim to be one."
                    ),
                },
                "expect_current": {
                    "type": ["string", "null"],
                    "description": (
                        "The description the column has now, repeated exactly, when replacing one. "
                        "Null when it has none or when you are not setting a description."
                    ),
                },
                "terms": {
                    "type": ["array", "null"],
                    "items": {"type": "string"},
                    "description": (
                        "Glossary term FQNs to attach, e.g. PAY_4_2.Domains.Fraud event types.Unauthorised. "
                        "Null leaves the existing terms alone; an empty list clears them. Every term "
                        "must exist or the write fails."
                    ),
                },
            },
            "required": ["table_fqn", "column_name", "description", "display_name", "expect_current", "terms"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

WRITE_TABLE_METADATA_TOOL_NAME = "write_table_metadata"
WRITE_TABLE_METADATA_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": WRITE_TABLE_METADATA_TOOL_NAME,
        "description": (
            "Set the table's own description and display name, and verify they landed. Same rules as "
            "write_column_metadata: null for what you do not mean to change, expect_current to "
            "replace an existing description, and a display name is not guarded."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "table_fqn": {
                    "type": "string",
                    "description": "Fully qualified table name, e.g. SQLSASTest.FIDW_BI.dbo.Y_01_01",
                },
                "description": {
                    "type": ["string", "null"],
                    "description": "The description to set, Markdown allowed. Null leaves it alone.",
                },
                "display_name": {
                    "type": ["string", "null"],
                    "description": (
                        "The label the catalogue shows instead of the table name, e.g. "
                        "'Y 01.01 Credit transfers transactions'. Null leaves it alone."
                    ),
                },
                "expect_current": {
                    "type": ["string", "null"],
                    "description": "The description the table has now, repeated exactly, when replacing one.",
                },
            },
            "required": ["table_fqn", "description", "display_name", "expect_current"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

CATALOGUE_TOOL_DEFINITIONS = (
    READ_TABLE_METADATA_TOOL_DEFINITION,
    WRITE_COLUMN_METADATA_TOOL_DEFINITION,
    WRITE_TABLE_METADATA_TOOL_DEFINITION,
)


# The server sanitises on write: the OWASP policy HTML-escapes `<`, `>`, `&` and `+`, so
# what comes back is never byte-identical to what went out. Comparing exactly reported a
# write that had in fact landed as "the server kept the old description" - a false alarm
# that reads exactly like the real bot-token refusal it was meant to catch.
ESCAPES = (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&#43;", "+"), ("&#39;", "'"), ("&quot;", '"'))


def unescaped(stored: str | None) -> str:
    """Stored text with the sanitiser's escapes undone, for comparison only."""
    text = stored or ""
    for escape, char in ESCAPES:
        text = text.replace(escape, char)
    return text.strip()


def landed(wanted: str, stored: str | None) -> bool:
    """Did what we sent survive the write, allowing for sanitisation?"""
    return unescaped(stored) == wanted.strip()


def article_reference(table: str, settings: Settings) -> str:
    """How to point at the Context Center article for a template.

    A link when the route is configured, the article's name otherwise. Naming it is worth
    doing either way: `find_context` resolves an article by name, so an agent can reach it
    from the name alone even where a person needs the URL.
    """
    if settings.page_url:
        return f"Full template reference: [{table}]({settings.page_url.format(name=table, fqn=table)})."
    return f"Full template reference: the Context Center article named {table}."


def report_table_write(written: dict[str, Any]) -> None:
    """Say what landed on the table itself. Both frameworks write it the same way."""
    if written.get("written"):
        refused = written.get("display_name_refused")
        print(
            "  table: description set"
            + (", display name refused (token may not set them)" if refused else ", display name set")
        )
    else:
        print(f"  table: not written - {written.get('reason')}")


def dora_display_names(dora: dict[str, DoraDatapoint]) -> dict[str, str]:
    """Column name to display name, unique within the table.

    Two ways a DORA label repeats, and they need different disambiguators. An open-row
    template matches on the column code alone, so several physical columns resolve to one
    datapoint and only the row ordinal differs. And a fixed template can reuse a column
    label under several column groups - B_99.01 has "Low", "Medium" and "High" three times
    over, same row, three different column codes - where only the column code differs.

    So the group decides: whichever of the two codes varies inside it is appended. That is
    a code in a label, which the PAY rule avoids, but the DORA export carries no
    column-group label, so there is nothing else that tells these apart. A code beats
    three columns that look identical.
    """
    groups: dict[str, list[str]] = defaultdict(list)
    for name, dp in dora.items():
        groups[dp.display_name()].append(name)

    labels: dict[str, str] = {}
    for label, names in groups.items():
        if len(names) == 1:
            labels[names[0]] = label
            continue
        # The physical name carries the ordinal an open template needs; the datapoint
        # carries the codes when the name is a pattern rather than a column.
        parts = {
            name: split_column_name(name) or {"row": dora[name].row_code, "col": dora[name].column_code}
            for name in names
        }
        rows = {part["row"] for part in parts.values()}
        columns = {part["col"] for part in parts.values()}
        for name in names:
            part = parts[name]
            codes = [f"r{part['row']}"] if len(rows) > 1 else []
            codes += [f"c{part['col']}"] if len(columns) > 1 else []
            labels[name] = f"{label} ({' '.join(codes)})" if codes else label
    return labels


def write_dora(
    http: httpx.Client, args: argparse.Namespace, fqn: str, table: str, dora: dict[str, DoraDatapoint]
) -> bool:
    """Describe a DORA table. Separate from the PAY path because almost nothing is shared.

    No variants, so there is no variant to establish and nothing to withhold; no open
    sheet axis either, so every column gets its datapoint id.
    """
    first = next(iter(dora.values()))
    label = f"{first.template.replace('_', ' ')} {first.template_name}"
    labels = dora_display_names(dora)
    print(f"{fqn}: {len(dora)} DORA datapoint column(s) to describe")

    if not args.commit:
        name, dp = next(iter(dora.items()))
        print(f"\n  Table display name: {label}")
        print(f"  Table description: {dora_table_description(dora, article_reference(table, Settings()))}")  # type: ignore[call-arg]
        if not args.no_terms:
            print(f"  Table term: {DORA_GLOSSARY}.Templates.{table}")
        print(f"\n  Example, {name}:")
        print(f"    display name: {labels[name]}")
        print(f"    {dp.description(args.labels_in_description)}")
        if not args.no_terms:
            for term in load_dora_terms().get((dp.template, dp.column_code), []):
                print(f"    term: {term}")
        print(f"\n  Nothing written. Re-run with --commit to write all {len(dora)}.")
        return True

    settings = Settings()  # type: ignore[call-arg]
    written = write_table_metadata(
        fqn,
        dora_table_description(dora, article_reference(table, settings)),
        label,
        replace=True,
        terms=None if args.no_terms else [f"{DORA_GLOSSARY}.Templates.{table}"],
    )
    report_table_write(written)

    terms = {} if args.no_terms else load_dora_terms()

    failed, unlabelled = [], 0
    for name, dp in dora.items():
        body: dict[str, Any] = {
            "description": dp.description(args.labels_in_description),
            "displayName": labels[name],
        }
        if not args.no_terms:
            # Omitting tags leaves the existing ones alone, so only send the key when there
            # is something to say. A column with no vocabulary row keeps whatever it has.
            for_column = terms.get((dp.template, dp.column_code), [])
            if for_column:
                body["tags"] = [{"tagFQN": term, "source": "Glossary"} for term in for_column]
        response, dropped = put_column(http, column_fqn(fqn, name), body)
        unlabelled += dropped
        if response.status_code >= 400:
            failed.append(f"{name}: {response.status_code} {response.text[:160]}")

    print(f"  {len(dora) - len(failed)} written, {len(failed)} failed")
    if not args.no_terms:
        tagged = sum(1 for dp in dora.values() if terms.get((dp.template, dp.column_code)))
        print(f"  {tagged} column(s) carried glossary terms from {DORA_GLOSSARY}")
    if unlabelled:
        print(f"  {unlabelled} description(s) written without a display name: this token may not set them.")
    for line in failed[:10]:
        print(f"  x {line}")
    return not failed


def describe_one(http: httpx.Client, args: argparse.Namespace, fqn: str, by_column: dict) -> bool:
    """Describe one table. Returns whether it was clean, and never exits the process."""
    by_column = load_datapoints()
    try:
        columns = fetch_columns(http, fqn)
    except CatalogueError as exc:
        print(f"{fqn}: {exc}")
        return False
    table = fqn.rsplit(".", 1)[-1]
    axis_column = find_open_axis(columns)

    # DORA first, because a DORA table has no PAY datapoints at all and would
    # otherwise report "0 to describe" with no reason given - which is what it did.
    dora = dora_for_table(table, [column.get("name", "") for column in columns])
    if dora:
        return write_dora(http, args, fqn, table, dora)

    if axis_column and args.variant:
        print(
            f"{fqn}: has an open axis, `{axis_column}`, so it holds every variant as rows "
            f"and a column is not one of them. Drop --variant: the descriptions will say what "
            f"holds for all six and name `{axis_column}` as where the rest comes from."
        )
        return False
    check_variant(by_column, table, args.variant)

    write, skipped = columns_to_write(columns, by_column, args.variant, axis_column)

    # Over every datapoint of the template, not just the columns present: the rule
    # disambiguates a repeated label from its siblings, and a sibling missing from
    # this table must not change what the others are called.
    labels = display_names([dps[0].model_dump() for dps in by_column.values() if dps[0].table_name == table])

    print(f"{fqn}: {len(columns)} columns, {len(write)} to describe")
    if axis_column:
        print(f"  open axis `{axis_column}`: every variant is present as rows, so descriptions omit")
        print("  the datapoint id and the unit and point at that column instead.")
    if skipped:
        per_variant = len({dp.column_name for dps in by_column.values() for dp in dps if dp.table_name == table})
        print(
            f"  {len(skipped)} datapoint column(s) skipped because no variant was given. "
            f"{table} has {per_variant} datapoint columns per variant; this table has "
            f"{len(skipped)}, so it holds one variant and only the pipeline that loads it "
            "knows which. Pass --variant once you know."
        )
    if not write:
        print(
            "  Nothing to write. "
            + (
                f"No datapoint in this pack belongs to {table}. PAY templates are Y_*, DORA are "
                "B_*; anything else is a framework this pack does not cover."
                if not any(dps[0].table_name == table for dps in by_column.values())
                else "Every datapoint column is already current."
            )
        )
        return True

    if not args.commit:
        fqn, dp = write[0]
        for_table = [dp for dps in by_column.values() for dp in dps if dp.table_name == table]
        for_table = [dp for dps in by_column.values() for dp in dps if dp.table_name == table]
        print(f"\n  Table display name: {table_name(dp.model_dump())}")
        print(
            "  Table description: "
            + pay_table_description(for_table, axis_column, args.variant, article_reference(table, Settings()))  # type: ignore[call-arg]
        )
        if not args.no_terms:
            print(f"  Table term: {GLOSSARY}.Templates.{table}")
        print(f"  Table description: {pay_table_description(for_table, axis_column, args.variant)}")
        print(f"\n  Example, {fqn.rsplit('.', 1)[-1]}:")
        print(f"    display name: {labels[dp.column_name]}")
        print(
            "    "
            + (
                dp.description_without_variant(axis_column, args.labels_in_description)
                if axis_column
                else dp.description(args.labels_in_description)
            )
        )
        if not args.no_terms:
            for term in dp.glossary_terms():
                print(f"    term: {term}")
        print(f"\n  Nothing written. Re-run with --commit to write all {len(write)}.")
        return True

    for_table = [dp for dps in by_column.values() for dp in dps if dp.table_name == table]
    settings = Settings()  # type: ignore[call-arg]
    report_table_write(
        write_table_metadata(
            fqn,
            pay_table_description(for_table, axis_column, args.variant, article_reference(table, settings)),
            table_name(write[0][1].model_dump()),
            replace=True,
            terms=None if args.no_terms else [f"{GLOSSARY}.Templates.{table}"],
        )
    )

    failed = []
    unlabelled = 0
    for fqn, dp in write:
        if args.no_terms:
            text = (
                dp.description_without_variant(axis_column, args.labels_in_description)
                if axis_column
                else dp.description(args.labels_in_description)
            )
            response, dropped = put_column(http, fqn, {"description": text, "displayName": labels[dp.column_name]})
        else:
            response, dropped = update_column(
                http, fqn, dp, axis_column, labels[dp.column_name], args.labels_in_description
            )
        unlabelled += dropped
        if response.status_code >= 400:
            failed.append(f"{fqn.rsplit('.', 1)[-1]}: {response.status_code} {response.text[:160]}")

    print(f"  {len(write) - len(failed)} written, {len(failed)} failed")
    if unlabelled:
        print(
            f"  {unlabelled} description(s) written without a display name: this token may not "
            "edit display names.\n  OpenMetadata denies EditDisplayName to application bots by "
            "policy. Use a personal access token to set labels."
        )
    for line in failed[:10]:
        print(f"  x {line}")
    if failed:
        print(
            "  A 404 here usually means a glossary term does not exist: the endpoint validates "
            "them. Load the glossary first, or re-run with --no-terms."
        )
    return not failed


def list_tables(http: httpx.Client, pattern: str) -> list[str]:
    """Table FQNs in a schema matching a shell-style pattern in the last part.

    `SQLSASTest.FIDW_BI.dbo.Y*` asks the catalogue which tables exist rather than guessing
    from the pack: a template this pack describes may not be loaded, and a table that is
    loaded may be a framework it does not cover. Only the table name may be a pattern -
    the schema has to be named, because that is what the listing is scoped to.
    """
    schema, _, name = pattern.rpartition(".")
    if not schema:
        raise CatalogueError(f"{pattern} is not a table FQN: it needs service.database.schema.table")

    found: list[str] = []
    after: str | None = None
    while True:
        params: dict[str, Any] = {"databaseSchema": schema, "limit": 500}
        if after:
            params["after"] = after
        response = http.get("/v1/tables", params=params)
        if response.status_code >= 400:
            raise CatalogueError(f"Listing {schema} failed: {response.status_code} {response.text[:300]}")
        body = response.json()
        found.extend(
            table["fullyQualifiedName"] for table in body.get("data") or [] if fnmatch(table.get("name", ""), name)
        )
        after = (body.get("paging") or {}).get("after")
        if not after:
            return sorted(found)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "fqn",
        help="table FQN, e.g. SQLSASTest.FIDW_BI.dbo.Y_01_01. The table part may be a pattern: "
        "'SQLSASTest.FIDW_BI.dbo.Y*' - quote it, or the shell will try to expand it",
    )
    parser.add_argument("--variant", help="which variant this table holds, e.g. 0010")
    parser.add_argument("--commit", action="store_true", help="write for real; dry run only without it")
    parser.add_argument("--no-terms", action="store_true", help="set descriptions but do not attach glossary terms")
    parser.add_argument("--show", action="store_true", help="print what the columns say now, as JSON, and stop")
    parser.add_argument(
        "--labels-in-description",
        action="store_true",
        help="repeat the row and column labels in the description, for a token that may not set display names",
    )
    args = parser.parse_args()

    settings = Settings()  # type: ignore[call-arg]
    with client(settings) as http:
        try:
            targets = list_tables(http, args.fqn) if "*" in args.fqn or "?" in args.fqn else [args.fqn]
        except CatalogueError as exc:
            raise SystemExit(f"  {exc}") from exc

        if not targets:
            raise SystemExit(f"  No table in the catalogue matches {args.fqn}.")

        if args.show:
            for fqn in targets:
                print(json.dumps(read_table_metadata(fqn), ensure_ascii=False, indent=2))
            return

        # A variant belongs to one table, so it cannot mean anything across a pattern.
        if args.variant and len(targets) > 1:
            raise SystemExit(
                f"  --variant names the variant one table holds, and {args.fqn} matched {len(targets)}. "
                "Run them one at a time, or drop it."
            )

        by_column = load_datapoints()
        results = {fqn: describe_one(http, args, fqn, by_column) for fqn in targets}

    if len(results) > 1:
        clean = sum(results.values())
        print(f"\n{len(results)} tables: {clean} clean, {len(results) - clean} with problems")
        for fqn, ok in sorted(results.items()):
            if not ok:
                print(f"  x {fqn}")
    if not all(results.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
