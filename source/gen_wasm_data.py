"""Publish the DPM as parquet a browser can query with DuckDB-WASM.

    uv run source/gen_wasm_data.py                       # every release, into web/public/data
    uv run source/gen_wasm_data.py --dpm-release 4.4     # into web/public/data/4.4
    uv run source/gen_wasm_data.py --out /tmp/data --db source/dpm2/dpm2_4_4.duckdb

A named release lands in its own directory and `releases.json` beside them lists what is
there, so the page can offer them. Releases are separate answers to the same question -
FINREP9 is taxonomy 3.2.0 in DPM 4.0 and 3.3.0 from 4.2 - and merging them would make
"which release says this" unanswerable, here as in the database.

Seven tables, pre-joined, answer every question the agent tools answer. Publishing the
model's own tables instead would be 71.6 MB, of which ContextComposition alone is 38.

Two things decide the size, and neither is the codec. Measured on the dimension table:

  - Sorting on the column the questions filter by, with 50k row groups: 7.58 MB to
    3.26 MB, and the bytes a browser pulls for six questions from 32.9 MB to 8.3 MB.
    Unsorted, parquet statistics prune nothing and DuckDB reads past the whole file.
  - Partitioning the three big tables by framework: one question reads one partition,
    0.35 MB for FINREP against 3.3 MB for all of them.

Against those, the codec is noise: zstd 3.26 MB, zstd 22 3.14 MB, brotli 3.01 MB, gzip
3.25 MB, snappy 3.84 MB. zstd at its highest level costs 0.3s to write and is read by
every DuckDB build; brotli's extra 4% is not worth finding out whether the WASM build
reads it.
"""

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import NamedTuple

import duckdb

REPO = Path(__file__).resolve().parent.parent
DIR = Path(os.environ.get("DPM2_DIR") or REPO / "source" / "dpm2")
DB = Path(os.environ.get("DPM2_DB") or DIR / "dpm2.duckdb")
OUT = REPO / "web" / "public" / "data"

# Sorted, because statistics can only prune what is clustered; 50k rows per group,
# measured in the browser rather than guessed.
ROW_GROUP_SIZE = 50_000
COMPRESSION = "COMPRESSION zstd, COMPRESSION_LEVEL 22"


class Published(NamedTuple):
    """One table as it is published: the query, how it is sorted, how it is split."""

    name: str
    sql: str
    order_by: str
    partition_by: str | None = None


# `?` twice in each of these is the release predicate: null means every release, and a
# release code means the module versions in force in it - the same window the lookups
# use, `StartReleaseID <= asked AND (EndReleaseID IS NULL OR EndReleaseID > asked)`.
IN_RELEASE = """
    AND (
        ? IS NULL
        OR EXISTS (
            SELECT 1 FROM Release asked
            WHERE asked.Code = ?
              AND mv.StartReleaseID <= asked.ReleaseID
              AND (mv.EndReleaseID IS NULL OR mv.EndReleaseID > asked.ReleaseID)
        )
    )
"""

FRAMEWORK_OF_TABLE = f"""
SELECT DISTINCT tv.Code AS table_code, f.Code AS framework
FROM   TableVersion tv
JOIN   ModuleVersionComposition mvc ON mvc.TableVID = tv.TableVID
JOIN   ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
JOIN   Module m ON m.ModuleID = mv.ModuleID
JOIN   Framework f ON f.FrameworkID = m.FrameworkID
WHERE  1 = 1 {IN_RELEASE}
"""

