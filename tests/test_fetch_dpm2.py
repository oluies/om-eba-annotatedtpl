"""The decision of whether to export, which is what went wrong.

The guard used to be `not CSV_DIR.exists()`. A directory that exists says nothing about
whether the export inside it finished, so an empty or partial one was read as "already
done" and DuckDB was then told to read a file that was never written.
"""

import fetch_dpm2
import pytest


def test_nothing_exported_yet(tmp_path):
    assert fetch_dpm2.missing_csvs(("Cell", "Concept"), tmp_path) == ["Cell", "Concept"]


def test_a_directory_that_exists_but_is_empty_is_still_missing_everything(tmp_path):
    """The user-reported failure: the directory was there, the exports were not."""
    (tmp_path / "csv").mkdir()
    assert fetch_dpm2.missing_csvs(("Cell",), tmp_path / "csv") == ["Cell"]


def test_a_partial_export_reports_only_what_is_absent(tmp_path):
    (tmp_path / "Cell.csv").write_text("CellID\n1\n")
    assert fetch_dpm2.missing_csvs(("Cell", "Concept"), tmp_path) == ["Concept"]


def test_a_complete_export_is_left_alone(tmp_path):
    for name in ("Cell", "Concept"):
        (tmp_path / f"{name}.csv").write_text("a\n1\n")
    assert fetch_dpm2.missing_csvs(("Cell", "Concept"), tmp_path) == []


def test_a_part_file_does_not_count_as_exported(tmp_path):
    """export() writes a .part and renames, so an interrupted write is not mistaken."""
    (tmp_path / "Cell.csv.part").write_text("truncated")
    assert fetch_dpm2.missing_csvs(("Cell",), tmp_path) == ["Cell"]


def test_load_refuses_rather_than_letting_duckdb_fail_on_a_missing_file(tmp_path):
    with pytest.raises(SystemExit, match="no export for Cell"):
        fetch_dpm2.load(tmp_path, ("Cell",), tmp_path / "out.duckdb")
