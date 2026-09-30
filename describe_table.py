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
import re
from collections import defaultdict
from pathlib import Path

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


def fetch_columns(client: httpx.Client, table_fqn: str) -> list[dict]:
    """Every column of the table, paging until the server stops truncating."""
    columns: list[dict] = []
    offset = 0
    while True:
        response = client.get(f"/v1/tables/name/{table_fqn}", params={"fields": "columns", "columnOffset": offset})
        if response.status_code >= 400:
            raise SystemExit(f"  Reading {table_fqn} failed: {response.status_code}\n  {response.text[:500]}")
        body = response.json()
        page = body.get("columns") or []
        columns.extend(page)
        if not body.get("columnsTruncated") or not page:
            return columns
        offset += len(page)


def update_column(client: httpx.Client, fqn: str, dp: Datapoint, axis_column: str | None) -> httpx.Response:
    """Set one column's description and glossary terms, addressed by name.

    `PUT /v1/columns/name/{fqn}` rather than a JSON patch on /columns/N: the index is
    positional and the array an agent reads back is paginated and trimmed, so N does not
    mean the same thing on both sides. PATCH on this resource answers 405 - verified -
    so PUT is the path, and it takes description and tags together.
    """
    return client.put(
        f"/v1/columns/name/{fqn}",
        params={"entityType": "table"},
        json={
            "description": dp.description_without_variant(axis_column) if axis_column else dp.description(),
            "tags": [{"tagFQN": term, "source": "Glossary"} for term in dp.glossary_terms()],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fqn", help="table FQN, e.g. SQLSASTest.FIDW_BI.dbo.Y_01_01")
    parser.add_argument("--variant", help="which variant this table holds, e.g. 0010")
    parser.add_argument("--commit", action="store_true", help="write for real; dry run only without it")
    parser.add_argument("--no-terms", action="store_true", help="set descriptions but do not attach glossary terms")
    args = parser.parse_args()

    settings = Settings()  # type: ignore[call-arg]
    with httpx.Client(
        base_url=settings.host.rstrip("/"),
        headers={"Authorization": f"Bearer {settings.jwt_token}"},
        verify=settings.ca_bundle or True,
        timeout=120.0,
    ) as client:
        by_column = load_datapoints()
        columns = fetch_columns(client, args.fqn)
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
                response = client.put(
                    f"/v1/columns/name/{fqn}", params={"entityType": "table"}, json={"description": text}
                )
            else:
                response = update_column(client, fqn, dp, axis_column)
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
