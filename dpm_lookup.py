"""Look things up in the EBA DPM 2.0 database itself, for frameworks the pack does not cover.

The pack covers PAY 4.2 and DORA 1.1.0 because those are the templates it was built from.
A warehouse holds more than that - BA_Form_Cell alone carries 33 taxonomies - and for a
COREP or FINREP column the pack's answer is, correctly, that it knows nothing. This reads
the model directly instead, so the agent has something to say about any template in it.

It is optional. The database is 139 MB and gitignored, so a checkout does not have one
until `uv run source/fetch_dpm2.py` builds it; without it every function here answers that
it is not available rather than failing. Nothing else in the pack depends on it.

    uv run dpm_lookup.py Y_01_01                      # a template
    uv run dpm_lookup.py Y_01_01 0010 0010 0010       # one cell
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import duckdb

PACK = Path(__file__).parent
# DPM2_DIR has to be honoured wherever DPM2_DB is, because fetch_dpm2.py puts the database
# inside it: resolving only DPM2_DB leaves this looking in the default directory for a file
# that was downloaded somewhere else, and reporting it as never downloaded.
DIR = Path(os.environ.get("DPM2_DIR") or PACK / "source" / "dpm2")
DB = Path(os.environ.get("DPM2_DB") or DIR / "dpm2.duckdb")

# 143 of the 1052 templates in release 4.2.1 have no headers and no cells recorded. That
# is a fact about the model, not about the report, and an empty answer would read as the
# template having no columns.
EMPTY_TEMPLATE = (
    "The model records no rows, columns or cells for this template in its current version - "
    "it is in the dictionary by code only. Do not conclude from this that the report has no "
    "columns. "
)

BUILD_IT = (
    "The DPM 2.0 database is not in this checkout. It is 139 MB and derived, so it is not "
    "in git: build it with `uv run source/fetch_dpm2.py`. Until then only PAY 4.2 and DORA "
    "are answerable, through lookup_datapoint."
)

# A template code is written four ways between the warehouse, the annotated layout and the
# model - Y_01_01, Y 01.01, Y_01.01, Y0101 - and they all mean the same template.
TEMPLATE = re.compile(r"^(?P<prefix>[A-Za-z]+)[ _]?(?P<major>[0-9]{2})[._]?(?P<minor>[0-9]{2})$")


class DpmError(Exception):
    """The DPM database is absent or does not hold what was asked for.

    An exception rather than SystemExit for the same reason the pack's own lookup uses
    one: an agent calls this in-process, and SystemExit walks past `except Exception`.
    """


def available() -> bool:
    return DB.exists()


def normalise(table: str) -> str | None:
    """Any of the four spellings to the model's own: Y_01.01. None if it is not one."""
    match = TEMPLATE.match(table.strip())
    return f"{match['prefix'].upper()}_{match['major']}.{match['minor']}" if match else None


def _connect() -> duckdb.DuckDBPyConnection:
    if not available():
        raise DpmError(BUILD_IT)
    return duckdb.connect(str(DB), read_only=True)


def _rows(con: duckdb.DuckDBPyConnection, sql: str, *params: Any) -> list[dict[str, Any]]:
    result = con.execute(sql, list(params))
    names = [d[0] for d in result.description]
    return [dict(zip(names, row, strict=True)) for row in result.fetchall()]


# The newest version of a template, with the open-axis flags that say what its rows,
# columns and sheets mean. Newest by start release: a template that has not changed since
# 3.4 has one version, one that changed in 4.2 has several and only the last is current.
TABLE_SQL = """
SELECT   tv.TableVID, tv.TableID, tv.Code, tv.Name,
         t.HasOpenRows <> 0 AS open_rows, t.HasOpenColumns <> 0 AS open_columns,
         t.HasOpenSheets <> 0 AS open_sheets
FROM     TableVersion tv
JOIN     "Table" t ON t.TableID = tv.TableID
WHERE    tv.Code = ?
ORDER BY tv.StartReleaseID DESC, tv.TableVID DESC
LIMIT    1
"""

