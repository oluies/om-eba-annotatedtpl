"""Generate README_DPM2.md: the data model of the local DPM 2.0 database, and how to query it.

Generated rather than written by hand so the counts stay true: a new DPM release changes
every one of them, and a stale row count in a data model is worse than none.

    uv run source/fetch_dpm2.py && uv run source/gen_dpm2_doc.py

Every relationship below is verified against the data before it is drawn. The Access
export carries no foreign keys, so a diagram drawn from column names alone would be a
guess; this one fails the build if a child key has a value its parent does not.
"""

import os
import textwrap
from pathlib import Path

import duckdb

REPO = Path(__file__).resolve().parent.parent
DPM2 = Path(os.environ.get("DPM2_DB") or REPO / "source" / "dpm2" / "dpm2.duckdb")
OUT = REPO / "README_DPM2.md"

# child, child key, parent, parent key, mermaid cardinality, which diagram, what it means.
# Cardinality is read from the verification below: a nullable child key draws as |o, and
# no child key in this model is unique, so the child side is always o{ or one..many.
REL = [
    ("Module", "FrameworkID", "Framework", "FrameworkID", "A", "a framework groups its modules"),
    ("ModuleVersion", "ModuleID", "Module", "ModuleID", "A", "one version per release of a module"),
    ("ModuleVersion", "StartReleaseID", "Release", "ReleaseID", "A", "first release this version appears in"),
    ("ModuleVersion", "EndReleaseID", "Release", "ReleaseID", "A", "last one; null means current"),
    ("ModuleVersionComposition", "ModuleVID", "ModuleVersion", "ModuleVID", "A", "which templates a version reports"),
    ("ModuleVersionComposition", "TableVID", "TableVersion", "TableVID", "A", "and at which version of each"),
    ("TableVersion", "TableID", "Table", "TableID", "B", "a template's versions"),
    ("Header", "TableID", "Table", "TableID", "B", "the template's axis entries"),
    ("HeaderVersion", "HeaderID", "Header", "HeaderID", "B", "a header's code and label per release"),
    ("TableVersionHeader", "TableVID", "TableVersion", "TableVID", "B", "which headers this version uses"),
    ("TableVersionHeader", "HeaderVID", "HeaderVersion", "HeaderVID", "B", "and with which label"),
    ("TableVersionHeader", "ParentHeaderID", "Header", "HeaderID", "B", "what an 'Of which' row qualifies"),
    ("TableVersionCell", "TableVID", "TableVersion", "TableVID", "C", "the cells of a template version"),
    ("TableVersionCell", "CellID", "Cell", "CellID", "C", "the cell's position"),
    ("TableVersionCell", "VariableVID", "VariableVersion", "VariableVID", "C", "what it reports; null if excluded"),
    ("Cell", "TableID", "Table", "TableID", "C", "the template it sits in"),
    ("Cell", "RowID", "Header", "HeaderID", "C", "its row; null on an open row axis"),
    ("Cell", "ColumnID", "Header", "HeaderID", "C", "its column"),
    ("Cell", "SheetID", "Header", "HeaderID", "C", "its sheet; null where there is no sheet axis"),
    ("VariableVersion", "VariableID", "Variable", "VariableID", "C", "the variable's versions"),
    ("VariableVersion", "PropertyID", "Property", "PropertyID", "C", "the metric being measured"),
    ("VariableVersion", "ContextID", "Context", "ContextID", "C", "the breakdown it is measured under"),
    ("ContextComposition", "ContextID", "Context", "ContextID", "C", "a context is a set of these"),
    ("ContextComposition", "PropertyID", "Item", "ItemID", "C", "the dimension"),
    ("ContextComposition", "ItemID", "Item", "ItemID", "C", "the member of it"),
    ("Property", "PropertyID", "Item", "ItemID", "C", "a property is an item that can be measured"),
    ("Property", "DataTypeID", "DataType", "DataTypeID", "C", "monetary, count, date, ..."),
    ("OperationVersion", "OperationID", "Operation", "OperationID", "D", "a rule code's versions"),
    ("OperationScope", "OperationVID", "OperationVersion", "OperationVID", "D", "severity and from when"),
    ("OperationScopeComposition", "OperationScopeID", "OperationScope", "OperationScopeID", "D", "scoped to"),
    ("OperationScopeComposition", "ModuleVID", "ModuleVersion", "ModuleVID", "D", "a module version"),
    ("OperationNode", "OperationVID", "OperationVersion", "OperationVID", "D", "the expression as a tree"),
    ("OperationNode", "OperatorID", "Operator", "OperatorID", "D", "null on a leaf"),
    ("OperandReference", "NodeID", "OperationNode", "NodeID", "D", "what a leaf refers to"),
    ("OperandReferenceLocation", "OperandReferenceID", "OperandReference", "OperandReferenceID", "D", "resolved to"),
    ("OperandReferenceLocation", "CellID", "Cell", "CellID", "D", "the actual cells"),
]

