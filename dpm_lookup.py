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

# A template code is written several ways between the warehouse, the annotated layout, the
# model and whatever a notebook happens to use - Y_01_01, Y 01.01, Y_01.01, Y0101, and for
# FINREP F_12.01.a, F1201A, F_04.04.1, F04041. Stripping everything that is not a letter or
# a digit and upper-casing maps all of them onto one key, and across the 1052 template codes
# in release 4.2.1 that key collides for none of them - measured, not assumed.
#
# A regex over the punctuation was the first attempt and could not read F_12.01.a at all:
# it expected exactly two pairs of digits and nothing after them.
CODE_KEY = re.compile(r"[^A-Za-z0-9]")


class DpmError(Exception):
    """The DPM database is absent or does not hold what was asked for.

    An exception rather than SystemExit for the same reason the pack's own lookup uses
    one: an agent calls this in-process, and SystemExit walks past `except Exception`.
    """


def available() -> bool:
    return DB.exists()


def code_key(table: str) -> str:
    """Any spelling of a template code reduced to one comparable key. Pure."""
    return CODE_KEY.sub("", table).upper()


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
TABLE_BY_KEY_SQL = """
SELECT   tv.TableVID, tv.TableID, tv.Code, tv.Name,
         t.HasOpenRows <> 0 AS open_rows, t.HasOpenColumns <> 0 AS open_columns,
         t.HasOpenSheets <> 0 AS open_sheets
FROM     TableVersion tv
JOIN     "Table" t ON t.TableID = tv.TableID
WHERE    upper(regexp_replace(tv.Code, '[^A-Za-z0-9]', '', 'g')) = ?
ORDER BY tv.StartReleaseID DESC, tv.TableVID DESC
LIMIT    1
"""

TABLE_IN_MODULE_SQL = """
SELECT   tv.TableVID, tv.TableID, tv.Code, tv.Name,
         t.HasOpenRows <> 0 AS open_rows, t.HasOpenColumns <> 0 AS open_columns,
         t.HasOpenSheets <> 0 AS open_sheets
FROM     ModuleVersionComposition mvc
JOIN     TableVersion tv ON tv.TableVID = mvc.TableVID
JOIN     ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
JOIN     "Table" t ON t.TableID = tv.TableID
WHERE    upper(regexp_replace(tv.Code, '[^A-Za-z0-9]', '', 'g')) = ?
     AND mv.Code = ? AND (? IS NULL OR mv.VersionNumber = ?)
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

# Keyed on a VariableVID: one cell's own members. Distinct from TABLE_DIMENSIONS_SQL
# below, which is keyed on a TableVID and counts cells per member across a template.
CELL_DIMENSIONS_SQL = """
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


# Names are trimmed on both sides of every comparison and on the way out: item names in
# the model carry trailing spaces inconsistently. The member on F_04.04.1's cells is
# "Credit institutions " while a separate, clean item of that name also exists, and two
# items are called "Central banks", differing only by a trailing space. Matching exactly
# found nothing for a name copied out of this tool's own listing.
#
# Every dimension a template breaks down by, with its members. The discovery step: a
# template can have 800 cells and 17 dimensions, so handing an agent every cell with
# every member is both unusable and unnecessary. 17 rows with 7 members at most is not.
TABLE_DIMENSIONS_SQL = """
SELECT   trim(dim.Name) AS dimension, trim(i.Name) AS member, count(DISTINCT c.CellID) AS cells
FROM     TableVersionCell c
JOIN     VariableVersion vv ON vv.VariableVID = c.VariableVID
JOIN     ContextComposition x ON x.ContextID = vv.ContextID
JOIN     Item i ON i.ItemID = x.ItemID
JOIN     Item dim ON dim.ItemID = x.PropertyID
WHERE    c.TableVID = ? AND c.IsExcluded = 0
GROUP BY trim(dim.Name), trim(i.Name)
ORDER BY trim(dim.Name), trim(i.Name)
"""

# The cells one member covers, with the datapoint id that an xBRL-CSV report keys on.
CELLS_BY_MEMBER_SQL = """
SELECT DISTINCT
         vv.VariableID AS datapoint,
         c.CellCode,
         hr.Code AS row_code, left(hr.Label, 90) AS row_label,
         hc.Code AS column_code, left(hc.Label, 90) AS column_label,
         coalesce(hs.Code, '') AS sheet_code
FROM     TableVersionCell c
JOIN     VariableVersion vv ON vv.VariableVID = c.VariableVID
JOIN     ContextComposition x ON x.ContextID = vv.ContextID
JOIN     Item i ON i.ItemID = x.ItemID
JOIN     Item dim ON dim.ItemID = x.PropertyID
JOIN     Cell cc ON cc.CellID = c.CellID
LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
LEFT JOIN TableVersionHeader tc ON tc.TableVID = c.TableVID AND tc.HeaderID = cc.ColumnID
LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
LEFT JOIN TableVersionHeader ts ON ts.TableVID = c.TableVID AND ts.HeaderID = cc.SheetID
LEFT JOIN HeaderVersion hs ON hs.HeaderVID = ts.HeaderVID
WHERE    c.TableVID = ? AND c.IsExcluded = 0
     AND trim(lower(dim.Name)) = trim(lower(?)) AND trim(lower(i.Name)) = trim(lower(?))
ORDER BY row_code, column_code, sheet_code
"""

