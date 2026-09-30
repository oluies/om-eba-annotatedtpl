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
import re
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

# dpm_cell_code is the coordinate including the sheet, so it differs per variant and
# belongs on the variant rather than in what is common to all six.
VARIES_BY_VARIANT = (*VARIES_BY_VARIANT, "dpm_cell_code")


class Resolved(BaseModel):
    """What a lookup answers with. Frozen: built once from the query, then only read."""

    model_config = ConfigDict(frozen=True)

    found: bool
    column_name: str
    message: str = ""
    common: dict[str, Any] = {}
    variant: dict[str, Any] = {}
    candidates: list[dict[str, Any]] = []


# Columns the store must have for a lookup to answer. The file is derived and gitignored,
# so a pull brings new code and a new CSV while leaving the old database in place - and a
# field added since it was built surfaces as a bare KeyError from a dict comprehension,
# which says nothing about what to do.
REQUIRED_COLUMNS = frozenset(CONSTANT_ACROSS_VARIANTS) | frozenset(VARIES_BY_VARIANT)
_CHECKED: set[Path] = set()


def check_store(db: Path) -> None:
    """Fail with what to run, once per file, rather than deep inside a comprehension."""
    if db in _CHECKED:
        return
    with duckdb.connect(str(db), read_only=True) as con:
        present = {row[0] for row in con.execute("DESCRIBE datapoints").fetchall()}
    missing = sorted(REQUIRED_COLUMNS - present)
    if missing:
        raise SystemExit(
            f"{db.name} is out of date: it has no {', '.join(missing)}.\n"
            "It is derived and not in git, so a pull leaves the old one behind.\n"
            "  uv run source/build_duckdb.py"
        )
    _CHECKED.add(db)


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

    check_store(DB)

    # config= rather than `SET temp_directory`, which also works on a read-only connection
    # but is global to the database instance: a SET here changes the setting for every
    # other connection in the process, including ones opened later. Verified. In a
    # long-running server that is someone else's bug, so keep it scoped to this connect.
    return duckdb.connect(str(DB), read_only=True, config=config)


def _rows(cursor: duckdb.DuckDBPyConnection, sql: str, *params: Any) -> list[dict[str, Any]]:
    result = cursor.execute(sql, list(params))
    names = [d[0] for d in result.description]
    return [dict(zip(names, row, strict=True)) for row in result.fetchall()]


# A column name splits the same way in both frameworks, but the row group is wider for
# DORA: an open row is written as a record ordinal such as r999, which is three digits,
# where a PAY row code is always four.
COLUMN_NAME = re.compile(
    r"^(?P<prefix>[A-Za-z]{1,})(?P<major>[0-9]{2})(?P<minor>[0-9]{2})_r(?P<row>[0-9]{1,})_c(?P<col>[0-9]{4})$"
)


def split_column_name(column_name: str) -> dict[str, str] | None:
    """Prefix, template major and minor, row and column, or None if it is not one."""
    match = COLUMN_NAME.match(column_name)
    if match is None:
        return None
    parts = match.groupdict()
    return parts | {
        "template": f"{parts['prefix']}_{parts['major']}.{parts['minor']}",
        "table": f"{parts['prefix']}_{parts['major']}_{parts['minor']}",
    }


# How to settle the variant without warehouse access, which the agent calling this does
# not have: this tool reads a local DuckDB file and knows nothing about the database the
# table lives in. What it does have is get_entity_details on the table.
#
# The first thing to look for is an open axis. The DPM's sheet axis can become one table
# per variant, or one table holding all of them with a context column saying which row is
# which - `Open_Axis_1`, whose values are the variant labels. Seen in the wild, so the
# column count alone does not settle it: a table with one variant's worth of datapoint
# columns may still carry all six, as rows.
VARIANT_HINT = (
    "The variant belongs to the row or the table, never the column, and this tool cannot "
    "see your warehouse. From get_entity_details on {table}, look for a context column "
    "named Open_Axis_1 or similar. If it is there the table holds every variant as rows, "
    "that column says which, and a column description must not name a datapoint id or a "
    "unit - both depend on the row. If there is no open axis the table holds a single "
    "variant, and only the pipeline that loads it knows which, so ask a person. Either "
    "way, until you know, describe only what is common to all {n}: the row, the column, "
    "the dimension members and the template."
)


