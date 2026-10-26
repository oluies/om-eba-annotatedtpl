"""The queries a page about a template asks, as pure functions over a DuckDB connection.

Shared by both page builders - the Observable site in obs/ and the markdown Quarto
writes for the catalogue - so a number cannot mean one thing on a page and another in
the article about it. Separate from either of them on purpose. A notebook cell that holds a 20-line join is a join
nobody reviews: it is not imported by the tests, ruff does not see it, and the first
reader to need the same answer writes it again slightly differently. Here it is ordinary
Python, and the page is prose with calls in it.

Every function takes the connection and returns rows - no module state, no open database
at import time - so the same functions answer for 4.2.1 and for 4.4 by being handed a
different file.

The joins are the ones `dpm_lookup.py` already uses: TableVersionCell carries the
VariableVID, Cell carries the row, column and sheet header ids, and TableVersionHeader
resolves those against the table version that is being asked about. A header resolved
without naming the table version is a header from some other version of the table.
"""

from __future__ import annotations

import csv
import os
import urllib.parse
from pathlib import Path
from typing import Any

import duckdb

# The rows this page shows are read, never written, and a read-only connection is also
# the only way two renders can run against one file at the same time.
# Quarto runs the kernel in the directory of the .qmd, not at the repository root, so a
# relative default resolves against quarto/ and finds nothing. Anchored on this file
# instead, which is next to the pages and one level below the database wherever the
# checkout happens to be.
HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE / "dpm2" / "dpm2_4_4.duckdb"


def connect(db: str | os.PathLike[str] | None = None) -> duckdb.DuckDBPyConnection:
    """Open the DPM database for reading, defaulting to the one `env.sh` points at."""
    asked = db or os.environ.get("DPM2_DB")
    path = Path(asked) if asked else DEFAULT_DB
    if not path.exists():
        raise SystemExit(
            f"{path} is not there. Build it with `uv run source/fetch_dpm2.py --release 4.4`,\n"
            "or point DPM2_DB at a database you already have."
        )
    return duckdb.connect(str(path), read_only=True)


def rows(con: duckdb.DuckDBPyConnection, sql: str, *args: Any) -> list[dict[str, Any]]:
    """A query's answer as dicts, which is what the page renders."""
    cursor = con.execute(sql, list(args))
    names = [column[0] for column in cursor.description or []]
    return [dict(zip(names, row, strict=True)) for row in cursor.fetchall()]


def one(con: duckdb.DuckDBPyConnection, sql: str, *args: Any) -> dict[str, Any]:
    """The first row, or an empty dict. For the counts a sentence is built from."""
    found = rows(con, sql, *args)
    return found[0] if found else {}


RELEASES = """
SELECT ReleaseID AS release_id, Code AS code
FROM   Release
ORDER  BY ReleaseID
"""


