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
import urllib.parse
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

# module_version is part of the answer, not a detail: with no version asked for, this is
# which one "the newest" resolved to, and a caller that scopes a second query by module
# needs that rather than a null. SUMS_SQL with a null version scopes to every version of
# the module at once, which took over two minutes for FINREP9 against 0.1s for one.
TABLE_IN_MODULE_SQL = """
SELECT   tv.TableVID, tv.TableID, tv.Code, tv.Name, mv.VersionNumber AS module_version,
         rel.Code AS dpm_release,
         mv.ToReferenceDate IS NOT NULL AND mv.FromReferenceDate = mv.ToReferenceDate AS do_not_use,
         t.HasOpenRows <> 0 AS open_rows, t.HasOpenColumns <> 0 AS open_columns,
         t.HasOpenSheets <> 0 AS open_sheets
FROM     ModuleVersionComposition mvc
JOIN     TableVersion tv ON tv.TableVID = mvc.TableVID
JOIN     ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
JOIN     Release rel ON rel.ReleaseID = mv.StartReleaseID
JOIN     "Table" t ON t.TableID = tv.TableID
WHERE    upper(regexp_replace(tv.Code, '[^A-Za-z0-9]', '', 'g')) = ?
     AND mv.Code = ? AND (? IS NULL OR mv.VersionNumber = ?)
-- A module version nobody reports under is the last thing "newest" should mean.
ORDER BY (mv.ToReferenceDate IS NOT NULL AND mv.FromReferenceDate = mv.ToReferenceDate),
         tv.StartReleaseID DESC, mv.FromReferenceDate DESC, tv.TableVID DESC
LIMIT    1
"""

MODULES_SQL = """
SELECT DISTINCT f.Code AS framework, f.Name AS framework_name, mv.Code AS module,
       mv.VersionNumber AS taxonomy_version, rel.Code AS dpm_release,
       mv.ToReferenceDate IS NOT NULL AND mv.FromReferenceDate = mv.ToReferenceDate AS do_not_use,
       -- ISO strings, not DATEs: these answers are serialised with json.dumps by whoever
       -- holds them, and a date raises there. Cast at the source so a caller that reaches
       -- past dispatch into the lookup is safe too.
       CAST(mv.FromReferenceDate AS VARCHAR) AS from_reference_date,
       CAST(mv.ToReferenceDate AS VARCHAR) AS to_reference_date
FROM   ModuleVersionComposition mvc
JOIN   ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
JOIN   Module m ON m.ModuleID = mv.ModuleID
JOIN   Framework f ON f.FrameworkID = m.FrameworkID
JOIN   Release rel ON rel.ReleaseID = mv.StartReleaseID
WHERE  mvc.TableID = ?
ORDER  BY mv.Code, mv.VersionNumber
"""

