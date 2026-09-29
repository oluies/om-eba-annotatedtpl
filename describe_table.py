"""Write PAY 4.2 descriptions onto a table's columns, addressed by name.

Do not patch `/columns/N/description`. JSON Patch addresses arrays positionally, and the
array an agent reads back from the MCP `get_entity_details` tool is not the stored one -
it is paginated and trimmed for context. Index 17 in that response is not index 17 in the
entity, so a correct description lands silently on the wrong column.

OpenMetadata has a name-keyed path instead:

    GET /v1/tables/name/{fqn}/export           text/plain CSV of the current columns
    PUT /v1/tables/name/{fqn}/import?dryRun=   the same CSV back, by column.name

Header, from json/data/table/tableCsvDocumentation.json in the server source:

    column.name*, column.displayName, column.description, column.dataTypeDisplay,
    column.dataType*, column.arrayDataType, column.dataLength, column.tags,
    column.glossaryTerms

This reads the export, fills description and glossaryTerms for every column that matches
a datapoint in 05-datapoints.csv, leaves everything else exactly as it came back, and
writes it home.

Usage:

    export OM_HOST=https://host/api OM_JWT_TOKEN=...
    uv run describe_table.py SQLSASTest.FIDW_BI.dbo.Y_01_01
    uv run describe_table.py SQLSASTest.FIDW_BI.dbo.Y_01_01 --variant 0010 --commit
"""

import argparse
import csv
import io
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


def fill(csv_text: str, by_column: dict[str, list[Datapoint]], variant: str | None) -> tuple[str, list[str], list[str]]:
    """Fill description and glossaryTerms on datapoint columns, leave the rest untouched."""
    reader = csv.DictReader(io.StringIO(csv_text))
    fields = list(reader.fieldnames or [])
    if "column.name" not in fields:
        raise SystemExit(f"  Unexpected export header: {fields}")

    written: list[str] = []
    skipped: list[str] = []
    rows = []
    for row in reader:
        # The export gives the column's FQN; the framework code is its last segment.
        name = (row.get("column.name") or "").split(".")[-1]
        candidates = by_column.get(name)
        if not DATAPOINT_COLUMN.match(name) or not candidates:
            rows.append(row)
            continue

        dp = pick(candidates, variant)
        if dp is None:
            skipped.append(f"{name} ({len(candidates)} variants, none chosen)")
            rows.append(row)
            continue

        row["column.description"] = dp.description()
        if "column.glossaryTerms" in fields:
            row["column.glossaryTerms"] = ";".join(dp.glossary_terms())
        written.append(name)
        rows.append(row)

    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue(), written, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fqn", help="table FQN, e.g. SQLSASTest.FIDW_BI.dbo.Y_01_01")
    parser.add_argument("--variant", help="which variant this table holds, e.g. 0010")
    parser.add_argument("--commit", action="store_true", help="write for real; dry run only without it")
    args = parser.parse_args()

    settings = Settings()  # type: ignore[call-arg]
    with httpx.Client(
        base_url=settings.host.rstrip("/"),
        headers={"Authorization": f"Bearer {settings.jwt_token}"},
        verify=settings.ca_bundle or True,
        timeout=120.0,
    ) as client:
        export = client.get(f"/v1/tables/name/{args.fqn}/export")
        if export.status_code >= 400:
            raise SystemExit(f"  Export failed: {export.status_code}\n  {export.text[:500]}")

        filled, written, skipped = fill(export.text, load_datapoints(), args.variant)
        print(f"{args.fqn}: {len(written)} datapoint column(s) described")
        for name in skipped:
            print(f"  skipped {name} — pass --variant to choose")
        if not written:
            raise SystemExit("  Nothing to write.")

        for dry_run in (True, False) if args.commit else (True,):
            response = client.put(
                f"/v1/tables/name/{args.fqn}/import",
                params={"dryRun": str(dry_run).lower()},
                content=filled,
                headers={"Content-Type": "text/plain"},
            )
            if response.status_code >= 400:
                raise SystemExit(f"  Import failed: {response.status_code}\n  {response.text[:500]}")
            result = response.json()
            label = "dry run" if dry_run else "committed"
            print(
                f"  {label}: status={result.get('status')} "
                f"processed={result.get('numberOfRowsProcessed')} "
                f"passed={result.get('numberOfRowsPassed')} failed={result.get('numberOfRowsFailed')}"
            )
            if result.get("numberOfRowsFailed"):
                raise SystemExit(f"  Rejected rows:\n{(result.get('importResultsCsv') or '')[:1500]}")

        if not args.commit:
            print("\n  Nothing written. Re-run with --commit once the dry run looks right.")


if __name__ == "__main__":
    main()
