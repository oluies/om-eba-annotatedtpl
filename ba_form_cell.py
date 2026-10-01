"""The warehouse's own form metadata - the primary source for what a cell is.

`FIDW_BI.dbo.BA_Form_Cell` describes every cell of every form the warehouse holds. Two
keys matter:

    Row_Column_Code   the physical column in the loaded table, e.g. Y0101_r0010_c0010
    DPM_Cell_Code     the DPM coordinate including the sheet, {Y 01.01, r0010, c0010, s0010}

One physical column therefore maps to several cells when the template has an open sheet
axis, and `dbo.BA_Form_Axis` joined on `Cell_sk` says which value of that axis each cell
stands for. That is the fact the pack alone cannot supply: the column holds every variant
as rows, and only the warehouse knows which values are actually defined for it.

So the roles are:

    BA_Form_Cell    what the cell *is* - form, taxonomy version, row and column labels,
    + BA_Form_Axis  data type, datapoint key, and the open-axis values the column carries.
                    Authoritative, covers every form, and is current by construction.
    the pack        a semantic overlay - dimension members, glossary terms and EBA's
                    VariableVID - joined on DPM_Cell_Code, and only valid where the
                    taxonomy matches the release the pack was generated from.

Where the taxonomy does not match, the overlay is left off rather than asserted. The table
spans 33 taxonomy names from DPM_2.6 to DPM_4.2 (census taken 2026-10-01), and a cell code
can carry a different meaning in each, so an id borrowed across releases is simply wrong.

`Current_flg = 1` is the definition in force, which is what a description should be written
against unless someone asks otherwise.

Optional. Without `BA_` settings the pack's own data answers on its own, which is what an
agent with no database access gets. Connecting costs a round trip per call, so it is for
enrichment rather than for the hot path.
"""

from collections.abc import Iterable, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Connection to the warehouse. Unset means the enrichment is simply off."""

    model_config = SettingsConfigDict(env_prefix="BA_", env_file=".env", extra="ignore")

    server: str | None = None
    database: str = "FIDW_BI"
    table: str = "dbo.BA_Form_Cell"
    axis_table: str = "dbo.BA_Form_Axis"
    # Kerberos: no username or password, the ticket from kinit carries the identity.
    trusted_connection: bool = True
    username: str | None = None
    password: str | None = None
    driver: str = "ODBC Driver 18 for SQL Server"
    encrypt: bool = True
    trust_server_certificate: bool = False


SETTINGS = Settings()

# The EBA release the generated pack describes, spelled the way BA_Form_Cell spells it.
# A cell whose current definition sits under any other taxonomy still has warehouse facts,
# but the pack's dimension members, unit and EBA datapoint id are about a different
# release and must not be attached to it.
PACK_TAXONOMIES = ("DPM_4.2",)


class FormCell(BaseModel):
    """One cell of one form, with the open-axis values BA_Form_Axis gives it."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    dpm_cell_code: str
    cell_sk: int | None = None
    row_column_code: str | None = None
    datapoint_sk: int | None = None
    table_code: str | None = None
    table_label: str | None = None
    row_code: str | None = None
    row_label: str | None = None
    column_code: str | None = None
    column_label: str | None = None
    open_axis_label_1: str | None = None
    open_axis_cnt: int | None = None
    open_axis_values: tuple[str, ...] = ()
    data_type: str | None = None
    form_bk: str | None = None
    form_name: str | None = None
    taxonomy_name: str | None = None


def enabled() -> bool:
    return SETTINGS.server is not None


def connection_string() -> str:
    """ODBC string. Kerberos is Trusted_Connection with no credentials in it."""
    parts = [
        f"DRIVER={{{SETTINGS.driver}}}",
        f"SERVER={SETTINGS.server}",
        f"DATABASE={SETTINGS.database}",
        f"Encrypt={'yes' if SETTINGS.encrypt else 'no'}",
        f"TrustServerCertificate={'yes' if SETTINGS.trust_server_certificate else 'no'}",
    ]
    if SETTINGS.trusted_connection:
        parts.append("Trusted_Connection=yes")
    elif SETTINGS.username and SETTINGS.password:
        parts += [f"UID={SETTINGS.username}", f"PWD={SETTINGS.password}"]
    return ";".join(parts) + ";"


# One statement for both lookups: the only thing that changes is which key is matched.
# The join is LEFT so a cell with no open axis still comes back, with no values.
# Current_flg picks the definition in force; a description written against a superseded
# one is wrong in a way nothing in the catalogue would show.
QUERY = """
SELECT  fc.DPM_Cell_Code, fc.Cell_sk, fc.Row_Column_Code, fc.Datapoint_sk,
        fc.Table_Code, fc.Table_Label,
        fc.Row_Code, fc.Row_Label, fc.Column_Code, fc.Column_Label,
        fc.Open_Axis_Label_1, fc.Open_Axis_cnt, fc.Data_Type,
        fc.Form_BK, fc.Form_Name, fc.Taxonomy_Name,
        fa.Open_Axis_value_1
FROM    {table} fc
LEFT JOIN {axis_table} fa ON fa.Cell_sk = fc.Cell_sk
WHERE   fc.{key} = ?
  AND   fc.Current_flg = 1
"""