# Direction X is the column axis, Y the row axis and Z the sheet axis. ParentHeaderID is
# what makes an "Of which" row a child of the row it qualifies - the nesting the annotated
# layout only shows by indentation.
#
# Header.IsKey marks the key dimensions of an open table: the headers that identify a
# record rather than hold a figure. They are what a report writes as its own columns, and
# property_code is the heading it writes - V_04.01 is keyed on qCDF, qBBE and ei1452, and
# a file of it carries exactly those three beside datapoint and factValue.
HEADERS_SQL = """
SELECT   h.Direction AS direction, hv.Code AS code, hv.Label AS label,
         parent.Code AS parent_code, tvh.IsAbstract <> 0 AS is_abstract,
         h.IsKey <> 0 AS is_key, ic.Code AS property_code, i.Name AS property
FROM     TableVersionHeader tvh
JOIN     HeaderVersion hv ON hv.HeaderVID = tvh.HeaderVID
JOIN     Header h ON h.HeaderID = tvh.HeaderID
LEFT JOIN TableVersionHeader ptvh ON ptvh.TableVID = tvh.TableVID AND ptvh.HeaderID = tvh.ParentHeaderID
LEFT JOIN HeaderVersion parent ON parent.HeaderVID = ptvh.HeaderVID
LEFT JOIN Item i ON i.ItemID = hv.PropertyID
-- EndReleaseID IS NULL is the code in force now, and it is exactly one per property:
-- 233 of them have been recoded at some point, and an unscoped join returned the header
-- once per code it has ever had - 11022 duplicated headers across the model, each of
-- which put a retired code into the set a report's columns are compared against.
LEFT JOIN ItemCategory ic ON ic.ItemID = i.ItemID AND ic.EndReleaseID IS NULL
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

# Two different versions, and conflating them is the usual mistake. `VersionNumber` is
# the *taxonomy* version of the module - FINREP9 3.3.0 - and the DPM version, which is
# what a reporting institution normally means by "the version", is the release the module
# version was introduced in: StartReleaseID, 4.2 for that one. Every answer here reports
# both, named.
#
# FromReferenceDate = ToReferenceDate marks a module version that is not to be used: it
# was published and superseded without ever covering a reporting period. 43 of the 165
# module versions in release 4.4 are such, so "the newest" has to skip them.

# A rule code is not one rule: the same code is re-issued per module version, and the
# expression and the severity both change between them - v09247_s is a warning in PSD_FRP
# 1.1.0 and an error in 1.2.0. So the module version is part of the answer, not a filter
# applied behind the caller's back.
RULES_SQL = """
SELECT   o.Code AS rule_code, os.Severity AS severity, ov.Expression AS expression,
         mv.Code || ' ' || mv.VersionNumber AS module,
         -- OperationScope.IsActive is the EBA's deactivated-rules list, in the model:
         -- 2928 of 30791 scopes are off. A description that names a deactivated rule
         -- tells a reader to satisfy a check nobody runs.
         os.IsActive <> 0 AS active
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
GROUP BY rule_code, severity, expression, module, active
ORDER BY rule_code, module
"""


def fold_rules(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One entry per rule, severity, expression and activity, with the module versions.

    Pure. Two entries for the same code is not a duplicate: it means the rule was changed
    between module versions, and which one applies depends on what the table reports.
    `active` is false for a rule the EBA has deactivated - published and not run.
    """
    folded: dict[tuple[str, str, str, bool], list[str]] = {}
    for row in rows:
        key = (row["rule_code"], row["severity"], row["expression"], bool(row["active"]))
        folded.setdefault(key, []).append(row["module"])
    return [
        # `active` is part of the key, not a property of the code: the EBA deactivates a
        # rule for one module version and leaves it running in another, so folding them
        # together would hide which is which.
        {"rule_code": code, "severity": severity, "expression": expression, "active": active, "modules": modules}
        for (code, severity, expression, active), modules in folded.items()
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


# A reported fact names a datapoint and nothing else, so this is the way back from a file
# to the model. One id can be a cell of several module versions, which is why the answer
# lists them rather than picking one.
DATAPOINT_SQL = """
SELECT DISTINCT
         tv.Code AS table_code, tv.Name AS table_name, c.CellCode,
         coalesce(hr.Code, '*') AS row_code, left(hr.Label, 90) AS row_label,
         coalesce(hc.Code, '*') AS column_code, left(hc.Label, 90) AS column_label,
         coalesce(hs.Code, '') AS sheet_code,
         c.IsExcluded <> 0 AS is_excluded
FROM     VariableVersion vv
JOIN     TableVersionCell c ON c.VariableVID = vv.VariableVID
JOIN     TableVersion tv ON tv.TableVID = c.TableVID
JOIN     Cell cc ON cc.CellID = c.CellID
LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
LEFT JOIN TableVersionHeader tc ON tc.TableVID = c.TableVID AND tc.HeaderID = cc.ColumnID
LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
LEFT JOIN TableVersionHeader ts ON ts.TableVID = c.TableVID AND ts.HeaderID = cc.SheetID
LEFT JOIN HeaderVersion hs ON hs.HeaderVID = ts.HeaderVID
WHERE    vv.VariableID = ?
"""

DATAPOINT_MODULES_SQL = """
SELECT DISTINCT mv.Code AS module, mv.VersionNumber AS taxonomy_version, rel.Code AS dpm_release,
         mv.ToReferenceDate IS NOT NULL AND mv.FromReferenceDate = mv.ToReferenceDate AS do_not_use
FROM     VariableVersion vv
JOIN     TableVersionCell c ON c.VariableVID = vv.VariableVID
JOIN     ModuleVersionComposition mvc ON mvc.TableVID = c.TableVID
JOIN     ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
JOIN     Release rel ON rel.ReleaseID = mv.StartReleaseID
WHERE    vv.VariableID = ?
ORDER BY 1, 2
"""

# The highest id this release knows. An unknown id above it is a newer release rather than
# a typo, and that is the one thing a caller cannot work out from an empty answer.
MAX_DATAPOINT_SQL = "SELECT max(VariableID) AS max_datapoint FROM VariableVersion"

RELEASES_SQL = "SELECT ReleaseID, Code FROM Release ORDER BY ReleaseID"

# A report's column headers are property codes, and they live here rather than in the
# taxonomy files. The code is scoped to a release: the same property is `x21` up to
# release 4.2 and `qx2013` after it, so a header that resolves to nothing is more often
# the wrong release than the wrong file.
PROPERTY_CODE_SQL = """
SELECT   ic.Code, i.Name AS property, ic.StartReleaseID, ic.EndReleaseID,
         nullif(i.Description, '') AS definition
FROM     ItemCategory ic
JOIN     Item i ON i.ItemID = ic.ItemID
WHERE    ic.Code = ?
ORDER BY ic.StartReleaseID DESC
"""


# Which taxonomy version of a module a DPM release shipped. A module version is in force
# from the release it was introduced in until the one that replaced it, and ReleaseID
# increases with publication order, so the window is a pair of comparisons. In DPM 4.0 the
# FINREP9 module version is 3.2.0 - the one marked do_not_use - which is what that release
# shipped and is the honest answer to "what did 4.0 have".
MODULE_VERSION_IN_RELEASE_SQL = """
SELECT   mv.VersionNumber AS version, rel.Code AS dpm_release,
         mv.ToReferenceDate IS NOT NULL AND mv.FromReferenceDate = mv.ToReferenceDate AS do_not_use
FROM     ModuleVersion mv
JOIN     Release rel ON rel.ReleaseID = mv.StartReleaseID
JOIN     Release asked ON asked.Code = ?
WHERE    mv.Code = ?
     AND mv.StartReleaseID <= asked.ReleaseID
     AND (mv.EndReleaseID IS NULL OR mv.EndReleaseID > asked.ReleaseID)
ORDER BY mv.StartReleaseID DESC
LIMIT    1
"""

RELEASES_IN_FILE_SQL = "SELECT Code FROM Release ORDER BY ReleaseID"

# A precondition is a real code with no scope of its own: it is not run against a module,
# it gates the rules that name it. p_1 reads `( {v_C_95.00} or {v_C_95.00} ) and
# {v_C_97.00}` and gates v22480_m. Answering "no such rule" for one would be wrong, and
# trimming its digits off would answer about a different precondition.
PRECONDITION_SQL = """
SELECT   op.Code AS code, op.Type AS type, ov.Expression AS expression,
         list_sort(list(DISTINCT used.Code)) AS used_by
FROM     Operation op
JOIN     OperationVersion ov ON ov.OperationID = op.OperationID
LEFT JOIN OperationVersion gated ON gated.PreconditionOperationVID = ov.OperationVID
LEFT JOIN Operation used ON used.OperationID = gated.OperationID
WHERE    trim(lower(op.Code)) = trim(lower(?))
GROUP BY op.Code, op.Type, ov.Expression
"""


def _version_asked_for(
    con: duckdb.DuckDBPyConnection, module: str, version: str | None, dpm_release: str | None
) -> str | None:
    """The taxonomy version a caller asked for, by either name. Null for "the newest".

    `version` is the module's own version number and `dpm_release` is the DPM release,
    which is what a reporting institution usually means. Both at once is two different
    questions, and answering one of them silently is how a release gets reported under a
    taxonomy version it never shipped.
    """
    if version and dpm_release:
        raise DpmError(
            f"Asked for both taxonomy version {version!r} and DPM release {dpm_release!r}. "
            "They are different numbers for different things - pass one."
        )
    if not dpm_release:
        return version
    found = _rows(con, MODULE_VERSION_IN_RELEASE_SQL, dpm_release, module)
    if found:
        return found[0]["version"]
    releases = [row["Code"] for row in _rows(con, RELEASES_IN_FILE_SQL)]
    if dpm_release not in releases:
        raise DpmError(
            f"No DPM release {dpm_release!r} in this copy of the database. It has: {', '.join(releases)}. "
            "A newer release is a separate download - see source/fetch_dpm2.py --release."
        )
    raise DpmError(f"Module {module!r} is not in DPM release {dpm_release!r}.")


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


def lookup_dpm_dimensions(
    table: str, module: str | None = None, version: str | None = None, dpm_release: str | None = None
) -> dict[str, Any]:
    """What a template breaks down by: its dimensions, their members, and how many cells each.

    The step to take before asking for cells. A template can carry 800 cells across 17
    dimensions, and the answer to "which rows make up this aggregate" starts with knowing
    that `Counterparty sector` is a dimension of it at all.
    """
    if not available():
        return {"found": False, "table": table, "message": BUILD_IT}
    try:
        with _connect() as con:
            version = _version_asked_for(con, module or "", version, dpm_release)
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
    table: str,
    dimension: str,
    member: str,
    module: str | None = None,
    version: str | None = None,
    dpm_release: str | None = None,
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
            version = _version_asked_for(con, module or "", version, dpm_release)
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


def lookup_dpm_sums(
    table: str, module: str, version: str | None = None, dpm_release: str | None = None
) -> dict[str, Any]:
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
            version = _version_asked_for(con, module, version, dpm_release)
            tv = _table_version(con, table, module, version)
            # Never the caller's null: see TABLE_IN_MODULE_SQL. Scoping the recursive
            # query to one module version is the difference between 0.1s and minutes.
            scoped = version or tv["module_version"]
            rows = _rows(con, SUMS_SQL, module, scoped, scoped, tv["Code"])
            release, unusable = tv["dpm_release"], tv["do_not_use"]
    except DpmError as exc:
        return {"found": False, "table": table, "message": str(exc)}

    totals = {row["total_row"] for row in rows}
    addends = {r for row in rows for r in row["addend_rows"]}
    return {
        "found": True,
        "table": tv["Code"],
        "module": module,
        "taxonomy_version": scoped,
        "dpm_release": release,
        "do_not_use": unusable,
        "sums": rows,
        "roots": sorted(totals - addends),
        "message": (
            "taxonomy_version is the module's own version number; dpm_release is the DPM "
            "version it belongs to, which is what a reporting institution usually means by the "
            "version. roots are the totals nothing else breaks down into - where to start walking. "
            "A row in both totals and addends is an intermediate level. An empty answer means "
            "the module's rules are not arithmetic: DORA's are presence and comparison checks."
            if rows
            else "No sum rule of this module reaches this template."
        ),
    }


DP = re.compile(r"^\s*(?:dp?)?(\d+)\s*$", re.IGNORECASE)

# A validation engine numbers each occurrence of a rule it ran: v3775_s covers 432 cells
# of C_20.00 and expands once per reported record, so an outcome names v3775_s_62. The
# model has the rule, never the occurrence. Only tried when the code itself is not found,
# because p_1133 and the dash-numbered variants v10270_a-2 are real codes in their own
# right and must not be truncated into something else.
OCCURRENCE = re.compile(r"^(?P<rule>.+?)_(?P<occurrence>\d+)$")


def datapoint_id(datapoint: str | int) -> int | None:
    """`dp1010005012`, `1010005012` or the integer, as the integer. Pure.

    A reported fact writes the id with the `dp` prefix the taxonomy gives it; the model
    stores the number. Anything else is a caller error worth naming rather than a zero.
    """
    if isinstance(datapoint, int):
        return datapoint
    found = DP.match(str(datapoint))
    return int(found.group(1)) if found else None


def lookup_dpm_datapoint(datapoint: str | int) -> dict[str, Any]:
    """What a reported datapoint id is: the cell, its labels, and the modules it is in.

    This is the way back from a file to the model. A fact in an xBRL-CSV report names a
    datapoint and nothing else, so without this an id is unreadable.

    An id the release does not have is reported with the highest it does have, because
    that is the difference between a typo and a file built against a newer release - and
    an empty answer alone cannot tell a caller which.
    """
    if not available():
        return {"found": False, "datapoint": datapoint, "message": BUILD_IT}
    number = datapoint_id(datapoint)
    if number is None:
        return {
            "found": False,
            "datapoint": datapoint,
            "message": f"{datapoint!r} is not a datapoint id. They look like dp1010005012 or 152217.",
        }
    with _connect() as con:
        cells = _rows(con, DATAPOINT_SQL, number)
        if not cells:
            highest = _rows(con, MAX_DATAPOINT_SQL)[0]["max_datapoint"]
            return {
                "found": False,
                "datapoint": number,
                "max_datapoint": highest,
                "message": (
                    f"No datapoint {number} in this copy of the DPM, whose highest is {highest}. "
                    + (
                        "The id is above that, so the file is built against a newer release than "
                        "the one downloaded here, not against another module of it."
                        if number > highest
                        else "The id is within range, so it is either a typo or a datapoint of a "
                        "release older than this one."
                    )
                ),
            }
        modules = _rows(con, DATAPOINT_MODULES_SQL, number)
    return {
        "found": True,
        "datapoint": number,
        "cells": cells,
        "modules": modules,
        "message": (
            "One id can be a cell of several module versions - the datapoint is what they share. "
            "An excluded cell is in the model but not reportable."
        ),
    }


def lookup_dpm_property(code: str) -> dict[str, Any]:
    """What a report's column header means: `qGDF`, `qBBE`, `ei1452`, `CPS`.

    The columns after `datapoint` and `factValue` in an xBRL-CSV report are the open
    dimensions, headed by the property's code. The code is scoped to a release - the same
    property is `x21` through release 4.2 and `qx2013` after it - so a header that
    resolves to nothing is more often the wrong release than the wrong file.
    """
    if not available():
        return {"found": False, "code": code, "message": BUILD_IT}
    with _connect() as con:
        found = _rows(con, PROPERTY_CODE_SQL, code.strip())
        releases = {row["ReleaseID"]: row["Code"] for row in _rows(con, RELEASES_SQL)}
    if not found:
        return {
            "found": False,
            "code": code,
            "message": (
                f"No property coded {code!r} in this copy of the DPM. A code is release-scoped, so "
                "a header from a newer release will not be here."
            ),
        }
    return {
        "found": True,
        "code": code,
        "properties": [
            {
                "property": row["property"],
                "definition": row["definition"],
                "from_release": releases.get(row["StartReleaseID"]),
                "until_release": releases.get(row["EndReleaseID"]),
            }
            for row in found
        ],
        "message": (
            "until_release is null where the code is the current one. More than one entry means "
            "the code was reused or renamed between releases."
        ),
    }


# A validation report names a rule code and nothing else, so this is the way back from an
# outcome to what was checked. One code is one rule per module version, and both the
# expression and the severity change between them - v0174_m is an error in COREP_OF 3.1.0
# and 4.0.0 and a warning in 4.1.0 - so the answer is a row per version, not one verdict.
RULE_SCOPES_SQL = """
SELECT   ov.OperationVID AS operation_vid,
         mv.Code AS module, mv.VersionNumber AS taxonomy_version, rel.Code AS dpm_release,
         mv.ToReferenceDate IS NOT NULL AND mv.FromReferenceDate = mv.ToReferenceDate AS do_not_use,
         os.Severity AS severity, os.IsActive <> 0 AS active,
         CAST(os.FromSubmissionDate AS VARCHAR) AS from_submission_date,
         ov.Expression AS expression, nullif(ov.Description, '') AS description
FROM     Operation op
JOIN     OperationVersion ov ON ov.OperationID = op.OperationID
JOIN     OperationScope os ON os.OperationVID = ov.OperationVID
JOIN     OperationScopeComposition osc ON osc.OperationScopeID = os.OperationScopeID
JOIN     ModuleVersion mv ON mv.ModuleVID = osc.ModuleVID
JOIN     Release rel ON rel.ReleaseID = mv.StartReleaseID
WHERE    trim(lower(op.Code)) = trim(lower(?))
ORDER BY mv.Code, mv.VersionNumber
"""

# The page that answers a rule code, so an answer can be cited rather than retyped. The
# release is in the query string, so a link is to the rule as that release had it - which
# matters, because 2037 of 7514 consecutive version pairs change the expression.
RULE_PAGE = "https://oluies.github.io/om-eba-annotatedtpl/"


def rule_url(rule_code: str, dpm_release: str | None = None) -> str:
    """A link to this rule on the published page, under one release when one is given."""
    query = urllib.parse.urlencode(
        {"q": "rule", "rule_code": rule_code} | ({"release": dpm_release} if dpm_release else {})
    )
    return f"{RULE_PAGE}?{query}"


# One row per version of the rule itself, which is not the same as one row per module
# version: a rule is reissued when its expression changes and reused across modules when
# it does not. RULE_SCOPES_SQL answers where it applies; this answers what it said when.
RULE_VERSIONS_SQL = """
SELECT   ov.OperationVID       AS operation_vid,
         rs.Code               AS from_release,
         coalesce(re.Code, '') AS to_release,
         ov.StartReleaseID     AS start_release_id,
         ov.Expression         AS expression,
         nullif(ov.Description, '') AS description,
         list_sort(list(DISTINCT os.Severity)) AS severities,
         bool_or(os.IsActive <> 0) AS active_anywhere
FROM     Operation op
JOIN     OperationVersion ov ON ov.OperationID = op.OperationID
LEFT JOIN OperationScope os ON os.OperationVID = ov.OperationVID
LEFT JOIN Release rs ON rs.ReleaseID = ov.StartReleaseID
LEFT JOIN Release re ON re.ReleaseID = ov.EndReleaseID
WHERE    trim(lower(op.Code)) = trim(lower(?))
GROUP BY ALL
ORDER BY ov.StartReleaseID
"""


def rule_changes(versions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """What changed about a rule between releases, read off its versions.

    The same derivation as for a datapoint, and for the same reason: the DPM's ChangeLog
    table ships empty, so an account of what changed is the difference between two rows or
    it does not exist.

    `rewritten` is the one that matters. A rule code is not a stable statement - 2037 of
    7514 consecutive version pairs change the expression - so "the file passed v0174_m"
    means nothing without the release it was checked under.
    """
    if not versions:
        return []
    ordered = sorted(versions, key=lambda row: row["start_release_id"])
    found = [{"release": ordered[0]["from_release"], "kind": "introduced"}]
    for before, after in zip(ordered, ordered[1:], strict=False):
        if before["expression"] != after["expression"]:
            # Whitespace only in 32 of the 2037 pairs that differ, and those 32 would be
            # false alarms on a page that says what changed. Labelled rather than hidden:
            # a reader comparing two releases byte for byte should still find them here.
            was, now = before["expression"] or "", after["expression"] or ""
            cosmetic = re.sub(r"\s+", "", was) == re.sub(r"\s+", "", now)
            found.append(
                {
                    "release": after["from_release"],
                    "kind": "reformatted" if cosmetic else "rewritten",
                    "was": was[:200],
                    "now": now[:200],
                }
            )
        if before["severities"] != after["severities"]:
            found.append(
                {
                    "release": after["from_release"],
                    "kind": "severity",
                    "was": ", ".join(before["severities"] or []),
                    "now": ", ".join(after["severities"] or []),
                }
            )
        if before["active_anywhere"] != after["active_anywhere"]:
            found.append(
                {
                    "release": after["from_release"],
                    "kind": "reactivated" if after["active_anywhere"] else "deactivated",
                }
            )
    if ordered[-1]["to_release"]:
        found.append({"release": ordered[-1]["to_release"], "kind": "withdrawn"})
    return found


# Which cells one version of the rule names. The DPM has already resolved every leaf of
# the expression to a location, so this is a join rather than a parse of the DPM-XL.
RULE_CELLS_SQL = """
SELECT DISTINCT l."Table" AS table_code, coalesce(l."Row", '*') AS row_code,
         coalesce(l."Column", '*') AS column_code, coalesce(l.Sheet, '') AS sheet_code
FROM     OperationNode n
JOIN     OperandReference r ON r.NodeID = n.NodeID
JOIN     OperandReferenceLocation l USING (OperandReferenceID)
WHERE    n.OperationVID = ?
ORDER BY 1, 2, 3
"""


def lookup_dpm_rule(rule_code: str) -> dict[str, Any]:
    """What a validation rule code means: the check, where it applies, and how severely.

    A validation report names a code and a failing cell; this is the way back to what was
    checked. One code is one rule *per module version*: v0174_m reads
    `{r0070} = {r0080} + {r0090} + {r0091}` on C_01.00 column 0010 in every version of
    COREP_OF that has it, but it is an error in 3.1.0 and 4.0.0 and a warning in 4.1.0.
    So the answer is a row per version with its own severity, submission date and cells,
    and a caller that needs one verdict has to say which version it is reporting under.
    """
    if not available():
        return {"found": False, "rule_code": rule_code, "message": BUILD_IT}
    occurrence = None
    with _connect() as con:
        scopes = _rows(con, RULE_SCOPES_SQL, rule_code)
        if not scopes and (gate := _rows(con, PRECONDITION_SQL, rule_code)):
            # Real, and not scoped to a module: say what it is rather than "no such rule".
            return {
                "found": True,
                "rule_code": rule_code,
                "occurrence": None,
                "type": gate[0]["type"],
                "scopes": [],
                "tables": [],
                "expressions": [row["expression"] for row in gate],
                "used_by": sorted({code for row in gate for code in row["used_by"] if code}),
                "message": (
                    f"This is a {gate[0]['type']}, not a rule run against a module: it has no "
                    "severity and no module version of its own. It gates the rules in used_by - "
                    "they are checked only where it holds - so an outcome naming it is about one "
                    "of those."
                ),
            }
        if not scopes and (found := OCCURRENCE.match(rule_code.strip())):
            # An outcome's code with the engine's occurrence number on it. The number is
            # only reported when the stem is a rule: otherwise this was a code that
            # happens to end in digits, and trimming it would invent a different one.
            scopes = _rows(con, RULE_SCOPES_SQL, found["rule"])
            if scopes:
                rule_code, occurrence = found["rule"], found["occurrence"]
        if not scopes:
            return {
                "found": False,
                "rule_code": rule_code,
                "message": (
                    f"No rule {rule_code!r} in this copy of the DPM. Codes look like v0174_m, "
                    "v23845_h or e23677_e. A rule retired before this release, or added after it, "
                    "is not here - check the release before the code."
                ),
            }
        cells = {scope["operation_vid"]: _rows(con, RULE_CELLS_SQL, scope["operation_vid"]) for scope in scopes}
        versions = _rows(con, RULE_VERSIONS_SQL, rule_code)
    severities = {scope["severity"] for scope in scopes}
    changed = rule_changes(versions)
    return {
        "found": True,
        "rule_code": rule_code,
        "occurrence": occurrence,
        "scopes": [
            {k: v for k, v in scope.items() if k != "operation_vid"} | {"cells": cells[scope["operation_vid"]]}
            for scope in scopes
        ],
        "tables": sorted({cell["table_code"] for rows in cells.values() for cell in rows}),
        "url": rule_url(rule_code),
        "versions": [
            {key: value for key, value in version.items() if key != "operation_vid"}
            | {"url": rule_url(rule_code, version["from_release"])}
            for version in versions
        ],
        "changes": changed,
        "message": (
            (
                f"The code asked for carried the occurrence number {occurrence}, which is the "
                "validation engine's count of which application of the rule failed - the rule "
                "itself is the part before it. The model has the rule, not the occurrence: which "
                "reported record or column the number points at is in the validation report. "
                if occurrence
                else ""
            )
            + "One row per module version, because that is what a rule code is. "
            + (
                f"The severity is not the same in all of them ({', '.join(sorted(severities))}), so an "
                "outcome means nothing until the module version it was raised under is known."
                if len(severities) > 1
                else f"The severity is {severities.pop()} in every version here."
            )
            + " from_submission_date is the first reporting date each version applies to."
            + (
                " What it checks is not the same in every release either: "
                + ", ".join(
                    f"{change['kind']} in {change['release']}" for change in changed if change["kind"] != "introduced"
                )
                + ". A code is not a stable statement, so cite the release with it - url carries one."
                if any(change["kind"] not in ("introduced", "reformatted") for change in changed)
                else " The expression, severity and activity are the same in every release here."
            )
        ),
    }


# The other direction: every rule that reaches one template, scoped to one module version
# because a rule belongs to one. The rows and columns are this template's own - a rule
# often spans two templates, and which cells of *this* one it touches is the question.
TABLE_RULES_SQL = """
SELECT   op.Code AS rule_code, os.Severity AS severity, os.IsActive <> 0 AS active,
         any_value(ov.Expression) AS expression,
         -- FILTER rather than a WHERE on the table: the rule's locations in other
         -- templates have to stay in the group, or `tables` below is always this one
         -- and a cross-return check reads as a local one.
         list_sort(list(DISTINCT coalesce(l."Row", '*')) FILTER (WHERE l."Table" = ?))    AS rows,
         list_sort(list(DISTINCT coalesce(l."Column", '*')) FILTER (WHERE l."Table" = ?)) AS columns,
         list_sort(list(DISTINCT l."Table")) AS tables
FROM     OperandReferenceLocation l
JOIN     OperandReference ref USING (OperandReferenceID)
JOIN     OperationNode n ON n.NodeID = ref.NodeID
JOIN     OperationVersion ov ON ov.OperationVID = n.OperationVID
JOIN     Operation op ON op.OperationID = ov.OperationID
JOIN     OperationScope os ON os.OperationVID = ov.OperationVID
JOIN     OperationScopeComposition osc ON osc.OperationScopeID = os.OperationScopeID
JOIN     ModuleVersion mv ON mv.ModuleVID = osc.ModuleVID
WHERE    mv.Code = ? AND mv.VersionNumber = ?
     AND ov.OperationVID IN (
         SELECT n2.OperationVID
         FROM   OperandReferenceLocation l2
         JOIN   OperandReference ref2 USING (OperandReferenceID)
         JOIN   OperationNode n2 ON n2.NodeID = ref2.NodeID
         WHERE  l2."Table" = ?
     )
GROUP BY op.Code, os.Severity, os.IsActive
ORDER BY op.Code
"""


# The newest version of a module, for a rules question that names no version. Separate
# from _table_version because a rule can name a template its own module does not contain:
# COREP_LE checks four cells of C_01.00, which belongs to COREP_OF.
MODULE_VERSION_SQL = """
SELECT   mv.VersionNumber AS version, rel.Code AS dpm_release,
         mv.ToReferenceDate IS NOT NULL AND mv.FromReferenceDate = mv.ToReferenceDate AS do_not_use
FROM     ModuleVersion mv
JOIN     Release rel ON rel.ReleaseID = mv.StartReleaseID
WHERE    mv.Code = ? AND (? IS NULL OR mv.VersionNumber = ?)
ORDER BY (mv.ToReferenceDate IS NOT NULL AND mv.FromReferenceDate = mv.ToReferenceDate),
         mv.FromReferenceDate DESC, mv.ModuleVID DESC
LIMIT    1
"""


def lookup_dpm_rules(
    table: str, module: str, version: str | None = None, dpm_release: str | None = None
) -> dict[str, Any]:
    """Every validation rule that reaches one template, with what it touches in it.

    The reverse of lookup_dpm_rule: that one starts from a code in a validation outcome,
    this one from a template you are about to describe or report. C_01.00 has 50 rules in
    COREP_OF 4.1.0 and 4 more in COREP_LE, which is why the module is not optional - the
    same template is checked differently depending on which return it is part of.

    The module need not be one the template belongs to. COREP_LE contains no C_01.00 and
    still checks four of its cells - the kind of rule a reader is least likely to know
    about, and the reason the template is resolved without the module here.

    `rows` and `columns` are this template's own; `tables` is every template the rule
    names. More than one means the check reaches outside this template, and its other
    half is not in this answer - v0655_m multiplies a C_01.00 row by a C_28.00 column.
    """
    if not available():
        return {"found": False, "table": table, "message": BUILD_IT}
    try:
        with _connect() as con:
            tv = _table_version(con, table)
            version = _version_asked_for(con, module, version, dpm_release)
            # The version goes through the database even when the caller named one. Taking
            # it on trust turned a mistyped version into found: true with no rules and the
            # message "no rule of this module version names a cell of this template" - a
            # confident claim that a template is unchecked, which is the one answer this
            # must never give by accident.
            found = _rows(con, MODULE_VERSION_SQL, module, version, version)
            if not found:
                scope = f"{module!r} taxonomy version {version!r}" if version else f"{module!r}"
                raise DpmError(f"No module {scope} in the DPM 2.0 database.")
            scoped, release, unusable = (found[0][key] for key in ("version", "dpm_release", "do_not_use"))
            rules = _rows(con, TABLE_RULES_SQL, tv["Code"], tv["Code"], module, scoped, tv["Code"])
    except DpmError as exc:
        return {"found": False, "table": table, "message": str(exc)}

    severities: dict[str, int] = {}
    for rule in rules:
        severities[rule["severity"]] = severities.get(rule["severity"], 0) + 1
    return {
        "found": True,
        "table": tv["Code"],
        "module": module,
        "taxonomy_version": scoped,
        "dpm_release": release,
        "do_not_use": unusable,
        "rules": rules,
        "severities": severities,
        "message": (
            "Every rule of this module version that names a cell of this template. rows and "
            "columns are the ones it names here; tables is every template the rule names, and "
            "more than one means the check reaches outside this one. active is false for a rule "
            "the EBA has deactivated: it is published and not run, so do not tell a reader to "
            "satisfy it. An empty "
            "answer means this module's rules do not reach the template, not that it is unchecked "
            "in every module - ask the others it belongs to as well."
            if rules
            else "No rule of this module version names a cell of this template. It may still be "
            "checked by another module the template belongs to; lookup_dpm_table lists them."
        ),
    }


LOOKUP_DPM_RULE_TOOL_NAME = "lookup_dpm_rule"

LOOKUP_DPM_RULE_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_RULE_TOOL_NAME,
        "description": (
            "What a validation rule code means - v0174_m, v23845_h, e23677_e. Use it to read a "
            "validation outcome, which names a code and a failing cell and nothing else: this "
            "returns the check itself, the cells it names, and one row per module version, each "
            "with its own severity and the first submission date it applies to. A code is not one "
            "rule: v0174_m is an error in COREP_OF 3.1.0 and a warning in 4.1.0, so an outcome "
            "means nothing until the module version it was raised under is known. A code pasted "
            "straight out of a report may carry the engine's occurrence number - v3775_s_62 is "
            "the 62nd application of v3775_s - which is stripped and reported back as occurrence."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "rule_code": {"type": "string", "description": "The rule code, e.g. v0174_m."},
            },
            "required": ["rule_code"],
            "additionalProperties": False,
        },
    },
}