def releases(con: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    """Every release this database knows, oldest first.

    The ids are not ordered the way the codes are - 4.2.1 is 1010000003 and 4.2 is 5 -
    so anything that sorts releases sorts by ReleaseID and shows the Code.
    """
    return rows(con, RELEASES)


# A template belongs to a framework through the module versions that compose it, not
# directly: the same join gen_wasm_data.py partitions by. A template in two frameworks -
# some are - is listed under both, which is what a reader looking for it expects.
FRAMEWORKS = """
SELECT   f.Code AS framework, f.Name AS name, count(DISTINCT tv.Code) AS templates
FROM     TableVersion tv
JOIN     ModuleVersionComposition mvc ON mvc.TableVID = tv.TableVID
JOIN     ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
JOIN     Module m ON m.ModuleID = mv.ModuleID
JOIN     Framework f ON f.FrameworkID = m.FrameworkID
GROUP BY f.Code, f.Name
ORDER BY templates DESC
"""


def frameworks(con: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    """Every framework in the database, largest first."""
    return rows(con, FRAMEWORKS)


TEMPLATES_OF = """
SELECT   tv.Code AS table_code,
         -- The name as the version in force has it, not max() over every version: the
         -- index and the page it links to disagreeing about a template's name is the
         -- kind of small wrongness that makes a reader doubt the rest.
         arg_max(tv.Name, tv.StartReleaseID) AS name,
         arg_max(tv.TableVID, tv.StartReleaseID) AS table_vid
FROM     TableVersion tv
JOIN     ModuleVersionComposition mvc ON mvc.TableVID = tv.TableVID
JOIN     ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
JOIN     Module m ON m.ModuleID = mv.ModuleID
JOIN     Framework f ON f.FrameworkID = m.FrameworkID
WHERE    f.Code = ?
     AND EXISTS (SELECT 1 FROM TableVersionCell c
                 WHERE c.TableVID = tv.TableVID AND c.IsExcluded = 0)
GROUP BY tv.Code
ORDER BY tv.Code
"""


def templates_of(con: duckdb.DuckDBPyConnection, framework: str) -> list[dict[str, Any]]:
    """The templates of one framework that have reportable cells.

    The EXISTS is not tidiness: a template version with every cell excluded is a layout
    the EBA publishes and nobody files, and a page for it would say 0 cells, 0 dimensions
    and nothing else.
    """
    return rows(con, TEMPLATES_OF, framework)


VERSIONS = """
SELECT tv.TableVID       AS table_vid,
       tv.Code           AS code,
       tv.Name           AS name,
       rs.Code           AS from_release,
       coalesce(re.Code, '-') AS to_release,
       tv.StartReleaseID AS start_release_id
FROM   TableVersion tv
LEFT JOIN Release rs ON rs.ReleaseID = tv.StartReleaseID
LEFT JOIN Release re ON re.ReleaseID = tv.EndReleaseID
WHERE  tv.Code = ?
ORDER  BY tv.StartReleaseID
"""


def versions(con: duckdb.DuckDBPyConnection, table_code: str) -> list[dict[str, Any]]:
    """Every version of one template, with the releases each was current for.

    `to_release` is the release the version stopped at, and '-' means it is the one in
    force: EndReleaseID is NULL for the current version, not for a withdrawn one.
    """
    return rows(con, VERSIONS, table_code)


# The coordinates of one table version, with the labels that make up a description.
# IsExcluded is the greyed-out cell of an annotated layout: it is in the grid and is not
# reported, so counting it as a datapoint overstates every total on the page.
CELLS = """
SELECT   c.CellCode                AS cell_code,
         vv.VariableID             AS variable_id,
         c.VariableVID             AS variable_vid,
         coalesce(hr.Code, '*')    AS row_code,
         trim(coalesce(hr.Label, '')) AS row_label,
         coalesce(hc.Code, '*')    AS column_code,
         trim(coalesce(hc.Label, '')) AS column_label,
         coalesce(hs.Code, '')     AS sheet_code
FROM     TableVersionCell c
JOIN     VariableVersion vv ON vv.VariableVID = c.VariableVID
JOIN     Cell cc ON cc.CellID = c.CellID
LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
LEFT JOIN TableVersionHeader tc ON tc.TableVID = c.TableVID AND tc.HeaderID = cc.ColumnID
LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
LEFT JOIN TableVersionHeader ts ON ts.TableVID = c.TableVID AND ts.HeaderID = cc.SheetID
LEFT JOIN HeaderVersion hs ON hs.HeaderVID = ts.HeaderVID
WHERE    c.TableVID = ? AND c.IsExcluded = 0
ORDER    BY row_code, column_code, sheet_code
"""


def cells(con: duckdb.DuckDBPyConnection, table_vid: int) -> list[dict[str, Any]]:
    """The reportable cells of one table version."""
    return rows(con, CELLS, table_vid)


DIMENSIONS = """
SELECT   trim(dim.Name) AS dimension,
         count(DISTINCT trim(i.Name)) AS members,
         string_agg(DISTINCT trim(i.Name), ', ' ORDER BY trim(i.Name)) AS wording
FROM     TableVersionCell c
JOIN     VariableVersion vv ON vv.VariableVID = c.VariableVID
JOIN     ContextComposition x ON x.ContextID = vv.ContextID
JOIN     Item i ON i.ItemID = x.ItemID
JOIN     Item dim ON dim.ItemID = x.PropertyID
WHERE    c.TableVID = ? AND c.IsExcluded = 0
GROUP BY trim(dim.Name)
ORDER BY trim(dim.Name)
"""


def dimensions(con: duckdb.DuckDBPyConnection, table_vid: int) -> list[dict[str, Any]]:
    """What the template breaks down by, and in whose wording.

    trim on both sides because the model holds "Credit institutions" and "Credit
    institutions " as separate items, differing by a trailing space. A reader copying a
    member out of a listing should not have to copy the space too.
    """
    return rows(con, DIMENSIONS, table_vid)


# The Official Journal's own Swedish and German, where source/fetch_its_labels.py has
# collected them. Absent is the normal case for most frameworks, so a page says so rather
# than leaving a gap a reader reads as "no translation exists".
OFFICIAL = HERE / "its_labels.csv"


INSTRUCTIONS = HERE / "its_instructions.csv"


def keyed(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    """A three-language CSV keyed on template and row, or empty if it is not collected."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return {(row["template"], row["row"]): row for row in csv.DictReader(handle)}


def official(path: Path | None = None) -> dict[tuple[str, str], dict[str, str]]:
    """Published translations of the row labels - what a row is called."""
    return keyed(path or OFFICIAL)


CHANGES = HERE / "its_label_changes.csv"


def reworded(path: Path | None = None) -> dict[tuple[str, str], list[dict[str, str]]]:
    """Rows the consolidations of the regulation word differently, oldest first.

    Sixteen templates of 165 have any, which is why this is a note on the rows that have
    one rather than a control offering a version: a selector that shows the same thing on
    149 pages teaches a reader that it never matters.
    """
    here = path or CHANGES
    if not here.exists():
        return {}
    import csv as _csv

    out: dict[tuple[str, str], list[dict[str, str]]] = {}
    with here.open(encoding="utf-8") as handle:
        for row in _csv.DictReader(handle):
            out.setdefault((row["template"], row["row"]), []).append(row)
    return out


def instructions(path: Path | None = None) -> dict[tuple[str, str], dict[str, str]]:
    """The instructions annex's prose - what a row means, and which article requires it.

    A different thing from a label, and the more useful one for a description: `1. Own
    funds Point (118) of Article 4(1) and Article 72 CRR The own funds of an institution
    shall be the sum of Tier 1 capital and Tier 2 capital.` - in Swedish and German too.
    """
    return keyed(path or INSTRUCTIONS)


def described(cell: dict[str, Any], table_name: str) -> str:
    """The description, composed.

    There is nothing to copy: `VariableVersion.Name` is NULL for all 299 573 rows in DPM
    4.4 and `Code` is set for 745 of them, so every tool that shows a description for a
    datapoint - this one, and the supervisory portals - builds it out of the table, the
    row and the column. Writing it in one place means the pack, the page and the
    catalogue say the same sentence.
    """
    parts = [table_name, f"Row: {cell['row_code']} - {cell['row_label']}"]
    parts.append(f"Column: {cell['column_code']} - {cell['column_label']}")
    if cell["sheet_code"]:
        parts.append(f"Sheet: {cell['sheet_code']}")
    return " / ".join(part for part in parts if part)


# Where one variable has sat, across every version of every table. The question behind
# "is a coordinate a safe key": it is not, if the same coordinate has carried more than
# one variable, and this is what says whether that happened here.
COORDINATES = """
SELECT   vv.VariableID          AS variable_id,
         tv.Code                AS table_code,
         coalesce(hr.Code, '*') AS row_code,
         coalesce(hc.Code, '*') AS column_code,
         coalesce(hs.Code, '')  AS sheet_code,
         rs.Code                AS from_release,
         tv.StartReleaseID      AS start_release_id
FROM     TableVersionCell c
JOIN     VariableVersion vv ON vv.VariableVID = c.VariableVID
JOIN     TableVersion tv ON tv.TableVID = c.TableVID
JOIN     Cell cc ON cc.CellID = c.CellID
LEFT JOIN Release rs ON rs.ReleaseID = tv.StartReleaseID
LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
LEFT JOIN TableVersionHeader tc ON tc.TableVID = c.TableVID AND tc.HeaderID = cc.ColumnID
LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
LEFT JOIN TableVersionHeader ts ON ts.TableVID = c.TableVID AND ts.HeaderID = cc.SheetID
LEFT JOIN HeaderVersion hs ON hs.HeaderVID = ts.HeaderVID
WHERE    c.IsExcluded = 0
     AND vv.VariableID IN (SELECT vv2.VariableID
                           FROM   TableVersionCell c2
                           JOIN   VariableVersion vv2 ON vv2.VariableVID = c2.VariableVID
                           WHERE  c2.TableVID = ? AND c2.IsExcluded = 0)
ORDER    BY variable_id, start_release_id
"""


def coordinates(con: duckdb.DuckDBPyConnection, table_vid: int) -> list[dict[str, Any]]:
    """Every coordinate ever held by the variables this table version reports."""
    return rows(con, COORDINATES, table_vid)


MOVED = """
WITH here AS (
  SELECT DISTINCT vv.VariableID
  FROM   TableVersionCell c
  JOIN   VariableVersion vv ON vv.VariableVID = c.VariableVID
  WHERE  c.TableVID = ? AND c.IsExcluded = 0
),
seen AS (
  SELECT vv.VariableID,
         tv.Code AS table_code,
         'r' || coalesce(hr.Code, '*') || ' c' || coalesce(hc.Code, '*') AS place
  FROM   TableVersionCell c
  JOIN   VariableVersion vv ON vv.VariableVID = c.VariableVID
  JOIN   here USING (VariableID)
  JOIN   TableVersion tv ON tv.TableVID = c.TableVID
  JOIN   Cell cc ON cc.CellID = c.CellID
  LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
  LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
  LEFT JOIN TableVersionHeader tc ON tc.TableVID = c.TableVID AND tc.HeaderID = cc.ColumnID
  LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
  WHERE  c.IsExcluded = 0
),
per AS (
  SELECT VariableID,
         count(DISTINCT place)      AS places,
         count(DISTINCT table_code) AS templates
  FROM   seen
  GROUP  BY VariableID
)
-- coalesce because sum() over no rows is NULL, not 0, and a template whose datapoints
-- are placed nowhere else renders "**{None:,} have sat at another row or column**",
-- which fails the whole build with a TypeError two hundred pages in.
SELECT count(*)                                  AS variables,
       coalesce(sum((places > 1)::INT), 0)       AS moved,
       coalesce(sum((templates > 1)::INT), 0)    AS shared
FROM   per
"""


def moved(con: duckdb.DuckDBPyConnection, table_vid: int) -> dict[str, Any]:
    """Where this version's datapoints have been, in two different senses.

    `moved` is a datapoint that has sat at more than one row/column. `shared` is one that
    appears in more than one template - the .a/.b/.c variants of a template report the
    same datapoints, so that is a property of the layout rather than a change over time.
    Reported apart because adding them together produces the useless claim that every
    datapoint in a variant template has moved.
    """
    return one(con, MOVED, table_vid)


RELABELLED = """
SELECT   h.HeaderID        AS header_id,
         hv.Code           AS code,
         trim(hv.Label)    AS label,
         rs.Code           AS from_release,
         coalesce(re.Code, '-') AS to_release
FROM     TableVersionHeader h
JOIN     HeaderVersion hv ON hv.HeaderID = h.HeaderID
LEFT JOIN Release rs ON rs.ReleaseID = hv.StartReleaseID
LEFT JOIN Release re ON re.ReleaseID = hv.EndReleaseID
WHERE    h.TableVID = ?
     AND h.HeaderID IN (SELECT HeaderID
                        FROM   HeaderVersion
                        GROUP  BY HeaderID
                        HAVING count(DISTINCT trim(Label)) > 1)
ORDER    BY hv.Code, hv.StartReleaseID
"""


def relabelled(con: duckdb.DuckDBPyConnection, table_vid: int) -> list[dict[str, Any]]:
    """Rows and columns of this table whose wording changed between releases.

    This is the history the description has: the coordinate and the datapoint stayed, the
    sentence a reader is shown did not. The EBA ships no account of it - the ChangeLog
    table is present and empty in every release - so it is read off the versions.
    """
    return rows(con, RELABELLED, table_vid)


# The rules reaching a template. OperandReferenceLocation holds the template, row and
# column each leaf of an expression resolved to, so this is a join and not a parse of the
# DPM-XL - the EBA has already done the resolving.
RULES = """
SELECT   o.Code           AS rule_code,
         os.Severity      AS severity,
         os.IsActive <> 0 AS active,
         count(DISTINCT coalesce(l."Row", '*')) AS rows_here
FROM     OperandReferenceLocation l
JOIN     OperandReference r ON r.OperandReferenceID = l.OperandReferenceID
JOIN     OperationNode n ON n.NodeID = r.NodeID
JOIN     OperationVersion ov ON ov.OperationVID = n.OperationVID
JOIN     Operation o ON o.OperationID = ov.OperationID
JOIN     OperationScope os ON os.OperationVID = ov.OperationVID
WHERE    l."Table" = ?
GROUP BY rule_code, severity, active
ORDER BY rule_code
"""


def rules(con: duckdb.DuckDBPyConnection, table_code: str) -> list[dict[str, Any]]:
    """The validation rules that reach any cell of this template.

    Keyed on the template code rather than a table version: a rule names a coordinate,
    not a version, which is the same reason a coordinate is an unsafe key over time.
    `active` is the EBA's deactivated-rules list - a description that names a rule nobody
    runs is worse than one that names none.
    """
    return rows(con, RULES, table_code)


# The query page answers a rule code, and the release is in its query string, so a link
# is to the rule as that release had it. That matters: 2005 of 7514 consecutive version
# pairs change what the rule checks, so a code without a release is not a statement.
PAGE = "https://oluies.github.io/om-eba-annotatedtpl/"


def rule_link(rule_code: str, release: str = "") -> str:
    """A markdown link from a rule code to the page that explains it."""
    query = urllib.parse.urlencode({"q": "rule", "rule_code": rule_code} | ({"release": release} if release else {}))
    return f"[{rule_code}]({PAGE}?{query})"


def markdown_table(records: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    """Rows as a GFM table, which both HTML and the catalogue render.

    Written out rather than taken from pandas: the page has to produce markdown that
    OpenMetadata accepts, and a DataFrame's repr is HTML in one output format and a
    fixed-width block in the other.
    """
    if not records:
        return "_nothing to show_"
    names = columns or list(records[0])
    header = "| " + " | ".join(names) + " |"
    rule = "|" + "|".join("---" for _ in names) + "|"
    body = [
        "| " + " | ".join(str(record.get(name, "")).replace("|", "\\|") for name in names) + " |" for record in records
    ]
    return "\n".join([header, rule, *body])