def warehouse_context(dpm_cell_code: str) -> dict[str, Any]:
    """What the warehouse's own form metadata says about this cell, when reachable.

    Optional and best-effort: without a BA_ connection, or if the query fails, the pack's
    own answer stands on its own. A lookup must not become unusable because a database is
    down.
    """
    try:
        import ba_form_cell  # noqa: PLC0415 - optional dependency, imported where used

        if not ba_form_cell.enabled():
            # Say so rather than returning nothing: silence reads the same as a miss.
            return {"warehouse": "not consulted - BA_SERVER is not set"}
        return ba_form_cell.describe(ba_form_cell.fetch(dpm_cell_code))
    except Exception as exc:  # noqa: BLE001 - enrichment must never fail the lookup
        return {"warehouse_lookup_failed": f"{type(exc).__name__}: {exc}"}


def lookup_dora(column_name: str, parts: dict[str, str]) -> dict[str, Any]:
    """Resolve a DORA column, where the row is a record ordinal and carries no meaning.

    The register has open rows - one per entity, contract or provider - which the DPM
    writes as `r*`. Template and column identify the datapoint on their own: 85 cells,
    85 ids, 85 distinct template-and-column pairs.

    Every DORA template has exactly one row, including `B_99.01`, whose row code is a
    fixed `0040` rather than `r*`; its 19 datapoints differ by column like everywhere
    else. So the row is never needed, and matching on it is a belt-and-braces check
    rather than part of the resolution.
    """
    with _connect() as con:
        rows = _rows(
            con,
            "SELECT * FROM dora WHERE template = ? AND column_code = ?",
            parts["template"],
            parts["col"],
        )
    if not rows:
        return Resolved(
            found=False,
            column_name=column_name,
            message=f"No DORA datapoint for template {parts['template']} column {parts['col']}.",
        ).model_dump()

    # Fixed-row templates need the row too; open-row ones must ignore what was given.
    fixed = [r for r in rows if r["row_kind"] == "fixed"]
    chosen = next((r for r in fixed if r["row_code"] == parts["row"]), rows[0]) if fixed else rows[0]

    note = (
        "Rows are open: one per record. The row number in the column name is an ordinal, "
        "not a framework code, and does not narrow the datapoint."
        if chosen["row_kind"] == "open"
        else "This template has fixed rows, so the row code is a framework code."
    )

    # The DPM writes an open row as r*, which is what a warehouse's form metadata keys on
    # - not the ordinal the column name carries.
    dpm_cell_code = (
        "{"
        + ", ".join([chosen["template"].replace("_", " "), f"r{chosen['row_code']}", f"c{chosen['column_code']}"])
        + "}"
    )

    return Resolved(
        found=True,
        column_name=column_name,
        message=f"DORA register of information. {note}",
        common={
            "framework": "DORA",
            "table_name": chosen["table_name"],
            "template": chosen["template"],
            "template_name": chosen["template_name"],
            "column_code": chosen["column_code"],
            "column_label": chosen["column_label"],
            "row_kind": chosen["row_kind"],
            "row_code": chosen["row_code"],
            "dpm_cell_code": dpm_cell_code,
        }
        | warehouse_context(dpm_cell_code),
        variant={"datapoint_id": chosen["datapoint_id"], "sign": chosen["sign"]},
    ).model_dump()