MODULES_SQL = """
SELECT DISTINCT f.Code AS framework, f.Name AS framework_name, mv.Code AS module,
       mv.VersionNumber AS version, mv.FromReferenceDate AS from_reference_date,
       mv.ToReferenceDate AS to_reference_date
FROM   ModuleVersionComposition mvc
JOIN   ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
JOIN   Module m ON m.ModuleID = mv.ModuleID
JOIN   Framework f ON f.FrameworkID = m.FrameworkID
WHERE  mvc.TableID = ?
ORDER  BY mv.Code, mv.VersionNumber
"""

# Direction X is the column axis, Y the row axis and Z the sheet axis. ParentHeaderID is
# what makes an "Of which" row a child of the row it qualifies - the nesting the annotated
# layout only shows by indentation.
HEADERS_SQL = """
SELECT   h.Direction AS direction, hv.Code AS code, hv.Label AS label,
         parent.Code AS parent_code, tvh.IsAbstract <> 0 AS is_abstract
FROM     TableVersionHeader tvh
JOIN     HeaderVersion hv ON hv.HeaderVID = tvh.HeaderVID
JOIN     Header h ON h.HeaderID = tvh.HeaderID
LEFT JOIN TableVersionHeader ptvh ON ptvh.TableVID = tvh.TableVID AND ptvh.HeaderID = tvh.ParentHeaderID
LEFT JOIN HeaderVersion parent ON parent.HeaderVID = ptvh.HeaderVID
WHERE    tvh.TableVID = ?
ORDER BY h.Direction, tvh."Order"
"""

CELL_SQL = """
SELECT CellCode, VariableVID, IsExcluded <> 0 AS is_excluded, Sign AS sign
FROM   TableVersionCell
WHERE  TableVID = ? AND CellCode = ?
"""

DIMENSIONS_SQL = """
SELECT DISTINCT dimension.Name AS dimension, member.Name AS member,
       nullif(member.Description, '') AS definition
FROM   VariableVersion vv
JOIN   ContextComposition cc ON cc.ContextID = vv.ContextID
JOIN   Item member ON member.ItemID = cc.ItemID
JOIN   Item dimension ON dimension.ItemID = cc.PropertyID
WHERE  vv.VariableVID = ?
ORDER  BY 1, 2
"""

DATATYPE_SQL = """
SELECT DISTINCT dt.Name AS data_type, lower(p.PeriodType) AS period_type
FROM   VariableVersion vv
JOIN   Property p ON p.PropertyID = vv.PropertyID
LEFT JOIN DataType dt ON dt.DataTypeID = p.DataTypeID
WHERE  vv.VariableVID = ?
"""

# A rule code is not one rule: the same code is re-issued per module version, and the
# expression and the severity both change between them - v09247_s is a warning in PSD_FRP
# 1.1.0 and an error in 1.2.0. So the module version is part of the answer, not a filter
# applied behind the caller's back.
RULES_SQL = """
SELECT   o.Code AS rule_code, os.Severity AS severity, ov.Expression AS expression,
         mv.Code || ' ' || mv.VersionNumber AS module
FROM     OperandReferenceLocation l
JOIN     OperandReference r ON r.OperandReferenceID = l.OperandReferenceID
JOIN     OperationNode n ON n.NodeID = r.NodeID
JOIN     OperationVersion ov ON ov.OperationVID = n.OperationVID
JOIN     Operation o ON o.OperationID = ov.OperationID
JOIN     OperationScope os ON os.OperationVID = ov.OperationVID
JOIN     OperationScopeComposition osc ON osc.OperationScopeID = os.OperationScopeID
JOIN     ModuleVersion mv ON mv.ModuleVID = osc.ModuleVID
WHERE    l."Table" = ? AND coalesce(l."Row", '') = ? AND coalesce(l."Column", '') = ?
     AND coalesce(l.Sheet, '') = ?
GROUP BY rule_code, severity, expression, module
ORDER BY rule_code, module
"""


