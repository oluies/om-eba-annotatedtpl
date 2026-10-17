"""The parquet tree a browser queries.

The layout is the whole design: sorted on the column the questions filter by, split by
framework, so DuckDB-WASM reads a few hundred kB over HTTP instead of a file. Measured in
a browser before it was written - unsorted, six questions pulled 32.9 MB; sorted and
partitioned, seven questions pulled 1.8 MB.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "source"))

import gen_wasm_data as gen  # noqa: E402

from conftest import needs_dpm2  # noqa: E402


def test_every_table_is_sorted_on_what_it_is_filtered_by():
    """Statistics prune only what is clustered, so an unsorted file is read whole."""
    for table in gen.TABLES:
        assert table.order_by, table.name
        first = table.order_by.split(",")[0].strip()
        assert first in table.sql, f"{table.name} sorts by {first}, which it does not select"


def test_the_big_tables_are_split_by_framework():
    """A question concerns one framework, so it should read one partition."""
    partitioned = {table.name for table in gen.TABLES if table.partition_by == "framework"}
    assert partitioned == {"cells", "cell_members", "rule_cells"}


@pytest.mark.parametrize("table", gen.TABLES, ids=lambda table: table.name)
def test_the_copy_statement_carries_the_layout(table, tmp_path):
    statement = gen.copy_statement(table, tmp_path)
    assert f"ROW_GROUP_SIZE {gen.ROW_GROUP_SIZE}" in statement
    assert gen.COMPRESSION in statement
    assert f"ORDER BY {table.order_by}" in statement
    if table.partition_by:
        assert "PARTITION_BY (framework)" in statement
        assert str(tmp_path / table.name) in statement
    else:
        assert str(tmp_path / f"{table.name}.parquet") in statement


@pytest.mark.parametrize("table", gen.TABLES, ids=lambda table: table.name)
def test_the_release_predicate_gets_its_parameters(table):
    """The predicate is `? IS NULL OR ... = ?`, twice per occurrence. Counting them keeps
    a query and its parameters together when one of them grows another join."""
    assert gen.release_parameters(table, None) == [None, None] * table.sql.count("? IS NULL")
    assert gen.release_parameters(table, "4.4") == ["4.4", "4.4"] * table.sql.count("? IS NULL")


def test_an_excluded_cell_is_not_published():
    """A greyed-out box is in the model and not reportable. The pack leaves them out, so
    a count of cells here must mean the same thing."""
    cells = next(table for table in gen.TABLES if table.name == "cells")
    assert "IsExcluded = 0" in cells.sql


def test_the_property_code_is_the_one_in_force():
    """233 properties have been recoded; an unscoped join returns a header once per code
    it has ever had."""
    headers = next(table for table in gen.TABLES if table.name == "headers")
    assert "ic.EndReleaseID IS NULL" in headers.sql


@needs_dpm2
def test_a_generated_tree_answers_and_carries_a_manifest(tmp_path):
    """End to end against the real model, for one framework's worth of questions."""
    import duckdb

    import dpm_lookup

    sys.argv = ["gen_wasm_data.py", "--db", str(dpm_lookup.DB), "--out", str(tmp_path), "--dpm-release", "4.2"]
    gen.main()

    written = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert written["dpm_release"] == "4.2"
    assert written["source"] == dpm_lookup.DB.name
    assert written["total_bytes"] > 0
    assert set(written["tables"]) == {table.name for table in gen.TABLES}

    con = duckdb.connect()
    answer = con.execute(
        f"SELECT severity, active FROM '{tmp_path}/rules.parquet' WHERE rule_code = 'v0174_m' AND module = 'COREP_OF'"
    ).fetchall()
    assert answer, "the rule is in release 4.2"
    con.close()


@needs_dpm2
def test_a_release_the_database_does_not_have_is_refused(tmp_path):
    import dpm_lookup

    sys.argv = ["gen_wasm_data.py", "--db", str(dpm_lookup.DB), "--out", str(tmp_path), "--dpm-release", "9.9"]
    with pytest.raises(SystemExit, match="no release"):
        gen.main()


def test_the_sums_recursion_is_prefiltered_and_version_free():
    """Two things make it finish. Only rules that can be sums enter the recursion - a
    root `=` with a `+` under it - and the shape is resolved per operation version with
    the module versions joined on afterwards. Carrying module and version through the
    recursion multiplies 48k nodes by the versions each rule belongs to, which is the
    difference between 0.1s and not finishing inside ten minutes."""
    sums = next(table for table in gen.TABLES if table.name == "sums")
    recursion = sums.sql[: sums.sql.index("), edges AS (")]
    assert "arith AS (" in sums.sql, "the prefilter"
    assert "Symbol = '='" in sums.sql and "Symbol = '+'" in sums.sql
    assert "ModuleVersion" not in recursion, "module versions must not enter the recursion"
    assert "ModuleVersion" in sums.sql, "they are joined on after it"


@needs_dpm2
def test_the_sums_match_what_the_lookup_says(tmp_path):
    """The page's answer has to be the tool's answer: F_12.01.a row 0010 is rows 0020 and
    0080 added together, under rule v23845_h."""
    import duckdb

    import dpm_lookup

    sys.argv = ["gen_wasm_data.py", "--db", str(dpm_lookup.DB), "--out", str(tmp_path), "--dpm-release", "4.2"]
    gen.main()

    con = duckdb.connect()
    published = con.execute(
        f"""SELECT total_row, addend_rows, rule_code FROM '{tmp_path}/sums.parquet'
            WHERE table_code = 'F_12.01.a' AND module = 'FINREP9' AND total_row = '0010'"""
    ).fetchall()
    con.close()
    assert published, "the lookup finds sums for this template"
    (total, addends, rule) = published[0]
    assert (total, list(addends)) == ("0010", ["0020", "0080"])
    assert rule == "v23845_h"

    from_tool = dpm_lookup.lookup_dpm_sums("F 12.01.a", "FINREP9")
    matching = [row for row in from_tool["sums"] if row["total_row"] == "0010"]
    assert matching and matching[0]["addend_rows"] == ["0020", "0080"]