LOOKUP_DPM_DATAPOINT_TOOL_NAME = "lookup_dpm_datapoint"
LOOKUP_DPM_PROPERTY_TOOL_NAME = "lookup_dpm_property"

LOOKUP_DPM_DATAPOINT_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_DATAPOINT_TOOL_NAME,
        "description": (
            "What a reported datapoint id is: the template, the cell, its row and column labels, "
            "and the module versions it belongs to. Use it to read an xBRL-CSV report, whose facts "
            "name a datapoint and nothing else - `dp1010005012` in a file means nothing until it "
            "is resolved here. An id the downloaded release does not have is answered with the "
            "highest it does, which says whether the file is from a newer release or the id is "
            "wrong."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "datapoint": {
                    "type": "string",
                    "description": "A datapoint id, with or without the prefix: dp1010005012 or 152217.",
                }
            },
            "required": ["datapoint"],
            "additionalProperties": False,
        },
    },
}

LOOKUP_DPM_PROPERTY_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_PROPERTY_TOOL_NAME,
        "description": (
            "What a column header of an xBRL-CSV report means. The columns after datapoint and "
            "factValue are the open dimensions, headed by a property code such as qGDF, qBBE, "
            "ei1452 or CPS, and this gives the property's name and the releases the code was "
            "current in. A code is release-scoped, so one that resolves to nothing usually means "
            "the file belongs to another release."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {"code": {"type": "string", "description": "The column header, e.g. qGDF or CPS."}},
            "required": ["code"],
            "additionalProperties": False,
        },
    },
}