def fold_rules(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One entry per rule, severity and expression, with the module versions it holds in.

    Pure. Two entries for the same code is not a duplicate: it means the rule was changed
    between module versions, and which one applies depends on what the table reports.
    """
    folded: dict[tuple[str, str, str], list[str]] = {}
    for row in rows:
        folded.setdefault((row["rule_code"], row["severity"], row["expression"]), []).append(row["module"])
    return [
        {"rule_code": code, "severity": severity, "expression": expression, "modules": modules}
        for (code, severity, expression), modules in folded.items()
    ]


def cell_code(table: str, row: str, column: str, sheet: str = "") -> str:
    """The model's own spelling of a coordinate: {Y_01.01, r0010, c0010, s0010}."""
    parts = [table, f"r{row}", f"c{column}"] + ([f"s{sheet}"] if sheet else [])
    return "{" + ", ".join(parts) + "}"


def _table_version(con: duckdb.DuckDBPyConnection, table: str) -> dict[str, Any]:
    code = normalise(table)
    if code is None:
        raise DpmError(f"{table!r} is not a template code. They look like Y_01_01, C_01.00 or F_32.04.")
    found = _rows(con, TABLE_SQL, code)
    if not found:
        raise DpmError(f"No template {code} in the DPM 2.0 database.")
    return found[0]


def lookup_dpm_table(table: str) -> dict[str, Any]:
    """A template from any framework in the model: what it is and how it is laid out."""
    if not available():
        return {"found": False, "table": table, "message": BUILD_IT}
    try:
        with _connect() as con:
            version = _table_version(con, table)
            vid = version["TableVID"]
            headers = _rows(con, HEADERS_SQL, vid)
            modules = _rows(con, MODULES_SQL, version["TableID"])
    except DpmError as exc:
        return {"found": False, "table": table, "message": str(exc)}

    axis = {
        direction: [{k: v for k, v in h.items() if k != "direction"} for h in headers if h["direction"] == direction]
        for direction in ("Y", "X", "Z")
    }
    open_axes = [
        name
        for name, flag in (("rows", "open_rows"), ("columns", "open_columns"), ("sheets", "open_sheets"))
        if version[flag]
    ]
    return {
        "found": True,
        "table": version["Code"],
        "name": version["Name"],
        "modules": modules,
        "open_axes": open_axes,
        "rows": axis["Y"],
        "columns": axis["X"],
        "sheets": axis["Z"],
        "message": ("" if headers else EMPTY_TEMPLATE)
        + (
            "parent_code is what an 'Of which' row is a breakdown of. An open axis has no fixed "
            "codes at all: its values come from the report rather than the framework, and a cell on "
            "it is written r*. A sheet is the third axis, and a template that has one needs it to "
            "identify a cell - PAY's six metric-and-geography variants are sheets, and they are "
            "fixed codes, not an open axis."
        ),
    }


def lookup_dpm_cell(table: str, row: str, column: str, sheet: str | None = None) -> dict[str, Any]:
    """One cell of any template: its dimension members, data type and validation rules.

    The sheet is the third axis, which not every template has - PAY's six metric-and-geography
    variants are sheets. Pass null where the template has none.
    """
    if not available():
        return {"found": False, "table": table, "message": BUILD_IT}
    try:
        with _connect() as con:
            version = _table_version(con, table)
            code = cell_code(version["Code"], row, column, sheet or "")
            cells = _rows(con, CELL_SQL, version["TableVID"], code)
            if not cells:
                codes = [h["code"] for h in _rows(con, HEADERS_SQL, version["TableVID"]) if h["direction"] == "Z"]
                raise DpmError(
                    f"No cell {code} in {version['Code']}."
                    + (f" This template has a sheet axis: {', '.join(codes)}." if codes and not sheet else "")
                )
            cell = cells[0]
            dimensions = _rows(con, DIMENSIONS_SQL, cell["VariableVID"])
            types = _rows(con, DATATYPE_SQL, cell["VariableVID"])
            rules = fold_rules(_rows(con, RULES_SQL, version["Code"], row, column, sheet or ""))
    except DpmError as exc:
        return {"found": False, "table": table, "message": str(exc)}

    return {
        "found": True,
        "cell_code": cell["CellCode"],
        "table": version["Code"],
        "table_name": version["Name"],
        "is_excluded": cell["is_excluded"],
        "sign": cell["sign"],
        "data_type": types[0]["data_type"] if types else None,
        "period_type": types[0]["period_type"] if types else None,
        "dimensions": dimensions,
        "validation_rules": rules,
        "message": (
            "An excluded cell is a greyed-out box in the template: in the model but not reportable. "
            "A member definition is empty wherever the EBA has not published one, which is most of "
            "them - say nothing rather than inventing one. Two entries under validation_rules with "
            "the same rule_code are not a duplicate: the rule differs between the module versions "
            "listed on each, in expression or in severity."
        ),
    }


LOOKUP_DPM_TABLE_TOOL_NAME = "lookup_dpm_table"
LOOKUP_DPM_CELL_TOOL_NAME = "lookup_dpm_cell"

LOOKUP_DPM_TABLE_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_TABLE_TOOL_NAME,
        "description": (
            "Look a reporting template up in the EBA DPM 2.0 database - any framework, not only the "
            "two this pack was built from: COREP, FINREP, resolution, ESG, MiCA and the rest. Returns "
            "the template's name, which module versions it belongs to, which of its axes are open, and "
            "every row and column with its code, label and parent. Use it for a warehouse table whose "
            "name looks like a template code that lookup_datapoint does not recognise. Prefer "
            "lookup_datapoint for PAY 4.2 and DORA: it knows the warehouse column naming and this does "
            "not. Answers that it is unavailable when the DPM database has not been downloaded."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "table": {
                    "type": "string",
                    "description": "Template code in any spelling: Y_01_01, Y 01.01, C_01.00, F_32.04.",
                }
            },
            "required": ["table"],
            "additionalProperties": False,
        },
    },
}

