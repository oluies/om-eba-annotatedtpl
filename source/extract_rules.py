"""Extract the validation rules of the pack's two modules from the DPM 2.0 database.

A rule's expression is DPM-XL, which would have to be parsed to know which cells it
constrains. It does not: the model resolves every operand itself, in
OperandReferenceLocation, down to table, row, column and sheet. This reads that out, so
the pack can say per column which rules touch it without interpreting anything.

    uv run source/fetch_dpm2.py && uv run source/extract_rules.py

Writes 09-validation-rules.csv, one row per rule and cell it reaches. Table codes are
rewritten to the warehouse spelling (Y_01_01), and the sheet code is the PAY variant -
a rule often applies to only some of the six.

An axis code the model leaves empty means one of two things, and the table's own open-axis
flags say which: `*` where the axis is open and the rule covers every value of it, as for
every DORA row, and empty where the table has no such axis at all, as for the sheet of
the Y_xx_02 loss tables.
"""

import csv
import os
from pathlib import Path

import duckdb

REPO = Path(__file__).resolve().parent.parent
# DPM2_DIR has to be honoured wherever DPM2_DB is, because fetch_dpm2.py puts the database
# inside it: resolving only DPM2_DB leaves this looking in the default directory for a file
# that was downloaded somewhere else, and reporting it as never downloaded.
DIR = Path(os.environ.get("DPM2_DIR") or REPO / "source" / "dpm2")
DPM2 = Path(os.environ.get("DPM2_DB") or DIR / "dpm2.duckdb")
OUT = REPO / "09-validation-rules.csv"

# The module versions the pack describes, as (ModuleVersion.Code, VersionNumber).
MODULES = (("PSD_FRP", "1.1.0"), ("DORA", "1.1.0"))

# A rule is in scope for a module version through OperationScope, and reaches cells
# through its nodes' operands. DISTINCT because an operand can appear in several nodes of
# the same rule - once per side of a sum - and the cell is the same cell either way.
SQL = """
SELECT DISTINCT
       o.Code                                            AS rule_code,
       os.Severity                                       AS severity,
       replace(l."Table", '.', '_')                      AS table_name,
       coalesce(l."Row",    CASE WHEN t.HasOpenRows   <> 0 THEN '*' ELSE '' END) AS row_code,
       coalesce(l."Column", CASE WHEN t.HasOpenColumns <> 0 THEN '*' ELSE '' END) AS column_code,
       coalesce(l.Sheet,    CASE WHEN t.HasOpenSheets  <> 0 THEN '*' ELSE '' END) AS sheet_code,
       ov.Expression                                     AS expression
FROM   OperationScopeComposition osc
JOIN   OperationScope os       ON os.OperationScopeID = osc.OperationScopeID
JOIN   OperationVersion ov     ON ov.OperationVID = os.OperationVID
JOIN   Operation o             ON o.OperationID = ov.OperationID
JOIN   OperationNode n         ON n.OperationVID = ov.OperationVID
JOIN   OperandReference r      ON r.NodeID = n.NodeID
JOIN   OperandReferenceLocation l ON l.OperandReferenceID = r.OperandReferenceID
JOIN   Cell c                  ON c.CellID = l.CellID
JOIN   "Table" t               ON t.TableID = c.TableID
WHERE  osc.ModuleVID = ?
ORDER  BY table_name, row_code, column_code, sheet_code, rule_code
"""

FIELDS = ("module", "rule_code", "severity", "table_name", "row_code", "column_code", "sheet_code", "expression")


def module_vid(con: duckdb.DuckDBPyConnection, code: str, version: str) -> int:
    row = con.execute(
        "SELECT ModuleVID FROM ModuleVersion WHERE Code = ? AND VersionNumber = ?", [code, version]
    ).fetchone()
    if row is None:
        raise SystemExit(f"no module version {code} {version} in {DPM2.name}")
    return row[0]


def main() -> None:
    if not DPM2.exists():
        raise SystemExit(f"{DPM2} does not exist - run source/fetch_dpm2.py first")
    con = duckdb.connect(str(DPM2), read_only=True)

    rows = [
        (f"{code} {version}", *record)
        for code, version in MODULES
        for record in con.execute(SQL, [module_vid(con, code, version)]).fetchall()
    ]
    con.close()

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(FIELDS)
        writer.writerows(rows)

    modules = {row[0] for row in rows}
    per_module = {m: len({r[1] for r in rows if r[0] == m}) for m in sorted(modules)}
    size = OUT.stat().st_size / 1024
    print(
        f"{OUT.name}: {len(rows)} rule-cell rows, "
        + ", ".join(f"{m} {n} rules" for m, n in per_module.items())
        + f"  ({size:.0f} KiB)"
    )


if __name__ == "__main__":
    main()