AXIS_VALUE_FIELD = "open_axis_value_1"


def fold_rows(names: Sequence[str], rows: Iterable[Sequence[Any]]) -> list[FormCell]:
    """Collapse the joined result into one FormCell per cell, values gathered.

    Pure, so the shape of the join can be tested without a database. Grouping on Cell_sk
    means the function is right whether the axis table holds one row per cell or many:
    either way a cell ends up with the distinct values defined for it, in table order.
    """
    cells: dict[Any, dict[str, Any]] = {}
    values: dict[Any, list[str]] = {}
    for row in rows:
        record = dict(zip(names, row, strict=True))
        value = record.pop(AXIS_VALUE_FIELD, None)
        key = record.get("cell_sk") or record["dpm_cell_code"]
        cells.setdefault(key, record)
        seen = values.setdefault(key, [])
        if value is not None and value not in seen:
            seen.append(value)
    return [FormCell.model_validate(record | {"open_axis_values": tuple(values[key])}) for key, record in cells.items()]


def _query(key: str, value: str, form_bk: str | None) -> list[FormCell]:
    """Run the one query against whichever key was given. The only I/O in this module."""
    if not enabled():
        return []

    import pyodbc  # noqa: PLC0415 - optional, and only where the connection is used

    sql = QUERY.format(table=SETTINGS.table, axis_table=SETTINGS.axis_table, key=key)
    params: list[Any] = [value]
    if form_bk:
        sql += "  AND   fc.Form_BK = ?\n"
        params.append(form_bk)

    with pyodbc.connect(connection_string()) as connection:
        cursor = connection.cursor()
        cursor.execute(sql, params)
        names = [c[0].lower() for c in cursor.description]
        return fold_rows(names, cursor.fetchall())


def fetch(dpm_cell_code: str, form_bk: str | None = None) -> list[FormCell]:
    """Current definitions of one DPM coordinate, optionally narrowed to one form.

    Returns every match rather than one: a cell code present under several forms is a
    fact about the warehouse, and picking silently would hide it.
    """
    return _query("DPM_Cell_Code", dpm_cell_code, form_bk)


def fetch_column(row_column_code: str, form_bk: str | None = None) -> list[FormCell]:
    """Every current cell a physical column carries - the variants it can hold.

    This is the question the pack cannot answer. A `.01` template gives six candidate
    variants and no way to tell which of them the column actually holds; here they come
    back enumerated, with the open-axis value that distinguishes each one.
    """
    return _query("Row_Column_Code", row_column_code, form_bk)


def pack_applies(cells: Sequence[FormCell]) -> bool:
    """Whether the pack's semantics may be attached to these cells.

    All of them, not any: a mixed result means the column spans releases, and attaching
    one release's ids to the whole of it would be worse than attaching none.
    """
    return bool(cells) and all(cell.taxonomy_name in PACK_TAXONOMIES for cell in cells)


def cell_facts(cell: FormCell) -> dict[str, Any]:
    """What the warehouse says this cell is, with the empty fields left out."""
    facts = {
        "dpm_cell_code": cell.dpm_cell_code,
        "taxonomy_name": cell.taxonomy_name,
        "form_bk": cell.form_bk,
        "form_name": cell.form_name,
        "table_code": cell.table_code,
        "table_label": cell.table_label,
        "row_code": cell.row_code,
        "row_label": cell.row_label,
        "column_code": cell.column_code,
        "column_label": cell.column_label,
        "data_type": cell.data_type,
        "datapoint_sk": cell.datapoint_sk,
        "open_axis_label": cell.open_axis_label_1,
        "open_axis_values": list(cell.open_axis_values),
    }
    return {key: value for key, value in facts.items() if value not in (None, [], "")}


def _overlay_note(cells: Sequence[FormCell]) -> str:
    """Say whether the pack's ids and dimension members belong on this answer."""
    if pack_applies(cells):
        return (
            f"The warehouse has this cell under {PACK_TAXONOMIES[0]}, the release the pack "
            "describes, so the pack's dimension members, unit and EBA datapoint id apply."
        )
    found = ", ".join(sorted({cell.taxonomy_name or "?" for cell in cells}))
    return (
        f"The warehouse has this cell under {found}, not {PACK_TAXONOMIES[0]}, which is the "
        "release the pack describes. Describe it from the warehouse fields above and leave "
        "the pack's datapoint id, unit and dimension members out - they belong to a "
        "different release and a cell code can mean something else in each."
    )


