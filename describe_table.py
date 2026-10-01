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
from pathlib import Path
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

PACK = Path(__file__).parent
DATAPOINTS = PACK / "05-datapoints.csv"

# Only these are framework columns. Everything else is warehouse context and is left alone.
DATAPOINT_COLUMN = re.compile(r"^[A-Za-z][0-9]{4}_r[0-9]{4}_c[0-9]{4}$")

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


class Datapoint(BaseModel):
    """One row of 05-datapoints.csv. Frozen: read once, then only read from."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    column_name: str
    table_name: str
    datapoint_id: str
    template: str
    variant: str
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

    def description_without_variant(self, axis_column: str) -> str:
        """What holds across every variant, for a table that carries all of them.

        No datapoint id and no unit: those differ per variant, and here the variant is a
        property of the row rather than of the table. Naming the axis column is what lets
        a reader get from this description to the specific datapoint.
        """
        members = "; ".join(f"{dim} = {member}" for dim, member in self.dimension_members)
        return (
            f"{self.row_label} — {self.column_label}. "
            + (f"Dimension members: {members}. " if members else "")
            + f"Template {self.template} (EBA PAY 4.2), row {self.row_code}, column {self.column_code}. "
            f"This table holds every variant; `{axis_column}` on each row gives the metric and "
            "geography, and with it the datapoint id and the unit. Non-negative."
        )

    def description(self) -> str:
        unit = "monetary amount" if self.unit != "#" else "count"
        members = "; ".join(f"{dim} = {member}" for dim, member in self.dimension_members)
        return (
            f"{self.row_label} — {self.column_label}, {self.metric.lower()} for {self.geography}. "
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


def fetch_columns(http: httpx.Client, table_fqn: str) -> list[dict]:
    """Every column of the table, paging until the server stops truncating."""
    columns: list[dict] = []
    offset = 0
    while True:
        response = http.get(f"/v1/tables/name/{table_fqn}", params={"fields": "columns", "columnOffset": offset})
        if response.status_code >= 400:
            raise SystemExit(f"  Reading {table_fqn} failed: {response.status_code}\n  {response.text[:500]}")
        body = response.json()
        page = body.get("columns") or []
        columns.extend(page)
        if not body.get("columnsTruncated") or not page:
            return columns
        offset += len(page)


def update_column(http: httpx.Client, fqn: str, dp: Datapoint, axis_column: str | None) -> httpx.Response:
    """Set one column's description and glossary terms, addressed by name.

    `PUT /v1/columns/name/{fqn}` rather than a JSON patch on /columns/N: the index is
    positional and the array an agent reads back is paginated and trimmed, so N does not
    mean the same thing on both sides. PATCH on this resource answers 405 - verified -
    so PUT is the path, and it takes description and tags together.
    """
    return http.put(
        f"/v1/columns/name/{fqn}",
        params={"entityType": "table"},
        json={
            "description": dp.description_without_variant(axis_column) if axis_column else dp.description(),
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


def read_table_descriptions(table_fqn: str) -> dict[str, Any]:
    """What every column of a table says now, in one call.

    One call rather than one per column: an agent about to describe a table wants to know
    which columns are already done, and asking forty times to find out is forty round
    trips and forty chances to lose track.
    """
    try:
        with client(Settings()) as http:  # type: ignore[call-arg]
            columns = [summarise(column) for column in fetch_columns(http, table_fqn)]
    except Exception as exc:  # noqa: BLE001 - a tool reports its failures, it does not raise them
        return {"table": table_fqn, "error": f"{type(exc).__name__}: {exc}"}
    return {
        "table": table_fqn,
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


def write_column_description(
    table_fqn: str,
    column_name: str,
    description: str,
    expect_current: str | None = None,
    terms: list[str] | None = None,
) -> dict[str, Any]:
    """Set one column's description, and prove it landed.

    Refuses to replace an existing description unless `expect_current` repeats it, so
    nothing a person wrote is overwritten by an agent that never read it. Then writes,
    reads back, and compares: this endpoint answers 200 for a write a bot token was not
    allowed to make, so the read-back is the only thing that distinguishes written from
    ignored.
    """
    fqn = column_fqn(table_fqn, column_name)
    wanted = description.strip()
    if not wanted:
        return {"column_fqn": fqn, "written": False, "reason": "empty description"}

    try:
        with client(Settings()) as http:  # type: ignore[call-arg]
            before = fetch_column(http, fqn)
            if not before:
                return {"column_fqn": fqn, "written": False, "reason": "no such column"}

            current = (before.get("description") or "").strip()
            if current == wanted:
                return {"column_fqn": fqn, "written": False, "unchanged": True, "description": current}
            if current:
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

            body: dict[str, Any] = {"description": wanted}
            if terms is not None:
                # Omitting tags leaves the existing ones alone; an empty list clears them.
                body["tags"] = [{"tagFQN": term, "source": "Glossary"} for term in terms]
            response = http.put(f"/v1/columns/name/{fqn}", params={"entityType": "table"}, json=body)
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
            after = (fetch_column(http, fqn).get("description") or "").strip()
    except Exception as exc:  # noqa: BLE001
        return {"column_fqn": fqn, "written": False, "reason": f"{type(exc).__name__}: {exc}"}

    if after != wanted:
        return {
            "column_fqn": fqn,
            "written": False,
            "reason": "the server answered 200 and kept the old text",
            "current": after,
            "hint": (
                "A bot token cannot overwrite a non-empty description through this endpoint. "
                "Use a user token, or have a person make the change."
            ),
        }
    return {"column_fqn": fqn, "written": True, "description": wanted, "terms": terms or []}


READ_TABLE_DESCRIPTIONS_TOOL_NAME = "read_table_descriptions"
READ_TABLE_DESCRIPTIONS_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": READ_TABLE_DESCRIPTIONS_TOOL_NAME,
        "description": (
            "List every column of a table in OpenMetadata with the description it has now, its "
            "data type, and any glossary terms attached. Call this before describing a table: it "
            "says which columns are already done and which are empty, and spells the column names "
            "the way the catalogue does. Reads only."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "table_fqn": {
                    "type": "string",
                    "description": "Fully qualified table name, e.g. SQLSASTest.FIDW_BI.dbo.Y_01_01",
                }
            },
            "required": ["table_fqn"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

WRITE_COLUMN_DESCRIPTION_TOOL_NAME = "write_column_description"
WRITE_COLUMN_DESCRIPTION_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": WRITE_COLUMN_DESCRIPTION_TOOL_NAME,
        "description": (
            "Set one column's description in OpenMetadata, and verify it landed. Writing over an "
            "existing description is refused unless expect_current repeats it exactly, so read the "
            "column first - the refusal returns the current text, so one retry is enough. The "
            "answer says written true or false and why; a false with 'kept the old text' means the "
            "token is not allowed to replace it, not that the text was wrong."
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
                    "type": "string",
                    "description": "The description to set. Markdown is allowed.",
                },
                "expect_current": {
                    "type": ["string", "null"],
                    "description": (
                        "The description the column has now, repeated exactly, when replacing one. "
                        "Null when the column has none."
                    ),
                },
                "terms": {
                    "type": ["array", "null"],
                    "items": {"type": "string"},
                    "description": (
                        "Glossary term FQNs to attach, e.g. PAY_4_2.Fraud event types.Unauthorised. "
                        "Null leaves the existing terms alone; an empty list clears them. Every term "
                        "must exist or the write fails."
                    ),
                },
            },
            "required": ["table_fqn", "column_name", "description", "expect_current", "terms"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

COLUMN_TOOL_DEFINITIONS = (READ_TABLE_DESCRIPTIONS_TOOL_DEFINITION, WRITE_COLUMN_DESCRIPTION_TOOL_DEFINITION)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fqn", help="table FQN, e.g. SQLSASTest.FIDW_BI.dbo.Y_01_01")
    parser.add_argument("--variant", help="which variant this table holds, e.g. 0010")
    parser.add_argument("--commit", action="store_true", help="write for real; dry run only without it")
    parser.add_argument("--no-terms", action="store_true", help="set descriptions but do not attach glossary terms")
    parser.add_argument("--show", action="store_true", help="print what the columns say now, as JSON, and stop")
    args = parser.parse_args()

    if args.show:
        print(json.dumps(read_table_descriptions(args.fqn), ensure_ascii=False, indent=2))
        return

    settings = Settings()  # type: ignore[call-arg]
    with client(settings) as http:
        by_column = load_datapoints()
        columns = fetch_columns(http, args.fqn)
        table = args.fqn.rsplit(".", 1)[-1]
        axis_column = find_open_axis(columns)

        if axis_column and args.variant:
            raise SystemExit(
                f"  {table} has an open axis, `{axis_column}`, so it holds every variant as rows "
                f"and a column is not one of them. Drop --variant: the descriptions will say what "
                f"holds for all six and name `{axis_column}` as where the rest comes from."
            )
        check_variant(by_column, table, args.variant)

        write, skipped = columns_to_write(columns, by_column, args.variant, axis_column)

        print(f"{args.fqn}: {len(columns)} columns, {len(write)} to describe")
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
            raise SystemExit("  Nothing to write.")

        if not args.commit:
            fqn, dp = write[0]
            print(f"\n  Example, {fqn.rsplit('.', 1)[-1]}:")
            print(f"    {dp.description_without_variant(axis_column) if axis_column else dp.description()}")
            if not args.no_terms:
                for term in dp.glossary_terms():
                    print(f"    term: {term}")
            print(f"\n  Nothing written. Re-run with --commit to write all {len(write)}.")
            return

        failed = []
        for fqn, dp in write:
            if args.no_terms:
                text = dp.description_without_variant(axis_column) if axis_column else dp.description()
                response = http.put(
                    f"/v1/columns/name/{fqn}", params={"entityType": "table"}, json={"description": text}
                )
            else:
                response = update_column(http, fqn, dp, axis_column)
            if response.status_code >= 400:
                failed.append(f"{fqn.rsplit('.', 1)[-1]}: {response.status_code} {response.text[:160]}")

        print(f"  {len(write) - len(failed)} written, {len(failed)} failed")
        for line in failed[:10]:
            print(f"  x {line}")
        if failed:
            raise SystemExit(
                "\n  A 404 here usually means a glossary term does not exist: the endpoint validates "
                "them. Load the glossary first, or re-run with --no-terms."
            )


if __name__ == "__main__":
    main()
