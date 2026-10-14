"""The decision of whether to export, which is what went wrong.

The guard used to be `not CSV_DIR.exists()`. A directory that exists says nothing about
whether the export inside it finished, so an empty or partial one was read as "already
done" and DuckDB was then told to read a file that was never written.
"""

import pytest

import fetch_dpm2


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


# --- where a release lands --------------------------------------------------------------


def test_the_default_release_keeps_the_names_it_has_always_had(tmp_path, monkeypatch):
    """Making the release configurable must not orphan a copy already downloaded."""
    monkeypatch.delenv("DPM2_DB", raising=False)
    here = fetch_dpm2.paths_for(fetch_dpm2.DEFAULT_RELEASE, tmp_path)
    assert here.csv_dir == tmp_path / "csv"
    assert here.db == tmp_path / "dpm2.duckdb"


def test_another_release_cannot_collide_with_it(tmp_path, monkeypatch):
    """Two releases are separate downloads of overlapping content, so every file of one
    has to be distinct from the other's - the CSV directory above all, since a half-mixed
    export would load without complaint."""
    monkeypatch.delenv("DPM2_DB", raising=False)
    default = fetch_dpm2.paths_for(fetch_dpm2.DEFAULT_RELEASE, tmp_path)
    other = fetch_dpm2.paths_for("4.3", tmp_path)
    assert set(default) & set(other) == set()
    assert other.csv_dir == tmp_path / "csv_4_3"
    assert other.db == tmp_path / "dpm2_4_3.duckdb"


def test_the_environment_still_wins(tmp_path, monkeypatch):
    """A caller naming one file means that file, whichever release is being fetched."""
    monkeypatch.setenv("DPM2_DB", str(tmp_path / "chosen.duckdb"))
    for release in (fetch_dpm2.DEFAULT_RELEASE, "4.3"):
        assert fetch_dpm2.paths_for(release, tmp_path).db == tmp_path / "chosen.duckdb"


def test_every_source_has_a_url_and_the_default_is_one_of_them():
    assert fetch_dpm2.DEFAULT_RELEASE in fetch_dpm2.SOURCES
    assert all(source.url.startswith("https://") for source in fetch_dpm2.SOURCES.values())
    assert fetch_dpm2.SOURCES[fetch_dpm2.DEFAULT_RELEASE].sha256, "the default release is pinned"