# Which rows add up to which, grouped. The edges of the tree rather than the tree, which
# is smaller and loses nothing: a caller that wants the nesting walks them.
SUMS_SQL = """
WITH RECURSIVE scoped AS (
    SELECT op.Code AS rule_code, os.Severity, ov.OperationVID
    FROM   Operation op
    JOIN   OperationVersion ov ON ov.OperationID = op.OperationID
    JOIN   OperationScope os ON os.OperationVID = ov.OperationVID
    JOIN   OperationScopeComposition osc ON osc.OperationScopeID = os.OperationScopeID
    JOIN   ModuleVersion mv ON mv.ModuleVID = osc.ModuleVID
    WHERE  mv.Code = ? AND (? IS NULL OR mv.VersionNumber = ?)
), node AS (
    SELECT s.rule_code, s.Severity, n.NodeID, n.ParentNodeID, n.IsLeaf, o.Symbol
    FROM   scoped s JOIN OperationNode n ON n.OperationVID = s.OperationVID
    LEFT JOIN Operator o ON o.OperatorID = n.OperatorID
), child AS (
    SELECT r.NodeID AS eq, c.NodeID, c.Symbol, c.IsLeaf
    FROM   node r JOIN node c ON c.ParentNodeID = r.NodeID
    WHERE  r.ParentNodeID IS NULL AND r.Symbol = '='
), addends AS (
    SELECT eq, NodeID AS node, IsLeaf FROM child WHERE Symbol = '+'
    UNION ALL
    SELECT a.eq, n.NodeID, n.IsLeaf FROM addends a JOIN node n ON n.ParentNodeID = a.node
), cells AS (
    SELECT r.NodeID, l."Table" AS tbl, coalesce(l."Row", '*') AS row_code,
           coalesce(l."Column", '*') AS col, coalesce(l.Sheet, '') AS sheet
    FROM   OperandReference r JOIN OperandReferenceLocation l USING (OperandReferenceID)
)
SELECT   t.rule_code, t.Severity AS severity, tc.row_code AS total_row,
         list_sort(list(DISTINCT ac.row_code))  AS addend_rows,
         list_sort(list(DISTINCT tc.col))       AS columns,
         list_sort(list(DISTINCT tc.sheet))     AS sheets
FROM     child eqs
JOIN     node t    ON t.NodeID = eqs.NodeID AND eqs.IsLeaf <> 0
JOIN     cells tc  ON tc.NodeID = t.NodeID
JOIN     addends a ON a.eq = eqs.eq AND a.IsLeaf <> 0
JOIN     cells ac  ON ac.NodeID = a.node
                  AND ac.tbl = tc.tbl AND ac.col = tc.col AND ac.sheet = tc.sheet
WHERE    tc.tbl = ?
GROUP BY t.rule_code, t.Severity, tc.row_code
ORDER BY tc.row_code, t.rule_code
"""


def cell_code(table: str, row: str, column: str, sheet: str = "") -> str:
    """The model's own spelling of a coordinate: {Y_01.01, r0010, c0010, s0010}."""
    parts = [table, f"r{row}", f"c{column}"] + ([f"s{sheet}"] if sheet else [])
    return "{" + ", ".join(parts) + "}"


def _table_version(
    con: duckdb.DuckDBPyConnection, table: str, module: str | None = None, version: str | None = None
) -> dict[str, Any]:
    """The template, newest first, or as one module version has it when that is given."""
    key = code_key(table)
    if not key:
        raise DpmError(f"{table!r} is not a template code. They look like Y_01_01, C_01.00 or F_12.01.a.")
    if module:
        # version twice: the predicate is `(? IS NULL OR mv.VersionNumber = ?)`, so that a
        # null version means the newest of that module rather than no match at all.
        found = _rows(con, TABLE_IN_MODULE_SQL, key, module, version, version)
    else:
        found = _rows(con, TABLE_BY_KEY_SQL, key)
    if not found:
        scope = f" in {module} {version}" if module else ""
        raise DpmError(f"No template matching {table!r}{scope} in the DPM 2.0 database.")
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
            dimensions = _rows(con, CELL_DIMENSIONS_SQL, cell["VariableVID"])
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