LOOKUP_DPM_DIMENSIONS_TOOL_NAME = "lookup_dpm_dimensions"
LOOKUP_DPM_CELLS_TOOL_NAME = "lookup_dpm_cells"
# Every placing of a datapoint, release by release. The join is the same one every other
# answer here uses; what is different is that it is not scoped to one table version, which
# is the whole point - a datapoint that stayed put and a datapoint that moved look the
# same until you look across versions.
#
# The release range comes from the table version rather than from the variable version:
# the variable can outlive the layout that placed it, and what a reader is asking about is
# where it was reported, which is the layout.
_PLACINGS = """
SELECT   vv.VariableID              AS datapoint,
         c.VariableVID              AS variable_vid,
         tv.Code                    AS table_code,
         coalesce(hr.Code, '*')     AS row_code,
         trim(coalesce(hr.Label, '')) AS row_label,
         coalesce(hc.Code, '*')     AS column_code,
         trim(coalesce(hc.Label, '')) AS column_label,
         coalesce(hs.Code, '')      AS sheet_code,
         trim(coalesce(pi.Name, '')) AS metric,
         -- Resolved rather than compared as ids. ContextID differs between 99.5% of
         -- consecutive versions of the same variable, so an alarm on the id fires almost
         -- always and says nothing; what a reader needs to know is whether the members
         -- changed, and between 3.5 and 4.0 the EBA renamed dimensions wholesale while
         -- the members stayed exactly as they were.
         (SELECT string_agg(trim(d.Name) || '=' || trim(m.Name), '; ' ORDER BY trim(d.Name))
          FROM   ContextComposition x
          JOIN   Item m ON m.ItemID = x.ItemID
          JOIN   Item d ON d.ItemID = x.PropertyID
          WHERE  x.ContextID = vv.ContextID) AS context,
         (SELECT string_agg(trim(m.Name), '; ' ORDER BY trim(m.Name))
          FROM   ContextComposition x
          JOIN   Item m ON m.ItemID = x.ItemID
          WHERE  x.ContextID = vv.ContextID) AS members,
         rs.Code                    AS from_release,
         coalesce(re.Code, '')      AS to_release,
         tv.StartReleaseID          AS start_release_id
FROM     TableVersionCell c
JOIN     VariableVersion vv ON vv.VariableVID = c.VariableVID
JOIN     TableVersion tv ON tv.TableVID = c.TableVID
JOIN     Cell cc ON cc.CellID = c.CellID
LEFT JOIN Item pi ON pi.ItemID = vv.PropertyID
LEFT JOIN Release rs ON rs.ReleaseID = tv.StartReleaseID
LEFT JOIN Release re ON re.ReleaseID = tv.EndReleaseID
LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
LEFT JOIN TableVersionHeader tc ON tc.TableVID = c.TableVID AND tc.HeaderID = cc.ColumnID
LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
LEFT JOIN TableVersionHeader ts ON ts.TableVID = c.TableVID AND ts.HeaderID = cc.SheetID
LEFT JOIN HeaderVersion hs ON hs.HeaderVID = ts.HeaderVID
WHERE    c.IsExcluded = 0
"""

