"""Check the datapoint ids the pack cites against the DPM, and repair them.

A reported fact names a datapoint and nothing else, so the id in a column description is
the one thing a reader can take back to the model. The DPM has two numbers per cell and
they are easy to confuse:

    VariableID   the datapoint. Stable across module versions - 436318 is
                 {Y_01.01, r0190, c0020, s0020} in PSD_FRP 1.0.1, 1.1.0 and 1.2.0 alike -
                 and what `lookup_dpm_datapoint` and an xBRL-CSV fact name.
    VariableVID  one version of that variable's specification. New at every module
                 version: the same cell is 436318, then 3263044, then 5461648.

The pack cited the VariableVID of PSD_FRP 1.1.0 for all 1 830 PAY cells, so not one of
them resolved as a datapoint, and eight of DORA's 85 as well. This is the check that would
have caught it, and `--fix` writes the ids back.

It needs the DPM database, so it is local rather than CI, like check_against_dpm2.py:

    uv run source/check_datapoint_ids.py           # report
    uv run source/check_datapoint_ids.py --fix     # and correct the two CSVs
"""

import argparse
import csv
import io
import sys
from pathlib import Path
from typing import Any, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import dpm_lookup  # noqa: E402

SOURCE = Path(__file__).resolve().parent
REPO = SOURCE.parent

# The id a reporter cites, by coordinate. VariableID rather than the cell's own
# VariableVID: the one is the datapoint, the other is this version's specification of it.
IDS_SQL = """
SELECT   tv.Code AS template,
         coalesce(hr.Code, '*') AS row_code,
         coalesce(hc.Code, '*') AS column_code,
         coalesce(hs.Code, '')  AS sheet_code,
         vv.VariableID          AS datapoint_id,
         c.Sign                 AS sign
FROM     ModuleVersionComposition mvc
JOIN     ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
JOIN     TableVersionCell c ON c.TableVID = mvc.TableVID AND c.IsExcluded = 0
JOIN     TableVersion tv ON tv.TableVID = c.TableVID
JOIN     Cell cc ON cc.CellID = c.CellID
JOIN     VariableVersion vv ON vv.VariableVID = c.VariableVID
LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
LEFT JOIN TableVersionHeader tc ON tc.TableVID = c.TableVID AND tc.HeaderID = cc.ColumnID
LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
LEFT JOIN TableVersionHeader ts ON ts.TableVID = c.TableVID AND ts.HeaderID = cc.SheetID
LEFT JOIN HeaderVersion hs ON hs.HeaderVID = ts.HeaderVID
WHERE    mv.Code = ? AND mv.VersionNumber = ?
"""


class Source(NamedTuple):
    """One CSV of cited ids, and how to read a coordinate out of a row."""

    label: str
    path: Path
    module: str
    version: str
    sheet_column: str | None


# PSD_FRP 1.2.0 is the version in force from 2026-03-31; 1.1.0 covered no reporting period
# at all. The datapoint ids are the same either way, which is the point - they do not move
# with the module version - but asking the live one means the sign comes from it too.
SOURCES = (
    Source("PAY", SOURCE / "dpm-psd_frp-1.2.0-datapoints.csv", "PSD_FRP", "1.2.0", "variant"),
    Source("DORA", SOURCE / "dpm-dora-1.1.0-datapoints.csv", "DORA", "1.1.0", None),
)


def published(module: str, version: str) -> dict[tuple[str, str, str, str], dict[str, Any]]:
    """Every reportable cell of one module version, by coordinate."""
    with dpm_lookup._connect() as con:  # noqa: SLF001 - the one connection helper the lookups have
        con.execute(IDS_SQL, [module, version])
        names = [column[0] for column in con.description or []]
        rows = [dict(zip(names, row, strict=True)) for row in con.fetchall()]
    return {(r["template"], r["row_code"], r["column_code"], r["sheet_code"]): r for r in rows}


def coordinate(row: dict[str, str], sheet_column: str | None) -> tuple[str, str, str, str]:
    """The row's coordinate, in the spelling the DPM uses for it."""
    return (
        row["template"],
        row["row_code"],
        row["column_code"],
        row[sheet_column] if sheet_column else "",
    )


class Audit(NamedTuple):
    """What the file gets wrong, and the id each row should carry."""

    said: list[str]
    rows: int
    wanted: dict[int, str]


def audit(source: Source, cells: dict[tuple[str, str, str, str], dict[str, Any]]) -> Audit:
    """What the CSV says against what the DPM says, by row number. Pure but for the read."""
    with source.path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    said: list[str] = []
    wanted: dict[int, str] = {}
    for n, row in enumerate(rows):
        where = coordinate(row, source.sheet_column)
        found = cells.get(where)
        if found is None:
            said.append(f"  {where} is not a reportable cell of this module version")
            continue
        want = str(found["datapoint_id"])
        if row["datapoint_id"] != want:
            said.append(f"  {where}: cites {row['datapoint_id']}, the datapoint is {want}")
            wanted[n] = want
    return Audit(said, len(rows), wanted)


def field(line: str, column: int, value: str) -> str:
    """The line back with one field replaced, quoted the way csv wants it. Pure."""
    fields = next(csv.reader([line]))
    fields[column] = value
    written = io.StringIO()
    csv.writer(written, lineterminator="\n").writerow(fields)
    return written.getvalue()


def repaired(path: Path, wanted: dict[int, str]) -> str:
    """The file's own text, with only the ids that were wrong replaced. Pure but for the read.

    Line by line rather than re-serialising every row: a full rewrite changes the quoting
    of fields nobody touched - and the line endings, if the writer is left to its default -
    so the diff of a repair stops being the repair.
    """
    header, *rest = path.read_text(encoding="utf-8").splitlines(keepends=True)
    column = next(n for n, name in enumerate(next(csv.reader([header]))) if name == "datapoint_id")
    return header + "".join(field(line, column, wanted[n]) if n in wanted else line for n, line in enumerate(rest))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fix", action="store_true", help="write the datapoint ids back into the CSVs")
    parser.add_argument("--quiet", action="store_true", help="only the counts, not every mismatch")
    args = parser.parse_args()

    if not dpm_lookup.available():
        raise SystemExit(dpm_lookup.BUILD_IT)

    wrong = 0
    for source in SOURCES:
        if not source.path.exists():
            raise SystemExit(f"{source.path} does not exist. Export it first - see the module docstring.")
        checked = audit(source, published(source.module, source.version))
        wrong += len(checked.said)
        print(
            f"{source.label} ({source.module} {source.version}, {source.path.name}): "
            f"{len(checked.said)} of {checked.rows} wrong"
        )
        if checked.said and not args.quiet:
            print("\n".join(checked.said[:20]))
            if len(checked.said) > 20:
                print(f"  ... and {len(checked.said) - 20} more")
        if args.fix and checked.wanted:
            source.path.write_text(repaired(source.path, checked.wanted), encoding="utf-8")
            print(f"  written: {source.path.relative_to(REPO)}")

    if wrong and not args.fix:
        raise SystemExit("The cited ids are not the DPM's datapoints. Re-run with --fix.")


if __name__ == "__main__":
    main()