def warehouse_name(table: str, row: str, column: str) -> str:
    """The column name a warehouse gives a cell: F04041_r0040_c0015. Pure.

    The shape the gist's aggregations are built in, and the same convention the pack uses
    for PAY and DORA - the template code with its punctuation stripped, then the row and
    column codes.
    """
    return f"{code_key(table)}_r{row}_c{column}"


def lookup_dpm_dimensions(table: str, module: str | None = None, version: str | None = None) -> dict[str, Any]:
    """What a template breaks down by: its dimensions, their members, and how many cells each.

    The step to take before asking for cells. A template can carry 800 cells across 17
    dimensions, and the answer to "which rows make up this aggregate" starts with knowing
    that `Counterparty sector` is a dimension of it at all.
    """
    if not available():
        return {"found": False, "table": table, "message": BUILD_IT}
    try:
        with _connect() as con:
            tv = _table_version(con, table, module, version)
            rows = _rows(con, TABLE_DIMENSIONS_SQL, tv["TableVID"])
    except DpmError as exc:
        return {"found": False, "table": table, "message": str(exc)}

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["dimension"], []).append({"member": row["member"], "cells": row["cells"]})
    return {
        "found": True,
        "table": tv["Code"],
        "name": tv["Name"],
        "dimensions": [{"dimension": name, "members": members} for name, members in grouped.items()],
        "message": (
            "A member's cell count is how many reportable cells carry it, so the counts do not "
            "sum to the template's total - a cell carries one member of each dimension it has. "
            "Ask lookup_dpm_cells for the cells of one member."
        ),
    }


def lookup_dpm_cells(
    table: str, dimension: str, member: str, module: str | None = None, version: str | None = None
) -> dict[str, Any]:
    """The cells where one dimension takes one member: the codes that make up an aggregate.

    This is the question a hand-maintained spreadsheet of row codes exists to answer, and
    the model answers it directly. Each cell comes with its datapoint id, which is what an
    xBRL-CSV report keys its facts by, and the warehouse column name.
    """
    if not available():
        return {"found": False, "table": table, "message": BUILD_IT}
    try:
        with _connect() as con:
            tv = _table_version(con, table, module, version)
            rows = _rows(con, CELLS_BY_MEMBER_SQL, tv["TableVID"], dimension, member)
    except DpmError as exc:
        return {"found": False, "table": table, "message": str(exc)}

    if not rows:
        return {
            "found": False,
            "table": tv["Code"],
            "message": (
                f"No reportable cell of {tv['Code']} has {dimension!r} = {member!r}. "
                "Names are matched without regard to case or surrounding spaces - the model carries "
                "trailing spaces on item names inconsistently - so a near miss is a real miss. "
                "lookup_dpm_dimensions lists what there is."
            ),
        }
    return {
        "found": True,
        "table": tv["Code"],
        "dimension": dimension,
        "member": member,
        "cells": [
            row | {"warehouse_column": warehouse_name(tv["Code"], row["row_code"] or "", row["column_code"] or "")}
            for row in rows
        ],
        "datapoints": [row["datapoint"] for row in rows],
        "message": (
            "datapoints is the list to sum: dp<N> in an xBRL-CSV report is this VariableID. "
            "Two things to narrow by before summing. A member usually spans several columns, "
            "so an aggregate meant to be one column's is not the whole list. And one member "
            "can appear in several blocks of a template with the same row label in each - "
            "F_04.04.1 has Credit institutions at r0040 under Debt securities and again at "
            "r0100 under Loans and advances - so the row labels will not tell them apart and "
            "lookup_dpm_table gives each row a parent_code that does."
        ),
    }


def lookup_dpm_sums(table: str, module: str, version: str | None = None) -> dict[str, Any]:
    """Which rows add up to which, from the validation rules rather than from reading a grid.

    Scoped to a module version because a rule belongs to one: the same code is reissued
    per version and both its expression and its severity change between them.

    These are the edges of a tree, not one level of it - a total's addends are often
    totals themselves. Two entries with the same total_row are not a contradiction but
    alternative roll-ups at different granularity, and which columns each covers is part
    of the answer: in F_12.01.a row 0520 excludes the POCI row in one column of twelve.
    """
    if not available():
        return {"found": False, "table": table, "message": BUILD_IT}
    try:
        with _connect() as con:
            tv = _table_version(con, table, module, version)
            rows = _rows(con, SUMS_SQL, module, version, version, tv["Code"])
    except DpmError as exc:
        return {"found": False, "table": table, "message": str(exc)}

    totals = {row["total_row"] for row in rows}
    addends = {r for row in rows for r in row["addend_rows"]}
    return {
        "found": True,
        "table": tv["Code"],
        "module": f"{module} {version}" if version else module,
        "sums": rows,
        "roots": sorted(totals - addends),
        "message": (
            "roots are the totals nothing else breaks down into - where to start walking. "
            "A row in both totals and addends is an intermediate level. An empty answer means "
            "the module's rules are not arithmetic: DORA's are presence and comparison checks."
            if rows
            else "No sum rule of this module reaches this template."
        ),
    }