HISTORY_OF_DATAPOINT_SQL = f"""
SELECT * FROM ({_PLACINGS} AND vv.VariableID = ?)
ORDER BY start_release_id, table_code, row_code, column_code
"""

# Filtered outside the subquery because the coordinate is three coalesces, and a WHERE
# that repeats them is a WHERE that will disagree with the SELECT after the next edit.
HISTORY_AT_COORDINATE_SQL = f"""
SELECT * FROM ({_PLACINGS})
WHERE  table_code = ? AND row_code = ? AND column_code = ? AND sheet_code = ?
ORDER  BY start_release_id, datapoint
"""


def _place(row: dict[str, Any]) -> str:
    """A placing as one string, for comparing one release's to the next."""
    return cell_code(row["table_code"], row["row_code"], row["column_code"], row["sheet_code"])


def changes(placings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """What happened to a datapoint between releases, read off its placings.

    Derived rather than looked up: the DPM ships a ChangeLog table and it is empty in
    every release, so an account of what changed exists only as the difference between
    two versions. The categories are the ones the difference can actually support -

      introduced   the first release this datapoint was reported in
      moved        it left one cell and arrived in another
      added        reported in a further place, the old one kept
      removed      one place dropped, others kept
      relabelled   the same cell, a different wording - the description changed and the
                   datapoint did not, which is the case nobody notices
      respecified  different dimension members: the number means something else while
                   looking identical
      renamed      the same members under renamed dimensions, which is most of what looks
                   like a change between 3.5 and 4.0 and is not one
      remetricked  a different metric behind the cell
      withdrawn    the last placing ended and nothing followed

    A datapoint is reported by several templates at once - the .a/.b/.c variants of a
    template share them - so this compares a release against a release, not a row against
    the next row. Reading the rows in order instead turns being in four places into three
    moves, every release.
    """
    if not placings:
        return []
    order: list[str] = []
    by_release: dict[str, dict[str, dict[str, Any]]] = {}
    for row in sorted(placings, key=lambda row: (row["start_release_id"], row["table_code"], row["row_code"])):
        release = row["from_release"]
        if release not in by_release:
            by_release[release] = {}
            order.append(release)
        by_release[release][_place(row)] = row

    first = by_release[order[0]]
    found = [{"release": order[0], "kind": "introduced", "now": ", ".join(sorted(first))}]
    for earlier, later in zip(order, order[1:], strict=False):
        was, now = by_release[earlier], by_release[later]
        gone, arrived = sorted(set(was) - set(now)), sorted(set(now) - set(was))
        if gone and arrived:
            found.append({"release": later, "kind": "moved", "was": ", ".join(gone), "now": ", ".join(arrived)})
        elif arrived:
            found.append({"release": later, "kind": "added", "now": ", ".join(arrived)})
        elif gone:
            found.append({"release": later, "kind": "removed", "was": ", ".join(gone)})
        # Only where the cell is the same in both releases is a difference in its wording
        # or its members a change to that cell rather than a consequence of the move.
        for place in sorted(set(was) & set(now)):
            before, after = was[place], now[place]
            for kind, old, new in _differences(before, after):
                entry = {"release": later, "kind": kind, "was": old, "now": new, "at": place}
                # The same renaming lands on every cell of a template at once. Said once.
                if not any(seen.get(key) == entry[key] for seen in found for key in ("release", "kind", "was", "now")):
                    found.append(entry)
    last = max(placings, key=lambda row: row["start_release_id"])
    if last["to_release"] and not any(row["to_release"] == "" for row in placings):
        found.append({"release": last["to_release"], "kind": "withdrawn", "was": _place(last)})
    return found


def _differences(before: dict[str, Any], after: dict[str, Any]) -> list[tuple[str, str, str]]:
    """What differs between one release's version of a cell and the next's.

    Members are compared by their wording rather than by ItemID, which looks like the
    wrong way round and is not: the DPM reissues item ids between releases, so only 1 380
    of 150 558 consecutive version pairs keep the same ids, and comparing ids would call
    everything a change. The names are the stable part.
    """
    found = []
    if before["row_label"] != after["row_label"]:
        found.append(("relabelled", before["row_label"], after["row_label"]))
    if before["column_label"] != after["column_label"]:
        found.append(("relabelled", before["column_label"], after["column_label"]))
    if before["members"] != after["members"]:
        found.append(("respecified", before["context"] or "", after["context"] or ""))
    elif before["context"] != after["context"]:
        found.append(("renamed", before["context"] or "", after["context"] or ""))
    if before["metric"] != after["metric"]:
        found.append(("remetricked", before["metric"], after["metric"]))
    return found


def lookup_dpm_history(
    datapoint: str | int | None = None,
    table: str | None = None,
    row: str | None = None,
    column: str | None = None,
    sheet: str | None = None,
) -> dict[str, Any]:
    """What has happened to a datapoint, or to a coordinate, across every DPM release.

    Two ways in, because the model has two reference systems and they are not
    interchangeable. `datapoint` is the VariableID, which is an identity: it survives a
    template being relaid out. The coordinate - template, row, column, sheet - is an
    address, and an address is reused. Within one release a coordinate names exactly one
    datapoint; across releases 4 517 of 135 043 coordinates in DPM 4.4 have carried more
    than one. A time series keyed on `r0550_c0020` is keyed on the address.

    Asked by coordinate, the answer therefore says which datapoints have been there and
    not only what the current one did, because that is the question behind the question:
    whether a column of a warehouse table has always meant the same thing.
    """
    if not available():
        return {"found": False, "message": BUILD_IT}
    if datapoint is None and not table:
        return {
            "found": False,
            "message": (
                "Ask by datapoint - the VariableID, e.g. 152217 or dp152217 - or by coordinate: "
                "table with row and column. The first asks what became of a thing, the second "
                "what has been in a place."
            ),
        }

    if datapoint is not None:
        number = datapoint_id(datapoint)
        if number is None:
            return {
                "found": False,
                "datapoint": datapoint,
                "message": f"{datapoint!r} is not a datapoint id. They look like dp1010005012 or 152217.",
            }
        with _connect() as con:
            placings = _rows(con, HISTORY_OF_DATAPOINT_SQL, number)
        if not placings:
            return {
                "found": False,
                "datapoint": number,
                "message": (
                    f"No reportable cell has ever carried datapoint {number} in this release of the "
                    "DPM. lookup_dpm_datapoint says whether the id exists at all."
                ),
            }
        return {
            "found": True,
            "asked": {"datapoint": number},
            "datapoint": number,
            "placings": placings,
            "changes": changes(placings),
            "message": (
                "placings is where this datapoint was reported, release by release; changes is "
                "what differed between consecutive ones. The DPM ships no changelog - its "
                "ChangeLog table is empty in every release - so these are derived by comparing "
                "versions, not read from one."
            ),
        }

    try:
        with _connect() as con:
            # Through the resolver so that F1201A and F_12.01.a are the same question, and
            # so an unknown template is named as such rather than answered with nothing.
            found = _table_version(con, table or "")
            placings = _rows(
                con,
                HISTORY_AT_COORDINATE_SQL,
                found["Code"],
                row or "*",
                column or "*",
                sheet or "",
            )
    except DpmError as exc:
        return {"found": False, "table": table, "message": str(exc)}

    here = cell_code(found["Code"], row or "*", column or "*", sheet or "")
    if not placings:
        return {
            "found": False,
            "table": found["Code"],
            "message": (
                f"No reportable cell at {here} in any release. An open table's rows are '*' "
                "rather than a code, and a template with a sheet axis needs the sheet."
            ),
        }
    seen: dict[int, list[dict[str, Any]]] = {}
    for placing in placings:
        seen.setdefault(placing["datapoint"], []).append(placing)
    current = placings[-1]["datapoint"]
    return {
        "found": True,
        "asked": {"table": found["Code"], "row": row, "column": column, "sheet": sheet},
        "coordinate": here,
        "datapoints": [
            {
                "datapoint": number,
                "from_release": theirs[0]["from_release"],
                "to_release": theirs[-1]["to_release"],
                "row_label": theirs[-1]["row_label"],
                "column_label": theirs[-1]["column_label"],
                "current": number == current,
            }
            for number, theirs in seen.items()
        ],
        "reused": len(seen) > 1,
        "placings": placings,
        "changes": changes(seen[current]),
        "message": (
            f"{len(seen)} datapoint(s) have been reported at {here}. "
            + (
                "More than one, so this coordinate is not a stable key: a series keyed on it "
                "joins figures that are not the same quantity. Key on the datapoint instead."
                if len(seen) > 1
                else "One, so far - which is a fact about this coordinate and not a guarantee about the next release."
            )
        ),
    }


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
    "description": (
        "The module's own taxonomy version, such as 1.1.0 or 3.3.0 - not the DPM version. "
        "Null means the newest one that is actually reported under. Every answer reports both: "
        "taxonomy_version and dpm_release, the DPM version the module version belongs to (4.2 "
        "for FINREP9 3.3.0), which is what a reporting institution usually means by the version."
    ),
}