TABLES = [
    Published(
        "modules",
        f"""
        SELECT DISTINCT f.Code AS framework, f.Name AS framework_name,
               mv.Code AS module, mv.Name AS module_name,
               mv.VersionNumber AS taxonomy_version, rel.Code AS dpm_release,
               CAST(mv.FromReferenceDate AS VARCHAR) AS from_reference_date,
               CAST(mv.ToReferenceDate AS VARCHAR) AS to_reference_date,
               mv.ToReferenceDate IS NOT NULL
                 AND mv.FromReferenceDate = mv.ToReferenceDate AS do_not_use
        FROM   ModuleVersion mv
        JOIN   Module m ON m.ModuleID = mv.ModuleID
        JOIN   Framework f ON f.FrameworkID = m.FrameworkID
        JOIN   Release rel ON rel.ReleaseID = mv.StartReleaseID
        WHERE  1 = 1 {IN_RELEASE}
        """,
        "framework, module, taxonomy_version",
    ),
    Published(
        "cells",
        f"""
        SELECT fw.framework, tv.Code AS table_code, mv.Code AS module,
               mv.VersionNumber AS taxonomy_version, rel.Code AS dpm_release,
               -- No CellCode: it is the three columns next to it with punctuation
               -- around them, and composing it where it is shown costs 46 kB less per
               -- framework than storing it. (Written without the braces, because this
               -- query is inside an f-string and a brace here is an expression.)
               vv.VariableID AS datapoint,
               coalesce(hr.Code, '*') AS row_code, left(hr.Label, 120) AS row_label,
               coalesce(hc.Code, '*') AS column_code, left(hc.Label, 120) AS column_label,
               coalesce(hs.Code, '') AS sheet_code
        FROM   TableVersionCell c
        JOIN   TableVersion tv ON tv.TableVID = c.TableVID
        JOIN   VariableVersion vv ON vv.VariableVID = c.VariableVID
        JOIN   Cell cc ON cc.CellID = c.CellID
        JOIN   ModuleVersionComposition mvc ON mvc.TableVID = tv.TableVID
        JOIN   ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
        JOIN   Release rel ON rel.ReleaseID = mv.StartReleaseID
        JOIN   ({FRAMEWORK_OF_TABLE}) fw ON fw.table_code = tv.Code
        LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
        LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
        LEFT JOIN TableVersionHeader tc ON tc.TableVID = c.TableVID AND tc.HeaderID = cc.ColumnID
        LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
        LEFT JOIN TableVersionHeader ts ON ts.TableVID = c.TableVID AND ts.HeaderID = cc.SheetID
        LEFT JOIN HeaderVersion hs ON hs.HeaderVID = ts.HeaderVID
        -- An excluded cell is a greyed-out box: in the model, not reportable. The pack
        -- leaves them out and so does this, or a count of cells means two things.
        WHERE  c.IsExcluded = 0 {IN_RELEASE}
        """,
        "table_code, module, taxonomy_version, row_code, column_code",
        partition_by="framework",
    ),
    Published(
        "cell_members",
        f"""
        -- The coordinates, not the datapoint id. The id is unique per cell, so inside
        -- a (template, dimension, member) group it is a random int64 that compresses to
        -- nothing: 336 kB of the COREP partition's 455. The row and column codes are
        -- short, sorted and already what the answer shows, and the id comes back from
        -- the join to `cells` for anyone who wants it. 455 kB to 122.
        SELECT DISTINCT fw.framework, tv.Code AS table_code,
               coalesce(hr.Code, '*') AS row_code, coalesce(hc.Code, '*') AS column_code,
               trim(dim.Name) AS dimension, trim(i.Name) AS member
        FROM   TableVersionCell c
        JOIN   Cell cc ON cc.CellID = c.CellID
        LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
        LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
        LEFT JOIN TableVersionHeader tc2 ON tc2.TableVID = c.TableVID AND tc2.HeaderID = cc.ColumnID
        LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc2.HeaderVID
        JOIN   TableVersion tv ON tv.TableVID = c.TableVID
        JOIN   VariableVersion vv ON vv.VariableVID = c.VariableVID
        JOIN   ContextComposition x ON x.ContextID = vv.ContextID
        JOIN   Item i ON i.ItemID = x.ItemID
        JOIN   Item dim ON dim.ItemID = x.PropertyID
        JOIN   ModuleVersionComposition mvc ON mvc.TableVID = tv.TableVID
        JOIN   ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
        JOIN   ({FRAMEWORK_OF_TABLE}) fw ON fw.table_code = tv.Code
        WHERE  c.IsExcluded = 0 {IN_RELEASE}
        """,
        "table_code, dimension, member, row_code, column_code",
        partition_by="framework",
    ),
    Published(
        "headers",
        f"""
        SELECT DISTINCT fw.framework, tv.Code AS table_code, h.Direction AS direction,
               hv.Code AS code, left(hv.Label, 120) AS label, parent.Code AS parent_code,
               tvh.IsAbstract <> 0 AS is_abstract, h.IsKey <> 0 AS is_key,
               ic.Code AS property_code, i.Name AS property
        FROM   TableVersionHeader tvh
        JOIN   TableVersion tv ON tv.TableVID = tvh.TableVID
        JOIN   HeaderVersion hv ON hv.HeaderVID = tvh.HeaderVID
        JOIN   Header h ON h.HeaderID = tvh.HeaderID
        JOIN   ModuleVersionComposition mvc ON mvc.TableVID = tv.TableVID
        JOIN   ModuleVersion mv ON mv.ModuleVID = mvc.ModuleVID
        JOIN   ({FRAMEWORK_OF_TABLE}) fw ON fw.table_code = tv.Code
        LEFT JOIN TableVersionHeader ptvh ON ptvh.TableVID = tvh.TableVID
                                         AND ptvh.HeaderID = tvh.ParentHeaderID
        LEFT JOIN HeaderVersion parent ON parent.HeaderVID = ptvh.HeaderVID
        LEFT JOIN Item i ON i.ItemID = hv.PropertyID
        -- The code in force: 233 properties have been recoded, and an unscoped join
        -- returns the header once per code it has ever had.
        LEFT JOIN ItemCategory ic ON ic.ItemID = i.ItemID AND ic.EndReleaseID IS NULL
        WHERE  1 = 1 {IN_RELEASE}
        """,
        "table_code, direction, code",
    ),
    Published(
        "rules",
        f"""
        SELECT DISTINCT op.Code AS rule_code, op.Type AS type, mv.Code AS module,
               mv.VersionNumber AS taxonomy_version, rel.Code AS dpm_release,
               os.Severity AS severity, os.IsActive <> 0 AS active,
               CAST(os.FromSubmissionDate AS VARCHAR) AS from_submission_date,
               ov.Expression AS expression, ov.OperationVID AS operation_vid
        FROM   Operation op
        JOIN   OperationVersion ov ON ov.OperationID = op.OperationID
        JOIN   OperationScope os ON os.OperationVID = ov.OperationVID
        JOIN   OperationScopeComposition osc ON osc.OperationScopeID = os.OperationScopeID
        JOIN   ModuleVersion mv ON mv.ModuleVID = osc.ModuleVID
        JOIN   Release rel ON rel.ReleaseID = mv.StartReleaseID
        WHERE  1 = 1 {IN_RELEASE}
        """,
        "rule_code, module, taxonomy_version",
    ),
    Published(
        "rule_cells",
        f"""
        SELECT DISTINCT fw.framework, n.OperationVID AS operation_vid,
               l."Table" AS table_code, coalesce(l."Row", '*') AS row_code,
               coalesce(l."Column", '*') AS column_code, coalesce(l.Sheet, '') AS sheet_code
        FROM   OperationNode n
        JOIN   OperandReference r ON r.NodeID = n.NodeID
        JOIN   OperandReferenceLocation l USING (OperandReferenceID)
        JOIN   ({FRAMEWORK_OF_TABLE}) fw ON fw.table_code = l."Table"
        """,
        # Within the rule, not only within the template: a rule's own rows and columns
        # are a run, and sorting by the table alone leaves them interleaved with every
        # other rule's. 499 kB to 172.
        "table_code, operation_vid, row_code, column_code",
        partition_by="framework",
    ),
    Published(
        # Which rows add up to which, taken from the rules rather than from reading a
        # grid. The browser cannot do this itself: the expression tree is 151k nodes, and
        # publishing it to re-walk there would cost more than the answer.
        #
        # The shape of a rule is resolved once per operation version and the module
        # versions are joined on at the end. Carrying module and version through the
        # recursion instead multiplies 48k nodes by the versions each rule belongs to,
        # which is the difference between seconds and not finishing.
        "sums",
        f"""
        WITH RECURSIVE arith AS (
            -- Only rules that can be sums enter the recursion: a root `=` with a `+`
            -- under it. 4972 of 19789 operation versions, 47890 of 151240 nodes.
            SELECT ov.OperationVID
            FROM   OperationVersion ov
            WHERE  EXISTS (
                     SELECT 1 FROM OperationNode r
                     LEFT JOIN Operator o ON o.OperatorID = r.OperatorID
                     WHERE r.OperationVID = ov.OperationVID AND r.ParentNodeID IS NULL AND o.Symbol = '=')
               AND EXISTS (
                     SELECT 1 FROM OperationNode p
                     LEFT JOIN Operator o2 ON o2.OperatorID = p.OperatorID
                     WHERE p.OperationVID = ov.OperationVID AND o2.Symbol = '+')
        ), node AS (
            SELECT n.OperationVID, n.NodeID, n.ParentNodeID, n.IsLeaf, o.Symbol
            FROM   arith
            JOIN   OperationNode n ON n.OperationVID = arith.OperationVID
            LEFT JOIN Operator o ON o.OperatorID = n.OperatorID
        ), child AS (
            SELECT r.OperationVID, r.NodeID AS eq, c.NodeID, c.Symbol, c.IsLeaf
            FROM   node r JOIN node c ON c.ParentNodeID = r.NodeID
            WHERE  r.ParentNodeID IS NULL AND r.Symbol = '='
        ), addends AS (
            SELECT eq, NodeID AS node, IsLeaf FROM child WHERE Symbol = '+'
            UNION ALL
            SELECT a.eq, n.NodeID, n.IsLeaf FROM addends a JOIN node n ON n.ParentNodeID = a.node
        ), located AS (
            SELECT r.NodeID, l."Table" AS tbl, coalesce(l."Row", '*') AS row_code,
                   coalesce(l."Column", '*') AS col, coalesce(l.Sheet, '') AS sheet
            FROM   OperandReference r JOIN OperandReferenceLocation l USING (OperandReferenceID)
        ), edges AS (
            SELECT   eqs.OperationVID, tc.tbl AS table_code, tc.row_code AS total_row,
                     list_sort(list(DISTINCT ac.row_code)) AS addend_rows,
                     list_sort(list(DISTINCT tc.col))      AS columns,
                     list_sort(list(DISTINCT tc.sheet))    AS sheets
            FROM     child eqs
            JOIN     located tc ON tc.NodeID = eqs.NodeID AND eqs.IsLeaf <> 0
            JOIN     addends a ON a.eq = eqs.eq AND a.IsLeaf <> 0
            JOIN     located ac ON ac.NodeID = a.node
                               AND ac.tbl = tc.tbl AND ac.col = tc.col AND ac.sheet = tc.sheet
            GROUP BY eqs.OperationVID, tc.tbl, tc.row_code
        )
        SELECT   fw.framework, e.table_code, mv.Code AS module,
                 mv.VersionNumber AS taxonomy_version, op.Code AS rule_code,
                 os.Severity AS severity, os.IsActive <> 0 AS active,
                 e.total_row, e.addend_rows, e.columns, e.sheets
        FROM     edges e
        JOIN     OperationVersion ov ON ov.OperationVID = e.OperationVID
        JOIN     Operation op ON op.OperationID = ov.OperationID
        JOIN     OperationScope os ON os.OperationVID = ov.OperationVID
        JOIN     OperationScopeComposition osc ON osc.OperationScopeID = os.OperationScopeID
        JOIN     ModuleVersion mv ON mv.ModuleVID = osc.ModuleVID
        JOIN     ({FRAMEWORK_OF_TABLE}) fw ON fw.table_code = e.table_code
        WHERE    1 = 1 {IN_RELEASE}
        """,
        "table_code, module, total_row, rule_code",
    ),
    Published(
        "properties",
        """
        SELECT ic.Code AS code, i.Name AS property, ic.StartReleaseID AS from_release_id,
               ic.EndReleaseID AS until_release_id
        FROM   ItemCategory ic
        JOIN   Item i ON i.ItemID = ic.ItemID
        """,
        "code",
    ),
    # What has changed about a template, which is the one thing on a page that is *not*
    # an answer under the release the reader picked - it is a comparison across all of
    # them, so it cannot be computed from the tables above and has to be published.
    #
    # Deliberately counts rather than a list: 119 816 variables have been placed
    # somewhere, and a reader wants to know whether this template moved, not which
    # datapoint went where. lookup_dpm_history answers that, one datapoint at a time.
    Published(
        "template_changes",
        f"""
        WITH fw AS ({FRAMEWORK_OF_TABLE}),
        placed AS (
          SELECT vv.VariableID, tv.Code AS table_code,
                 'r' || coalesce(hr.Code, '*') || ' c' || coalesce(hc.Code, '*') AS place
          FROM   TableVersionCell c
          JOIN   VariableVersion vv ON vv.VariableVID = c.VariableVID
          JOIN   TableVersion tv ON tv.TableVID = c.TableVID
          JOIN   Cell cc ON cc.CellID = c.CellID
          LEFT JOIN TableVersionHeader tr ON tr.TableVID = c.TableVID AND tr.HeaderID = cc.RowID
          LEFT JOIN HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
          LEFT JOIN TableVersionHeader tc ON tc.TableVID = c.TableVID AND tc.HeaderID = cc.ColumnID
          LEFT JOIN HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
          WHERE  c.IsExcluded = 0
        ),
        here AS (SELECT DISTINCT VariableID, table_code FROM placed),
        spread AS (
          SELECT h.table_code, h.VariableID,
                 count(DISTINCT p.place) AS places,
                 count(DISTINCT p.table_code) AS templates
          FROM   here h JOIN placed p USING (VariableID)
          GROUP  BY h.table_code, h.VariableID
        )
        SELECT   fw.framework, spread.table_code,
                 count(*)                               AS datapoints,
                 coalesce(sum((places > 1)::INT), 0)    AS moved,
                 coalesce(sum((templates > 1)::INT), 0) AS shared
        FROM     spread
        JOIN     fw ON fw.table_code = spread.table_code
        GROUP BY fw.framework, spread.table_code
        """,
        "table_code",
        partition_by="framework",
    ),
    # Rows whose wording changed while the coordinate and the datapoint stayed - the
    # change nobody notices, because nothing in a report looks different.
    #
    # The condition is on the coordinate and not on the header. A header's label can vary
    # across versions that this template never carried, and the framework join fans a row
    # out once per framework the template is in - so filtering on "this HeaderID has more
    # than one wording somewhere" published rows that show one wording, several times
    # over. What a page claims is that *this row* was reworded, so that is what is asked.
    Published(
        "relabelled",
        f"""
        WITH fw AS ({FRAMEWORK_OF_TABLE}),
        said AS (
          SELECT DISTINCT
                 fw.framework, tv.Code AS table_code, hv.Code AS row_code,
                 th.HeaderID AS header_id,
                 rs.Code AS from_release, coalesce(re.Code, '') AS to_release,
                 trim(hv.Label) AS label, hv.StartReleaseID AS start_release_id
          FROM   TableVersionHeader th
          JOIN   TableVersion tv ON tv.TableVID = th.TableVID
          JOIN   HeaderVersion hv ON hv.HeaderID = th.HeaderID
          JOIN   fw ON fw.table_code = tv.Code
          LEFT JOIN Release rs ON rs.ReleaseID = hv.StartReleaseID
          LEFT JOIN Release re ON re.ReleaseID = hv.EndReleaseID
          WHERE  hv.Code IS NOT NULL
        )
        -- header_id is published because the row is the header, not the code: a page that
        -- groups two rows sharing a code tells the same story this query had to be fixed
        -- for telling.
        SELECT   framework, table_code, row_code, header_id, from_release, to_release,
                 label, start_release_id
        FROM     said
        -- By header and not by row code: a template can serve one code from two headers -
        -- C_17.01.a has both "TOTAL EVENT TYPES" and "Total recovery from insurance" at
        -- 0080 - and those are two rows sharing a code, not a row that was reworded.
        QUALIFY  count(DISTINCT label) OVER (PARTITION BY framework, table_code, header_id) > 1
        """,
        "table_code, row_code, start_release_id",
        partition_by="framework",
    ),
]


