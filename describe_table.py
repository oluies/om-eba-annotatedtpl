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


def columns_to_write(
    table_columns: list[dict], by_column: dict[str, list[Datapoint]], variant: str | None
) -> tuple[list[tuple[str, Datapoint]], list[str]]:
    """Pair each datapoint column with the datapoint it reports.

    Pure. Context columns and columns with no datapoint are left out rather than
    described from a framework they do not belong to.
    """
    write, skipped = [], []
    for column in table_columns:
        fqn = column["fullyQualifiedName"]
        name = fqn.rsplit(".", 1)[-1]
        candidates = by_column.get(name)
        if not DATAPOINT_COLUMN.match(name) or not candidates:
            continue
        chosen = pick(candidates, variant)
        if chosen is None:
            skipped.append(f"{name} ({len(candidates)} variants, none chosen)")
            continue
        write.append((fqn, chosen))
    return write, skipped


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


def update_column(client: httpx.Client, fqn: str, dp: Datapoint) -> httpx.Response:
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
            "description": dp.description(),
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
        columns = fetch_columns(client, args.fqn)
        write, skipped = columns_to_write(columns, load_datapoints(), args.variant)

        print(f"{args.fqn}: {len(columns)} columns, {len(write)} to describe")
        for name in skipped:
            print(f"  skipped {name} - pass --variant to choose")
        if not write:
            raise SystemExit("  Nothing to write.")

        if not args.commit:
            fqn, dp = write[0]
            print(f"\n  Example, {fqn.rsplit('.', 1)[-1]}:")
            print(f"    {dp.description()}")
            if not args.no_terms:
                for term in dp.glossary_terms():
                    print(f"    term: {term}")
            print(f"\n  Nothing written. Re-run with --commit to write all {len(write)}.")
            return

        failed = []
        for fqn, dp in write:
            if args.no_terms:
                response = client.put(
                    f"/v1/columns/name/{fqn}", params={"entityType": "table"}, json={"description": dp.description()}
                )
            else:
                response = update_column(client, fqn, dp)
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