_RELEASE_ARG = {
    "type": ["string", "null"],
    "description": (
        "The DPM release, such as 4.2 or 4.4 - what a reporting institution usually means by "
        "the version. Resolves to whichever taxonomy version of the module that release shipped, "
        "which is the translation a caller cannot do alone. Pass this or version, never both. "
        "Null when neither is being pinned."
    ),
}


LOOKUP_DPM_RULES_TOOL_NAME = "lookup_dpm_rules"

LOOKUP_DPM_RULES_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_RULES_TOOL_NAME,
        "description": (
            "Every validation rule that reaches one template, with the rows and columns of it "
            "each one names. The reverse of lookup_dpm_rule, which starts from a code in a "
            "validation outcome; this starts from a template you are about to describe or "
            "report. Needs the module code, because the same template is checked differently "
            "depending on which return it is part of - C_01.00 has 50 rules in COREP_OF and 4 "
            "more in COREP_LE, a module it is not part of at all. Each rule lists every template "
            "it names, so a check reaching outside this one is visible as such."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "table": _TABLE_ARG,
                "module": {"type": "string", "description": "Module code, e.g. COREP_OF. Required here."},
                "version": _VERSION_ARG,
                "dpm_release": _RELEASE_ARG,
            },
            "required": ["table", "module", "version", "dpm_release"],
            "additionalProperties": False,
        },
    },
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
            "properties": {
                "table": _TABLE_ARG,
                "module": _MODULE_ARG,
                "version": _VERSION_ARG,
                "dpm_release": _RELEASE_ARG,
            },
            "required": ["table", "module", "version", "dpm_release"],
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
                "dpm_release": _RELEASE_ARG,
            },
            "required": ["table", "dimension", "member", "module", "version", "dpm_release"],
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
                "dpm_release": _RELEASE_ARG,
            },
            "required": ["table", "module", "version", "dpm_release"],
            "additionalProperties": False,
        },
    },
}