def lookup(name: str) -> Published:
    """One published table by name, raising rather than returning None.

    So that a test naming a table turns a rename into a failure instead of quietly
    checking nothing.
    """
    for table in TABLES:
        if table.name == name:
            return table
    raise KeyError(f"{name!r} is not published; there is {', '.join(t.name for t in TABLES)}")


def copy_statement(table: Published, out: Path) -> str:
    """The COPY that writes one table. Pure, so the layout is testable without a database.

    A partitioned table writes a directory of `framework=X/data_0.parquet`; an unpartitioned
    one writes a single file. Both are sorted, because that is what makes the statistics
    worth reading.
    """
    target = out / table.name if table.partition_by else out / f"{table.name}.parquet"
    options = [f"FORMAT parquet, {COMPRESSION}", f"ROW_GROUP_SIZE {ROW_GROUP_SIZE}"]
    if table.partition_by:
        options.append(f"PARTITION_BY ({table.partition_by}), OVERWRITE_OR_IGNORE")
    return f"COPY (SELECT * FROM ({table.sql}) ORDER BY {table.order_by}) TO '{target}' ({', '.join(options)})"


def release_parameters(table: Published, dpm_release: str | None) -> list[str | None]:
    """One pair of parameters per occurrence of the release predicate in the query.

    The predicate is `? IS NULL OR ... asked.Code = ?`, so each occurrence takes the same
    value twice. Counting them rather than hard-coding a number is what keeps a query and
    its parameters together when one of them grows another join.
    """
    return [dpm_release, dpm_release] * (table.sql.count("? IS NULL"))