def lookup_datapoint(column_name: str, variant: str | None = None) -> dict[str, Any]:
    """Resolve a warehouse column name to its datapoint, in either framework.

    Which rule applies is decided here rather than by the caller: PAY needs a row and a
    variant, DORA needs neither. Asking an agent to pick the rule is asking it to get it
    wrong on the one column where the frameworks disagree.

    For PAY, a column name carries no variant, so a `.01` template gives six candidates.
    Without `variant` this returns what they share and lists the six rather than picking
    one: choosing arbitrarily would invent five sixths of an answer.
    """
    parts = split_column_name(column_name)

    with _connect() as con:
        rows = _rows(con, "SELECT * FROM datapoints WHERE column_name = ? ORDER BY variant", column_name)

    if not rows and parts is not None:
        dora = lookup_dora(column_name, parts)
        if dora["found"]:
            return dora

    if not rows:
        return Resolved(
            found=False,
            column_name=column_name,
            message=(
                "No datapoint has this column name in PAY 4.2 or DORA. If it does not match "
                "^[A-Za-z]{1,}[0-9]{2}[0-9]{2}_r[0-9]{1,}_c[0-9]{4}$ it is a warehouse context "
                "column with no framework meaning, and should not be described from a framework."
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
            common=common | warehouse_context(chosen["dpm_cell_code"]),
            variant={field: chosen[field] for field in VARIES_BY_VARIANT},
        ).model_dump()

    if len(rows) == 1:
        return Resolved(
            found=True,
            column_name=column_name,
            common=common | warehouse_context(rows[0]["dpm_cell_code"]),
            variant={field: rows[0][field] for field in VARIES_BY_VARIANT},
        ).model_dump()

    # Spell the variants out rather than leaving the caller to characterise them from
    # the candidate list: an agent handed the list still paraphrased it from memory and
    # said 0010 meant "Payments in EUR" - it is metric crossed with geography, and
    # currency does not come into it.
    spelled = "; ".join(f"{r['variant']} = {r['metric']}, {r['geography']}" for r in rows)
    return Resolved(
        found=True,
        column_name=column_name,
        message=(
            f"{len(rows)} variants share this column name, one per metric and geography: {spelled}. "
            "The fields under 'common' hold for all of them; datapoint id, unit, metric and "
            "geography do not. Without a variant, state neither a datapoint id nor a unit - the "
            "row, the column, the dimension members and the template are safe to describe. "
            "Do not characterise the variants from memory; use the wording above."
        ),
        common=common
        | {
            "determining_the_variant": VARIANT_HINT.format(table=common["table_name"], n=len(rows)),
            "warehouse": (
                "not consulted - no single cell to look up until the variant is known. "
                "Call again with one, and the warehouse's own datapoint key comes with it."
            ),
        },
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


LOOKUP_DATAPOINT_TOOL_NAME = "lookup_datapoint"

# `strict` requires every property to appear in `required`, so an optional argument is
# expressed as a nullable type rather than an absent key. `variant` is therefore always
# sent, as null when the table does not establish one.
LOOKUP_DATAPOINT_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DATAPOINT_TOOL_NAME,
        "description": (
            "Resolve a warehouse column name from an EBA reporting framework to the datapoint it "
            "reports. Covers PAY 4.2 (columns like Y0101_r0010_c0010) and DORA (B0101_r999_c0020), "
            "and decides which framework and which resolution rule applies on its own - the caller "
            "does not choose. Returns the template, the row and column with their labels, the "
            "dimension members and the datapoint id. Call this whenever a column matching "
            "^[A-Za-z]{1,}[0-9]{4}_r[0-9]{1,}_c[0-9]{4}$ has to be described, in preference to "
            "reading a template page and locating the row by eye: landing one line off yields a "
            "correct-looking description of the wrong datapoint and nothing detects it. Do not call "
            "it for a column that does not match that shape - warehouse context columns such as "
            "Period_SK or Taxonomy_Name carry no framework meaning and the answer is a refusal. "
            "Only PAY 4.2 and DORA are loaded: another EBA framework of the same shape resolves to "
            "nothing rather than to a guess."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "column_name": {
                    "type": "string",
                    "description": "Warehouse column name, e.g. Y0101_r0010_c0010 or B0101_r999_c0020.",
                },
                "variant": {
                    "type": ["string", "null"],
                    "description": (
                        "PAY 4.2 only: the sheet variant, 0010 to 0060, when the table establishes "
                        "which metric and geography it holds. Pass null when that is not known, and "
                        "always for DORA, which has no variants. With null the answer gives the "
                        "fields common to all six variants and lists the six; it does not pick one, "
                        "and neither should the caller."
                    ),
                },
            },
            "required": ["column_name", "variant"],
            "additionalProperties": False,
        },
    },
}

# The earlier name, kept so an existing import does not break.
TOOL_DEFINITION = LOOKUP_DATAPOINT_TOOL_DEFINITION


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args:
        raise SystemExit("usage: pay42_lookup.py <column_name> [variant]")
    print(json.dumps(lookup_datapoint(args[0], args[1] if len(args) > 1 else None), ensure_ascii=False, indent=2))