LOOKUP_DPM_DIMENSIONS_TOOL_NAME = "lookup_dpm_dimensions"
LOOKUP_DPM_CELLS_TOOL_NAME = "lookup_dpm_cells"
LOOKUP_DPM_SUMS_TOOL_NAME = "lookup_dpm_sums"

_TABLE_ARG = {
    "type": "string",
    "description": (
        "Template code in any spelling - F_12.01.a, F1201A, F 12.01.a, Y_01_01, C_01.00 - "
        "matched by stripping the punctuation, which collides for none of the model's 1052 codes."
    ),
}
_MODULE_ARG = {
    "type": ["string", "null"],
    "description": (
        "Module code such as PSD_FRP, FINREP9 or COREP_OF, with version, to pin the answer to "
        "one module version. Null takes the newest version of the template, which is right for "
        "a question about the current framework and wrong for a question about a past one."
    ),
}
_VERSION_ARG = {
    "type": ["string", "null"],
    "description": "Module version such as 1.1.0 or 3.3.0. Null means the newest.",
}

LOOKUP_DPM_DIMENSIONS_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_DIMENSIONS_TOOL_NAME,
        "description": (
            "What a reporting template breaks down by: every dimension of it, that dimension's "
            "members, and how many reportable cells carry each member. Call this before "
            "lookup_dpm_cells - it is what tells you that 'Counterparty sector' or 'Type of "
            "financial instruments' is a dimension of the template at all, and under which exact "
            "wording. Use it to answer which rows or columns make up a business aggregate without "
            "maintaining a spreadsheet of row codes by hand. Answers that it is unavailable when "
            "the DPM database has not been downloaded."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {"table": _TABLE_ARG, "module": _MODULE_ARG, "version": _VERSION_ARG},
            "required": ["table", "module", "version"],
            "additionalProperties": False,
        },
    },
}

LOOKUP_DPM_CELLS_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_CELLS_TOOL_NAME,
        "description": (
            "The cells of a template where one dimension takes one member - the codes that make "
            "up an aggregate. Returns each cell's datapoint id, which is what an xBRL-CSV report "
            "keys its facts by, its row and column codes with their labels, and the warehouse "
            "column name such as F04041_r0040_c0015. Take the dimension and member wording from "
            "lookup_dpm_dimensions; a near miss matches nothing. Answers that it is unavailable "
            "when the DPM database has not been downloaded."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "table": _TABLE_ARG,
                "dimension": {
                    "type": "string",
                    "description": "As lookup_dpm_dimensions spells it, e.g. 'Counterparty sector'.",
                },
                "member": {
                    "type": "string",
                    "description": "As lookup_dpm_dimensions spells it, e.g. 'Credit institutions'.",
                },
                "module": _MODULE_ARG,
                "version": _VERSION_ARG,
            },
            "required": ["table", "dimension", "member", "module", "version"],
            "additionalProperties": False,
        },
    },
}

LOOKUP_DPM_SUMS_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_SUMS_TOOL_NAME,
        "description": (
            "Which rows of a template add up to which, taken from the module's validation rules "
            "rather than from reading a grid. Returns one entry per rule and total: the total "
            "row, its addend rows, and which columns and sheets the rule covers. These are the "
            "edges of a tree, not one level - an addend is often a total itself, and `roots` "
            "names the totals nothing else breaks down into. Two entries with the same total row "
            "are alternative roll-ups at different granularity, not a contradiction, and a rule "
            "can cover eleven columns of twelve. Needs the module code because a rule belongs to "
            "one module version and changes between them. Answers nothing for a module whose "
            "rules are not arithmetic, such as DORA's presence checks."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "table": _TABLE_ARG,
                "module": {"type": "string", "description": "Module code, e.g. FINREP9 or PSD_FRP. Required here."},
                "version": _VERSION_ARG,
            },
            "required": ["table", "module", "version"],
            "additionalProperties": False,
        },
    },
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

DPM_TOOL_DEFINITIONS = (
    LOOKUP_DPM_TABLE_TOOL_DEFINITION,
    LOOKUP_DPM_CELL_TOOL_DEFINITION,
    LOOKUP_DPM_DIMENSIONS_TOOL_DEFINITION,
    LOOKUP_DPM_CELLS_TOOL_DEFINITION,
    LOOKUP_DPM_SUMS_TOOL_DEFINITION,
)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    answer = lookup_dpm_table(args[0]) if len(args) == 1 else lookup_dpm_cell(*args[:4])
    print(json.dumps(answer, indent=2, default=str))