def published_files(out: Path) -> list[Path]:
    return sorted(path for path in out.rglob("*.parquet") if path.is_file())


def releases_published(root: Path) -> list[str]:
    """The release directories under `root`, newest last, by scanning rather than by
    remembering: a release deleted by hand should disappear from the page too."""
    return sorted(path.name for path in root.iterdir() if path.is_dir() and (path / "manifest.json").is_file())


def manifest(
    out: Path,
    db: Path,
    dpm_release: str | None,
    releases: list[str],
    counts: dict[str, int],
    draft: bool = False,
) -> dict:
    """What was published, from what, and when - the page shows it, and a stale copy is
    otherwise indistinguishable from a current one."""
    files = published_files(out)
    return {
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        # Travels with the data, because a published copy is read where this repository
        # is not: the EBA authorises reproduction provided the source is acknowledged,
        # and a file that does not carry the acknowledgement cannot be reproduced further
        # without someone going to look it up.
        "source_notice": (
            "Derived from the EBA DPM 2.0 database. Reproduction of EBA material is "
            "authorised provided the source is acknowledged "
            "(https://www.eba.europa.eu/legal-notice). Not published by or endorsed by "
            "the EBA; for the database itself, see eba.europa.eu."
        ),
        "source": db.name,
        "dpm_release": dpm_release or "all",
        # A draft technical package is still being changed, so an answer from it is a
        # draft answer. The page says so where the release is chosen, not only here.
        "draft": draft,
        "releases_in_source": releases,
        "row_group_size": ROW_GROUP_SIZE,
        "compression": COMPRESSION,
        "tables": {
            table.name: {
                "rows": counts[table.name],
                "partitioned_by": table.partition_by,
                "bytes": sum(
                    path.stat().st_size for path in files if table.name in path.parts or path.stem == table.name
                ),
            }
            for table in TABLES
        },
        "total_bytes": sum(path.stat().st_size for path in files),
        "files": len(files),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", type=Path, default=DB, help=f"the DPM database to read (default {DB})")
    parser.add_argument("--out", type=Path, default=OUT, help=f"where to write (default {OUT})")
    parser.add_argument("--dpm-release", default=None, help="only what this release ships, e.g. 4.4")
    parser.add_argument(
        "--draft",
        action="store_true",
        help="this release is a draft technical package, so anything built from it is a draft too",
    )
    args = parser.parse_args()

    if not args.db.exists():
        raise SystemExit(f"{args.db} does not exist - run source/fetch_dpm2.py first")
    args.out.mkdir(parents=True, exist_ok=True)

    # A named release gets its own directory; without one, everything goes in the root,
    # which is what a single-release site wants.
    root = args.out
    if args.dpm_release:
        args.out = args.out / args.dpm_release
        args.out.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(args.db), read_only=True)
    try:
        releases = [row[0] for row in con.execute("SELECT Code FROM Release ORDER BY ReleaseID").fetchall()]
        if args.dpm_release and args.dpm_release not in releases:
            raise SystemExit(f"{args.db.name} has no release {args.dpm_release!r}. It has: {', '.join(releases)}")
        counts = {}
        for table in TABLES:
            parameters = release_parameters(table, args.dpm_release)
            counted = con.execute(f"SELECT count(*) FROM ({table.sql})", parameters).fetchone()
            counts[table.name] = counted[0] if counted else 0
            con.execute(copy_statement(table, args.out), parameters)
            print(f"  {table.name:14} {counts[table.name]:>9,} rows", flush=True)
    finally:
        con.close()

    written = manifest(args.out, args.db, args.dpm_release, releases, counts, args.draft)
    (args.out / "manifest.json").write_text(json.dumps(written, indent=2) + "\n", encoding="utf-8")
    if args.dpm_release:
        (root / "releases.json").write_text(json.dumps(releases_published(root), indent=2) + "\n", encoding="utf-8")
    print(f"\n{written['files']} file(s), {written['total_bytes'] / 1e6:.2f} MB in {args.out}")


if __name__ == "__main__":
    main()