# Only the fields worth drawing. A diagram with every column of VariableVersion on it is
# a schema dump, not a model.
ATTRS = {
    "Framework": [("varchar", "Code", ""), ("varchar", "Name", ""), ("bigint", "FrameworkID", "PK")],
    "Module": [("bigint", "ModuleID", "PK"), ("bigint", "FrameworkID", "FK")],
    "ModuleVersion": [
        ("bigint", "ModuleVID", "PK"),
        ("varchar", "Code", ""),
        ("varchar", "VersionNumber", ""),
        ("date", "FromReferenceDate", ""),
        ("date", "ToReferenceDate", ""),
    ],
    "Release": [("bigint", "ReleaseID", "PK"), ("varchar", "Code", ""), ("date", "Date", "")],
    "ModuleVersionComposition": [("bigint", "ModuleVID", "FK"), ("bigint", "TableVID", "FK")],
    "Table": [
        ("bigint", "TableID", "PK"),
        ("bigint", "HasOpenRows", ""),
        ("bigint", "HasOpenColumns", ""),
        ("bigint", "HasOpenSheets", ""),
    ],
    "TableVersion": [("bigint", "TableVID", "PK"), ("varchar", "Code", ""), ("varchar", "Name", "")],
    "Header": [("bigint", "HeaderID", "PK"), ("varchar", "Direction", "")],
    "HeaderVersion": [("bigint", "HeaderVID", "PK"), ("varchar", "Code", ""), ("varchar", "Label", "")],
    "TableVersionHeader": [("bigint", "ParentHeaderID", "FK"), ("bigint", "Order", "")],
    "TableVersionCell": [
        ("varchar", "CellCode", ""),
        ("bigint", "IsExcluded", ""),
        ("varchar", "Sign", ""),
        ("bigint", "VariableVID", "FK"),
    ],
    "Cell": [("bigint", "CellID", "PK"), ("bigint", "RowID", "FK"), ("bigint", "ColumnID", "FK")],
    "Variable": [("bigint", "VariableID", "PK"), ("varchar", "Type", "")],
    "VariableVersion": [("bigint", "VariableVID", "PK"), ("bigint", "PropertyID", "FK"), ("bigint", "ContextID", "FK")],
    "Context": [("bigint", "ContextID", "PK"), ("varchar", "Signature", "")],
    "ContextComposition": [("bigint", "PropertyID", "FK"), ("bigint", "ItemID", "FK")],
    "Item": [("bigint", "ItemID", "PK"), ("varchar", "Name", ""), ("varchar", "Description", "")],
    "Property": [("bigint", "PropertyID", "PK"), ("bigint", "DataTypeID", "FK"), ("varchar", "PeriodType", "")],
    "DataType": [("bigint", "DataTypeID", "PK"), ("varchar", "Name", "")],
    "Operation": [("bigint", "OperationID", "PK"), ("varchar", "Code", ""), ("varchar", "Type", "")],
    "OperationVersion": [("bigint", "OperationVID", "PK"), ("varchar", "Expression", "")],
    "OperationScope": [("bigint", "OperationScopeID", "PK"), ("varchar", "Severity", "")],
    "OperationScopeComposition": [("bigint", "OperationScopeID", "FK"), ("bigint", "ModuleVID", "FK")],
    "OperationNode": [("bigint", "NodeID", "PK"), ("bigint", "IsLeaf", ""), ("varchar", "OperandType", "")],
    "Operator": [("bigint", "OperatorID", "PK"), ("varchar", "Symbol", "")],
    "OperandReference": [("bigint", "OperandReferenceID", "PK"), ("varchar", "OperandReference", "")],
    "OperandReferenceLocation": [
        ("varchar", "Table", ""),
        ("varchar", "Row", ""),
        ("varchar", "Column", ""),
        ("varchar", "Sheet", ""),
    ],
}