LOOKUP_DPM_CELL_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_CELL_TOOL_NAME,
        "description": (
            "Look one cell of a reporting template up in the EBA DPM 2.0 database, by template, row "
            "and column. Returns the dimension members that define it, its data type and period type, "
            "whether it is reportable at all, and the validation rules that constrain it with their "
            "DPM-XL expressions. Use it to say what a single datapoint column means in a framework "
            "this pack does not cover, or to get a rule's expression. Answers that it is unavailable "
            "when the DPM database has not been downloaded."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "table": {"type": "string", "description": "Template code, e.g. Y_01_01 or C_01.00."},
                "row": {"type": "string", "description": "Row code, four digits, e.g. 0010."},
                "column": {"type": "string", "description": "Column code, four digits, e.g. 0010."},
                "sheet": {
                    "type": ["string", "null"],
                    "description": (
                        "Sheet code for a template that has a sheet axis - PAY's six variants are "
                        "sheets, 0010 to 0060. Null for a template without one."
                    ),
                },
            },
            "required": ["table", "row", "column", "sheet"],
            "additionalProperties": False,
        },
    },
}

DPM_TOOL_DEFINITIONS = (LOOKUP_DPM_TABLE_TOOL_DEFINITION, LOOKUP_DPM_CELL_TOOL_DEFINITION)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    answer = lookup_dpm_table(args[0]) if len(args) == 1 else lookup_dpm_cell(*args[:4])
    print(json.dumps(answer, indent=2, default=str))
