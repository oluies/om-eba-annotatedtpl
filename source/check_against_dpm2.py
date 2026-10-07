"""Check the pack against the EBA DPM 2.0 database it is supposed to describe.

The pack is extracted from the annotated table layout - a spreadsheet rendering of the
model. This asks the model directly whether that extraction kept every cell and invented
none, which is the one thing the build cannot check about itself.

    uv run source/fetch_dpm2.py && uv run source/check_against_dpm2.py

Two details the comparison has to absorb:

  * The DPM writes a table code as `Y_01.01`, the annotated layout and the warehouse's
    BA_Form_Cell write it `Y 01.01`. Same cell, different separator.
  * A cell with IsExcluded set is a greyed-out box in the template: in the model but not
    reportable. The pack leaves them out, so the comparison does too.

Exits non-zero when the pack and the model disagree.
"""

import os
import sys
from pathlib import Path

import duckdb

REPO = Path(__file__).resolve().parent.parent
DPM2 = Path(os.environ.get("DPM2_DB") or REPO / "source" / "dpm2" / "dpm2.duckdb")
PACK = Path(os.environ.get("PAY42_DB") or REPO / "pay42.duckdb")

# The two modules the pack covers, by ModuleVersion.Code and VersionNumber.
MODULES = {"PAY": ("PSD_FRP", "1.1.0"), "DORA": ("DORA", "1.1.0")}

# The pack's PAY cell code, normalised to the DPM's spelling, against the module's
# reportable cells. A full outer join so a cell missing on either side shows up.
PAY_SQL = """
WITH dpm AS (
    SELECT replace(c.CellCode, '_', ' ') AS cell
    FROM   ModuleVersionComposition mvc
    JOIN   TableVersionCell c ON c.TableVID = mvc.TableVID
    WHERE  mvc.ModuleVID = ? AND c.IsExcluded = 0
)
SELECT coalesce(d.cell, p.dpm_cell_code) AS cell,
       d.cell IS NOT NULL                AS in_dpm,
       p.dpm_cell_code IS NOT NULL       AS in_pack
FROM   dpm d FULL OUTER JOIN pack.datapoints p ON p.dpm_cell_code = d.cell
WHERE  d.cell IS NULL OR p.dpm_cell_code IS NULL
"""

# DORA's open tables have no sheet axis and a literal `r*` row, so the pack stores a
# column pattern rather than a cell code. Table, row and column codes still line up.
DORA_SQL = """
WITH dpm AS (
    SELECT DISTINCT replace(tv.Code, '.', '_') AS tbl,
           regexp_extract(c.CellCode, 'r([0-9*]+)', 1) AS row_code,
           regexp_extract(c.CellCode, 'c([0-9*]+)', 1) AS column_code
    FROM   ModuleVersionComposition mvc
    JOIN   TableVersion tv ON tv.TableVID = mvc.TableVID
    JOIN   TableVersionCell c ON c.TableVID = mvc.TableVID
    WHERE  mvc.ModuleVID = ? AND c.IsExcluded = 0
), pk AS (
    SELECT table_name AS tbl, row_code, column_code FROM pack.dora
)
SELECT coalesce(d.tbl, p.tbl) || ' r' || coalesce(d.row_code, p.row_code)
         || ' c' || coalesce(d.column_code, p.column_code) AS cell,
       d.tbl IS NOT NULL AS in_dpm,
       p.tbl IS NOT NULL AS in_pack
FROM   dpm d FULL OUTER JOIN pk p
       ON p.tbl = d.tbl AND p.row_code = d.row_code AND p.column_code = d.column_code
WHERE  d.tbl IS NULL OR p.tbl IS NULL
"""


def one(con: duckdb.DuckDBPyConnection, sql: str, *params: object) -> tuple:
    """A query that must return a row. fetchone() types as optional and a None here would
    mean the DPM database is not the one this was written against, which is worth saying."""
    row = con.execute(sql, list(params)).fetchone()
    if row is None:
        raise SystemExit(f"{DPM2.name} answered nothing to: {sql.strip()}")
    return row


def module_vid(con: duckdb.DuckDBPyConnection, code: str, version: str) -> int:
    row = con.execute(
        "SELECT ModuleVID FROM ModuleVersion WHERE Code = ? AND VersionNumber = ?", [code, version]
    ).fetchone()
    if row is None:
        raise SystemExit(f"no module version {code} {version} in {DPM2.name}")
    return int(row[0])


def report(label: str, differences: list[tuple[str, bool, bool]]) -> bool:
    if not differences:
        return True
    missing = [c for c, in_dpm, _ in differences if in_dpm]
    extra = [c for c, _, in_pack in differences if in_pack]
    print(f"{label}: {len(missing)} cell(s) in the DPM but not the pack, {len(extra)} the other way")
    for cell in (missing + extra)[:10]:
        print(f"    {cell}")
    return False


def main() -> None:
    for path in (DPM2, PACK):
        if not path.exists():
            raise SystemExit(f"{path} does not exist - run source/fetch_dpm2.py and source/build_duckdb.py")

    con = duckdb.connect(str(DPM2), read_only=True)
    con.execute(f"ATTACH '{PACK}' AS pack (READ_ONLY)")
    release = one(con, "SELECT Code, Date FROM Release ORDER BY ReleaseID DESC LIMIT 1")
    print(f"DPM 2.0 release {release[0]} ({release[1]})")

    ok = True
    for label, (sql, (code, version)) in {
        "PAY": (PAY_SQL, MODULES["PAY"]),
        "DORA": (DORA_SQL, MODULES["DORA"]),
    }.items():
        vid = module_vid(con, code, version)
        differences = con.execute(sql, [vid]).fetchall()
        table = "datapoints" if label == "PAY" else "dora"
        total = one(con, f"SELECT count(*) FROM pack.{table}")[0]  # noqa: S608 - fixed above
        ok &= report(f"{code} {version}", differences)
        if not differences:
            print(f"{code} {version}: all {total} pack rows match the model, none missing")

    rules = con.execute(
        """
        SELECT mv.Code, count(*)
        FROM   OperationScopeComposition osc
        JOIN   ModuleVersion mv ON mv.ModuleVID = osc.ModuleVID
        WHERE  osc.ModuleVID IN ?
        GROUP  BY 1 ORDER BY 1
        """,
        [tuple(module_vid(con, c, v) for c, v in MODULES.values())],
    ).fetchall()
    print("validation rules, extracted to 09-validation-rules.csv: " + ", ".join(f"{c} {n}" for c, n in rules))
    con.close()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