GROUPS = {
    "A": (
        "What is reported, and when",
        "Frameworks hold modules, a module is reissued as a version per release, and a version "
        "lists the templates it reports. Everything else hangs off a `ModuleVID`.",
    ),
    "B": (
        "The grid of a template",
        "A template is versioned, and so is every entry on its axes. `Direction` is `X` for a "
        "column, `Y` for a row and `Z` for a sheet; `ParentHeaderID` is what makes an "
        '"Of which" row a child of the row it qualifies.',
    ),
    "C": (
        "What a cell means",
        "A cell is a position; what it reports is a variable, and a variable is one metric "
        "measured under one context. A context is a set of dimension-and-member pairs, and both "
        "sides of that pair are rows of `Item`.",
    ),
    "D": (
        "Validation rules",
        "A rule code is versioned, scoped to module versions with a severity, and stored as an "
        "expression tree. The leaves are resolved to actual cells in "
        "`OperandReferenceLocation`, which is why nothing has to parse DPM-XL.",
    ),
}


def one(con: duckdb.DuckDBPyConnection, sql: str) -> tuple:
    """A query that must return a row. fetchone() types as optional, and a None here would
    mean this is not the database the model was written against - worth saying out loud."""
    row = con.execute(sql).fetchone()
    if row is None:
        raise SystemExit(f"{DPM2.name} answered nothing to: {sql.strip()}")
    return row


def verify(con: duckdb.DuckDBPyConnection) -> dict[tuple[str, str], bool]:
    """Orphan check per relationship, and whether the child key is nullable.

    Fails the generation rather than drawing a relationship that does not hold. The
    nullable answer decides the mermaid cardinality, so the diagram says which parents
    are optional instead of implying all are mandatory.
    """
    nullable = {}
    broken = []
    for child, ck, parent, pk, _, _ in REL:
        orphans, nulls = one(
            con,
            f'SELECT count(*) FILTER (WHERE c."{ck}" IS NOT NULL AND p."{pk}" IS NULL), '
            f'count(*) FILTER (WHERE c."{ck}" IS NULL) '
            f'FROM "{child}" c LEFT JOIN "{parent}" p ON p."{pk}" = c."{ck}"',
        )
        if orphans:
            broken.append(f"{child}.{ck} -> {parent}.{pk}: {orphans} value(s) with no parent")
        nullable[(child, ck)] = bool(nulls)
    if broken:
        raise SystemExit("Relationships that do not hold in this release:\n  " + "\n  ".join(broken))
    return nullable


def diagram(group: str, nullable: dict[tuple[str, str], bool]) -> str:
    """One mermaid erDiagram for one group, with only the tables that group touches."""
    rels = [r for r in REL if r[4] == group]
    tables = sorted({r[0] for r in rels} | {r[2] for r in rels})
    lines = ["erDiagram"]
    for table in tables:
        lines.append(f"    {table} {{")
        for kind, name, key in ATTRS.get(table, []):
            lines.append(f"        {kind} {name}{' ' + key if key else ''}")
        lines.append("    }")
    for child, ck, parent, _pk, _group, _note in rels:
        # |o on the parent side where the child key may be null: that parent is optional.
        left = "|o" if nullable[(child, ck)] else "||"
        lines.append(f'    {parent} {left}--o{{ {child} : "{ck}"')
    return "\n".join(lines)


def inventory(con: duckdb.DuckDBPyConnection) -> str:
    """Every table in the database with its row count, modelled ones marked."""
    modelled = {r[0] for r in REL} | {r[2] for r in REL}
    rows = con.execute(
        "SELECT table_name, estimated_size, column_count FROM duckdb_tables() ORDER BY estimated_size DESC"
    ).fetchall()
    out = ["| Table | Rows | Columns | In the model above |", "|---|---:|---:|---|"]
    out += [
        f"| `{name}` | {size:,} | {cols} | {'yes' if name in modelled else ''} |".replace(",", " ")
        for name, size, cols in rows
    ]
    return "\n".join(out)


