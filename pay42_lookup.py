"""Deterministic datapoint lookup, for use as an agent tool.

An agent reading a template page has to find the right line in a grid of up to eighty
rows, and when it lands one line off it produces correct prose about the wrong datapoint
with nothing to catch it. That happened: `Y0101_r0010_c0010` was described as datapoint
437824, which is row 0030.

This removes the counting. One call in, the resolved datapoint out.

The store is DuckDB over the generated CSVs, so the same file also answers ad-hoc SQL:

    duckdb pay42.duckdb -c "SELECT * FROM datapoints WHERE row_label ILIKE '%fraud%'"

Build it with `uv run source/build_duckdb.py`; it is derived, so it is gitignored.
"""

import json
from pathlib import Path
from typing import Any

import duckdb
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

PACK = Path(__file__).parent


class DuckDBSettings(BaseSettings):
    """Where the store and DuckDB's scratch files live.

    DuckDB reads no environment variables of its own - every directory is a `SET` or a
    connection config - so these are ours, read once at import.

    Left alone, DuckDB puts scratch files next to the database, at `<db>.tmp` - so a
    read-only mount holding the store has nowhere to spill. (The documented `.tmp`
    relative to the working directory applies to in-memory databases, not this one.)
    Setting `PAY42_TEMP_DIR` moves them somewhere writable.
    """

    model_config = SettingsConfigDict(env_prefix="PAY42_", env_file=".env", extra="ignore")

    db: Path = PACK / "pay42.duckdb"
    temp_dir: Path | None = None
    extension_dir: Path | None = None
    memory_limit: str | None = None


SETTINGS = DuckDBSettings()
DB = SETTINGS.db

# Fields that are identical across every variant of one column name, measured across the
# 302 multi-variant columns rather than assumed. Everything else differs per variant, so
# with no variant chosen there is no datapoint id and no unit to report.
CONSTANT_ACROSS_VARIANTS = (
    "table_name",
    "column_name",
    "template",
    "template_name",
    "row_code",
    "row_label",
    "column_code",
    "column_label",
    "row_dimensions",
    "column_dimensions",
)
VARIES_BY_VARIANT = ("datapoint_id", "variant", "variant_label", "metric", "geography", "unit")


class Resolved(BaseModel):
    """What a lookup answers with. Frozen: built once from the query, then only read."""

    model_config = ConfigDict(frozen=True)

    found: bool
    column_name: str
    message: str = ""
    common: dict[str, Any] = {}
    variant: dict[str, Any] = {}
    candidates: list[dict[str, Any]] = []


def _connect() -> duckdb.DuckDBPyConnection:
    if not DB.exists():
        raise SystemExit(f"{DB} is missing. Build it with: uv run source/build_duckdb.py")

    config: dict[str, str] = {}
    if SETTINGS.temp_dir:
        SETTINGS.temp_dir.mkdir(parents=True, exist_ok=True)
        config["temp_directory"] = str(SETTINGS.temp_dir)
    if SETTINGS.extension_dir:
        config["extension_directory"] = str(SETTINGS.extension_dir)
    if SETTINGS.memory_limit:
        config["memory_limit"] = SETTINGS.memory_limit

    return duckdb.connect(str(DB), read_only=True, config=config)


def _rows(cursor: duckdb.DuckDBPyConnection, sql: str, *params: Any) -> list[dict[str, Any]]:
    result = cursor.execute(sql, list(params))
    names = [d[0] for d in result.description]
    return [dict(zip(names, row, strict=True)) for row in result.fetchall()]


def lookup_datapoint(column_name: str, variant: str | None = None) -> dict[str, Any]:
    """Resolve a warehouse column name to its datapoint.

    A column name carries no variant, so a `.01` template gives six candidates. Without
    `variant` this returns what they share and lists the six rather than picking one:
    choosing arbitrarily would invent five sixths of an answer.
    """
    with _connect() as con:
        rows = _rows(con, "SELECT * FROM datapoints WHERE column_name = ? ORDER BY variant", column_name)

    if not rows:
        return Resolved(
            found=False,
            column_name=column_name,
            message=(
                "No datapoint has this column name. If it does not match "
                "^[A-Za-z]{1,}[0-9]{2}[0-9]{2}_r[0-9]{4}_c[0-9]{4}$ it is a warehouse context "
                "column with no framework meaning, and should not be described from this framework."
            ),
        ).model_dump()

    common = {field: rows[0][field] for field in CONSTANT_ACROSS_VARIANTS}

    if variant:
        chosen = next((r for r in rows if r["variant"] == variant), None)
        if chosen is None:
            available = ", ".join(r["variant"] for r in rows)
            return Resolved(
                found=False,
                column_name=column_name,
                message=f"No variant {variant!r} for this column. Available: {available}.",
                common=common,
            ).model_dump()
        return Resolved(
            found=True,
            column_name=column_name,
            common=common,
            variant={field: chosen[field] for field in VARIES_BY_VARIANT},
        ).model_dump()

    if len(rows) == 1:
        return Resolved(
            found=True,
            column_name=column_name,
            common=common,
            variant={field: rows[0][field] for field in VARIES_BY_VARIANT},
        ).model_dump()

    return Resolved(
        found=True,
        column_name=column_name,
        message=(
            f"{len(rows)} variants share this column name. The fields under 'common' hold for all "
            "of them; datapoint id, unit, metric and geography do not. Establish the variant from "
            "the table, then call again with it. Without one, state neither a datapoint id nor a unit."
        ),
        common=common,
        candidates=[{field: r[field] for field in VARIES_BY_VARIANT} for r in rows],
    ).model_dump()


def lookup_by_datapoint_id(datapoint_id: str) -> dict[str, Any]:
    """Resolve a numeric datapoint id, which is unique on its own."""
    with _connect() as con:
        rows = _rows(con, "SELECT * FROM datapoints WHERE datapoint_id = ?", datapoint_id)
    if not rows:
        return {"found": False, "datapoint_id": datapoint_id, "message": "No such datapoint in PAY 4.2."}
    return {"found": True, **rows[0]}


def glossary_terms_for(column_name: str) -> list[str]:
    """Glossary term FQNs for a column's dimension members, in template order."""
    with _connect() as con:
        rows = _rows(con, "SELECT term_fqn FROM column_terms WHERE column_name = ? ORDER BY ordinal", column_name)
    return [r["term_fqn"] for r in rows]


# The tool definition to drop into the agent's TOOLS list.
TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "lookup_datapoint",
        "description": (
            "Resolve an EBA PAY 4.2 warehouse column name, e.g. Y0101_r0010_c0010, to its datapoint. "
            "Use this instead of reading a template page and counting rows: landing one line off "
            "produces a correct-looking description of the wrong datapoint. A column name carries no "
            "variant, so without one the answer gives the fields common to all six and lists them."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "column_name": {"type": "string", "description": "Warehouse column name, e.g. Y0101_r0010_c0010."},
                "variant": {
                    "type": "string",
                    "description": "Sheet variant, 0010 to 0060, if the table establishes one. Omit if unknown.",
                },
            },
            "required": ["column_name"],
        },
    },
}


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args:
        raise SystemExit("usage: pay42_lookup.py <column_name> [variant]")
    print(json.dumps(lookup_datapoint(args[0], args[1] if len(args) > 1 else None), ensure_ascii=False, indent=2))