LOOKUP_DPM_HISTORY_TOOL_NAME = "lookup_dpm_history"

LOOKUP_DPM_HISTORY_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": LOOKUP_DPM_HISTORY_TOOL_NAME,
        "description": (
            "What has happened to a datapoint, or to a coordinate, across every DPM release the "
            "database carries - 3.4 to 4.4. Ask by datapoint (the VariableID, which is an "
            "identity) or by coordinate (template, row, column, which is an address). Returns "
            "where it was reported release by release and what differed between consecutive "
            "ones, classified: introduced, moved, relabelled (same cell, new wording - the "
            "description changed and the figure did not), respecified (different dimension "
            "members, so the number means something else while looking identical), renamed (the "
            "same members under renamed dimensions, which is most of what looks like a change "
            "between 3.5 and 4.0), remetricked, withdrawn. Asked by coordinate it also says "
            "whether more than one datapoint has ever been reported there, which is the question "
            "behind a time series keyed on a column name. The EBA ships no changelog - the DPM's "
            "ChangeLog table is empty in every release - so all of this is derived by comparing "
            "versions. Use it before telling anyone a column has always meant the same thing."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "datapoint": {
                    "type": ["string", "null"],
                    "description": (
                        "The datapoint id, e.g. 152217 or dp152217, to ask what became of one "
                        "thing. Null when asking by coordinate."
                    ),
                },
                "table": {
                    "type": ["string", "null"],
                    "description": "Template code, e.g. F_18.00.a, to ask what has been in one place.",
                },
                "row": {"type": ["string", "null"], "description": "Row code, four digits. '*' for an open table."},
                "column": {"type": ["string", "null"], "description": "Column code, four digits."},
                "sheet": {
                    "type": ["string", "null"],
                    "description": "Sheet code for a template with a sheet axis. Null otherwise.",
                },
            },
            "required": ["datapoint", "table", "row", "column", "sheet"],
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
    LOOKUP_DPM_DATAPOINT_TOOL_DEFINITION,
    LOOKUP_DPM_PROPERTY_TOOL_DEFINITION,
    LOOKUP_DPM_RULE_TOOL_DEFINITION,
    LOOKUP_DPM_RULES_TOOL_DEFINITION,
    LOOKUP_DPM_DIMENSIONS_TOOL_DEFINITION,
    LOOKUP_DPM_CELLS_TOOL_DEFINITION,
    LOOKUP_DPM_SUMS_TOOL_DEFINITION,
    LOOKUP_DPM_HISTORY_TOOL_DEFINITION,
)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    answer = lookup_dpm_table(args[0]) if len(args) == 1 else lookup_dpm_cell(*args[:4])
    print(json.dumps(answer, indent=2, default=str))