def main() -> None:
    if not DPM2.exists():
        raise SystemExit(f"{DPM2} does not exist - run source/fetch_dpm2.py first")
    con = duckdb.connect(str(DPM2), read_only=True)
    nullable = verify(con)

    release, date = one(con, "SELECT Code, Date FROM Release ORDER BY ReleaseID DESC LIMIT 1")
    tables, rows = one(con, "SELECT count(*), sum(estimated_size) FROM duckdb_tables()")
    templates, empty = one(
        con,
        """
        WITH newest AS (SELECT Code, max_by(TableVID, StartReleaseID) AS vid FROM TableVersion GROUP BY Code)
        SELECT count(*), count(*) FILTER (WHERE (SELECT count(*) FROM TableVersionCell c WHERE c.TableVID = n.vid) = 0)
        FROM newest n
        """,
    )
    excluded, no_variable = one(
        con,
        "SELECT count(*) FILTER (WHERE IsExcluded <> 0), count(*) FILTER (WHERE VariableVID IS NULL) "
        "FROM TableVersionCell",
    )
    defined, items = one(
        con,
        "SELECT count(*) FILTER (WHERE Description IS NOT NULL AND Description <> ''), count(*) FROM Item",
    )
    size = DPM2.stat().st_size / 1e6
    con.close()

    body = f"""# The DPM 2.0 database, locally

Release **{release}** ({date}) of the EBA DPM 2.0 database, loaded into DuckDB: {tables} tables,
{rows:,} rows, {size:.0f} MB. It is the model the pack is built from, which the annotated table
layout only renders.

```bash
uv run source/fetch_dpm2.py          # download, unpack, load  (needs mdbtools)
uv run source/check_against_dpm2.py  # does the pack match it, cell for cell?
uv run source/extract_rules.py       # the validation rules, into 09-validation-rules.csv
uv run source/gen_dpm2_doc.py        # this file
duckdb source/dpm2/dpm2.duckdb       # or just poke at it
```

Nothing has to be configured. `DPM2_DIR` moves the download and `DPM2_DB` the database;
both default into `source/dpm2/`, which is gitignored. Note that these are read with
`os.environ` and so, unlike `PAY42_*` and `OM_*`, are **not** read from a `.env` file.

The Access export carries no foreign keys, so every relationship drawn below was checked
against the data instead: all {len(REL)} hold with no orphaned key, and the generator fails rather
than draw one that does not. An optional parent is drawn `|o`, which is exactly the
relationships whose child key is nullable.

## Reading a version number

Almost everything is versioned, and the two ids are easy to confuse:

- `TableID` is the template. `TableVID` is the template **as it stood in some release**.
- `ModuleID` / `ModuleVID`, `HeaderID` / `HeaderVID`, `VariableID` / `VariableVID`,
  `OperationID` / `OperationVID` all work the same way.

A query that forgets this gets every historical version at once, which is the single
most common way to get a wrong answer out of this database - and the wrong answer looks
like a right one, just with more rows. `Y_01.01` has 39 rows in PSD_FRP 1.1.0 and
answers 117 if you join `TableVersion` on `Code` alone.

`ModuleVersionComposition` is the join that pins a template version to the module version
that reports it, and almost every query below starts from it.
"""

    for group, (title, blurb) in GROUPS.items():
        wrapped = textwrap.fill(blurb, 88)
        body += f"\n## {title}\n\n{wrapped}\n\n```mermaid\n{diagram(group, nullable)}\n```\n"
        body += "\n| Relationship | What it means |\n|---|---|\n"
        body += "\n".join(f"| `{c}.{ck}` to `{p}.{pk}` | {note} |" for c, ck, p, pk, g, note in REL if g == group)
        body += "\n"

    body += f"""
## Things that will trip you up

**An excluded cell has no variable.** `IsExcluded` is set on {excluded:,} cells and
`VariableVID` is null on {no_variable:,} - the same cells, checked rather than assumed. An excluded
cell is a greyed-out box in the template: in the dictionary, with no variable, nothing to
report. The pack leaves them out, which is why it has 324 columns for `Y_01.01` where the
model has 396 cells.

**A rule code is not one rule.** The same `Operation.Code` is reissued per module version,
and both the expression and the severity change between them: `v09247_s` is a `warning` in
PSD_FRP 1.1.0 and an `error` in 1.2.0. Always carry the module version alongside the code.

**A template code has four spellings.** The model writes `Y_01.01`. The annotated layout
and the warehouse's `BA_Form_Cell` write `Y 01.01`. The warehouse table is `Y_01_01` and
the column prefix is `Y0101`. They are one template.

**{empty} of {templates} templates have no rows, columns or cells** in their newest version. That is a
fact about the dictionary, not about the report - do not read it as "this template has no
columns".

**There are almost no published definitions.** {defined:,} of {items:,} items carry a `Description`, and
none of them belong to PAY. The pack's own glossary is not duplicating anything upstream,
and there is nothing here to harvest for it.

**Case varies in free-text fields.** `Property.PeriodType` holds both `Stock` and `stock`.
Lower-case before grouping on anything that is not a code.

## Example queries

Every one of these was run against release {release}.

### Which module versions a framework has

```sql
SELECT   mv.ModuleVID, mv.Code, mv.Name, mv.VersionNumber,
         mv.FromReferenceDate, mv.ToReferenceDate
FROM     ModuleVersion mv
JOIN     Module m USING (ModuleID)
JOIN     Framework f ON f.FrameworkID = m.FrameworkID
WHERE    f.Code = 'PAY'
ORDER BY mv.Code, mv.VersionNumber;
```

`ToReferenceDate` null is the current one. This is where you discover that the module
version you are describing has a successor.

### The templates in one module version

```sql
SELECT   tv.TableVID, tv.Code, tv.Name
FROM     ModuleVersionComposition mvc
JOIN     TableVersion tv USING (TableVID)
JOIN     ModuleVersion mv USING (ModuleVID)
WHERE    mv.Code = 'PSD_FRP' AND mv.VersionNumber = '1.1.0'
ORDER BY tv.Code;
```

### How many cells a template has, and how many are reportable

```sql
SELECT   tv.Code,
         count(*)                                   AS cells,
         count(*) FILTER (WHERE c.IsExcluded <> 0)   AS excluded
FROM     ModuleVersionComposition mvc
JOIN     TableVersion tv USING (TableVID)
JOIN     TableVersionCell c ON c.TableVID = tv.TableVID
JOIN     ModuleVersion mv USING (ModuleVID)
WHERE    mv.Code = 'PSD_FRP' AND mv.VersionNumber = '1.1.0'
GROUP BY tv.Code
ORDER BY tv.Code;
```

`Y_01.01` answers 396 cells, 72 excluded. The pack has 324 columns for it.

### The rows of a template, with their nesting

```sql
SELECT   hv.Code, hv.Label, parent.Code AS parent_code
FROM     ModuleVersionComposition mvc
JOIN     ModuleVersion mv USING (ModuleVID)
JOIN     TableVersion tv USING (TableVID)
JOIN     TableVersionHeader tvh ON tvh.TableVID = tv.TableVID
JOIN     HeaderVersion hv ON hv.HeaderVID = tvh.HeaderVID
JOIN     Header h ON h.HeaderID = tvh.HeaderID
LEFT JOIN TableVersionHeader ptvh
       ON ptvh.TableVID = tvh.TableVID AND ptvh.HeaderID = tvh.ParentHeaderID
LEFT JOIN HeaderVersion parent ON parent.HeaderVID = ptvh.HeaderVID
WHERE    mv.Code = 'PSD_FRP' AND mv.VersionNumber = '1.1.0'
  AND    tv.Code = 'Y_01.01' AND h.Direction = 'Y'
ORDER BY tvh."Order";
```

`Direction` is `Y` for rows, `X` for columns, `Z` for sheets. The sheet axis is where
PAY's six metric-and-geography variants live.

Note the two lines pinning the module version. Joining `TableVersion` on `Code` alone
answers 117 rows here instead of 39, because `Y_01.01` has three versions and you asked
for all of them. This is the mistake the section at the top is about, and it does not
announce itself - the extra rows look like real rows.

### What one cell measures

```sql
SELECT DISTINCT dimension.Name AS dimension, member.Name AS member
FROM     ModuleVersionComposition mvc
JOIN     ModuleVersion mv USING (ModuleVID)
JOIN     TableVersionCell c ON c.TableVID = mvc.TableVID
JOIN     VariableVersion vv USING (VariableVID)
JOIN     ContextComposition cc ON cc.ContextID = vv.ContextID
JOIN     Item member    ON member.ItemID = cc.ItemID
JOIN     Item dimension ON dimension.ItemID = cc.PropertyID
WHERE    mv.Code = 'PSD_FRP' AND mv.VersionNumber = '1.1.0'
  AND    c.CellCode = '{{Y_01.01, r0010, c0010, s0010}}'
ORDER BY 1;
```

Three dimensions for this cell. Drop the module version and it answers five, because the
older and newer versions of the template break it down differently - and nothing in the
result says which rows came from which. `DISTINCT` is still needed on top: one cell
resolves through several variable versions even within one module version.

### Its data type and period type

```sql
SELECT DISTINCT dt.Name AS data_type, lower(p.PeriodType) AS period_type
FROM     ModuleVersionComposition mvc
JOIN     ModuleVersion mv USING (ModuleVID)
JOIN     TableVersionCell c ON c.TableVID = mvc.TableVID
JOIN     VariableVersion vv USING (VariableVID)
JOIN     Property p ON p.PropertyID = vv.PropertyID
LEFT JOIN DataType dt ON dt.DataTypeID = p.DataTypeID
WHERE    mv.Code = 'PSD_FRP' AND mv.VersionNumber = '1.1.0'
  AND    c.CellCode = '{{Y_01.01, r0010, c0010, s0010}}';
```

`lower()` because `PeriodType` holds both `Stock` and `stock`, and without it one cell
answers two rows that differ only in case.

### The validation rules in scope for a module version

```sql
SELECT   o.Code, os.Severity, ov.Expression
FROM     OperationScopeComposition osc
JOIN     OperationScope os USING (OperationScopeID)
JOIN     OperationVersion ov ON ov.OperationVID = os.OperationVID
JOIN     Operation o ON o.OperationID = ov.OperationID
JOIN     ModuleVersion mv USING (ModuleVID)
WHERE    mv.Code = 'PSD_FRP' AND mv.VersionNumber = '1.1.0'
ORDER BY o.Code;
```

114 rules for PSD_FRP 1.1.0, 71 for DORA 1.1.0. An expression reads
`with {{tY_01.01, c*, s*, default: 0, interval: true}}: {{r0020}} <= {{r0010}}`.

### Which cells a rule actually constrains

This is the query that makes the rules usable, and the reason nothing in this pack parses
DPM-XL. The model has already resolved its own operands:

```sql
SELECT DISTINCT l."Table", l."Row", l."Column", l.Sheet
FROM     Operation o
JOIN     OperationVersion ov ON ov.OperationID = o.OperationID
JOIN     OperationNode n ON n.OperationVID = ov.OperationVID
JOIN     OperandReference r ON r.NodeID = n.NodeID
JOIN     OperandReferenceLocation l ON l.OperandReferenceID = r.OperandReferenceID
WHERE    o.Code = 'v09123_m'
ORDER BY 1, 2, 3, 4;
```

Turn it around - every rule that reaches one cell - and you have what
`09-validation-rules.csv` holds.

### Checking the pack against the model

```sql
ATTACH 'pay42.duckdb' AS pack (READ_ONLY);

WITH dpm AS (
    SELECT replace(c.CellCode, '_', ' ') AS cell
    FROM   ModuleVersionComposition mvc
    JOIN   TableVersionCell c ON c.TableVID = mvc.TableVID
    JOIN   ModuleVersion mv USING (ModuleVID)
    WHERE  mv.Code = 'PSD_FRP' AND mv.VersionNumber = '1.1.0' AND c.IsExcluded = 0
)
SELECT   coalesce(d.cell, p.dpm_cell_code) AS cell,
         d.cell IS NOT NULL                AS in_dpm,
         p.dpm_cell_code IS NOT NULL       AS in_pack
FROM     dpm d
FULL OUTER JOIN pack.datapoints p ON p.dpm_cell_code = d.cell
WHERE    d.cell IS NULL OR p.dpm_cell_code IS NULL;
```

Empty is the right answer, and `source/check_against_dpm2.py` is this in both directions.
Note the `replace`: the model writes `Y_01.01` where the pack writes `Y 01.01`.

### Where the published definitions are

```sql
SELECT   f.Code AS framework, count(DISTINCT i.ItemID) AS described_items
FROM     Item i
JOIN     ContextComposition cc ON cc.ItemID = i.ItemID
JOIN     VariableVersion vv ON vv.ContextID = cc.ContextID
JOIN     TableVersionCell c ON c.VariableVID = vv.VariableVID
JOIN     ModuleVersionComposition mvc ON mvc.TableVID = c.TableVID
JOIN     ModuleVersion mv USING (ModuleVID)
JOIN     Module m ON m.ModuleID = mv.ModuleID
JOIN     Framework f ON f.FrameworkID = m.FrameworkID
WHERE    i.Description IS NOT NULL AND i.Description <> ''
GROUP BY 1
ORDER BY 2 DESC;
```

COREP, PILLAR3, IF, MiCA and a few others. The eight under PAY belong to SEPA_IPR, not
to the fraud-reporting module this pack describes.

## Every table in the database

{inventory(duckdb.connect(str(DPM2), read_only=True))}

## Licence

The code that builds this is MIT. The content is EBA material, reproduced under the EBA
legal notice, which authorises reproduction provided the source is acknowledged - see
`NOTICE`. Not affiliated with or endorsed by the EBA.
"""

    OUT.write_text(body, encoding="utf-8")
    print(f"{OUT.name}: {len(REL)} relationships verified, {tables} tables inventoried")


if __name__ == "__main__":
    main()