def describe(cells: list[FormCell]) -> dict[str, Any]:
    """Fold the matches into the cell facts a description should be written from.

    Three shapes, because they call for three different descriptions: nothing found, one
    cell, or a column that carries several - which is the ordinary case for a template
    with an open sheet axis, and the one the pack has to defer to.
    """
    if not cells:
        return {"warehouse": "no row in BA_Form_Cell for this key with Current_flg = 1"}

    where = f"BA_Form_Cell joined to BA_Form_Axis on {SETTINGS.server}"
    if len(cells) == 1:
        return {"warehouse": where, **cell_facts(cells[0]), "pack_overlay": _overlay_note(cells)}

    forms = {(cell.form_bk, cell.form_name, cell.taxonomy_name) for cell in cells}
    values = [value for cell in cells for value in cell.open_axis_values]
    distinct = list(dict.fromkeys(values))
    axis_label = next((cell.open_axis_label_1 for cell in cells if cell.open_axis_label_1), None)

    if len(forms) == 1:
        # One form, several cells: the open axis. This is the answer to "which variant",
        # and it is the warehouse's to give - the column holds all of these, as rows.
        form_bk, form_name, taxonomy = next(iter(forms))
        return {
            "warehouse": where,
            "taxonomy_name": taxonomy,
            "form_bk": form_bk,
            "form_name": form_name,
            "open_axis_label": axis_label,
            "open_axis_values": distinct,
            "message": (
                f"This column carries {len(cells)} cells of one form, separated by "
                f"{axis_label or 'the open axis'}. Every value listed above appears as rows in "
                "the same column, so a column description must cover all of them and must not "
                "name a datapoint id or a unit - both belong to the row."
            ),
            "cells": [cell_facts(cell) for cell in cells],
            "pack_overlay": _overlay_note(cells),
        }

    return {
        "warehouse": where,
        "ambiguous": (
            f"{len(cells)} current cells define this key across {len(forms)} forms: "
            + ", ".join(sorted(f"{bk} ({tax})" for bk, _, tax in forms))
            + ". The column means different things in each, so establish which form the table "
            "belongs to from its Form_BK before describing it."
        ),
        "open_axis_values": distinct,
        "cells": [cell_facts(cell) for cell in cells],
        "pack_overlay": _overlay_note(cells),
    }


def check_connection() -> dict[str, Any]:
    """Prove the connection works, for when a lookup says nothing about the warehouse.

    Answers the question "did it actually reach SQL Server", which an empty result cannot,
    and checks the axis table too - the join is the part that has not been run from here.
    """
    if not enabled():
        return {"connected": False, "reason": "BA_SERVER is not set, so the warehouse is not consulted at all"}
    try:
        import pyodbc  # noqa: PLC0415

        with pyodbc.connect(connection_string()) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT SUSER_SNAME()")
            who = cursor.fetchone()[0]
            cursor.execute(f"SELECT COUNT(*) FROM {SETTINGS.table} WHERE Current_flg = 1")  # noqa: S608
            current = cursor.fetchone()[0]
            cursor.execute(f"SELECT COUNT(*) FROM {SETTINGS.axis_table}")  # noqa: S608
            axis = cursor.fetchone()[0]
            cursor.execute(  # noqa: S608
                f"SELECT TOP 5 Taxonomy_Name, COUNT(*) AS cells FROM {SETTINGS.table} "
                "WHERE Current_flg = 1 GROUP BY Taxonomy_Name ORDER BY COUNT(*) DESC"
            )
            taxonomies = {name: count for name, count in cursor.fetchall()}
        return {
            "connected": True,
            "server": SETTINGS.server,
            "table": SETTINGS.table,
            "axis_table": SETTINGS.axis_table,
            "authenticated_as": who,
            "current_cells": current,
            "axis_rows": axis,
            "largest_current_taxonomies": taxonomies,
            "pack_taxonomies": list(PACK_TAXONOMIES),
        }
    except Exception as exc:  # noqa: BLE001 - the point is to report the failure
        return {"connected": False, "reason": f"{type(exc).__name__}: {exc}"}


if __name__ == "__main__":
    import json
    import sys

    # With an argument, look that column or cell code up; without, just prove the
    # connection. Both print JSON, so the output can be piped into anything.
    if len(sys.argv) > 1:
        key = sys.argv[1]
        found = fetch(key) if key.startswith("{") else fetch_column(key)
        print(json.dumps(describe(found), ensure_ascii=False, indent=2, default=str))
    else:
        print(json.dumps(check_connection(), ensure_ascii=False, indent=2, default=str))
