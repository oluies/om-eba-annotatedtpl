"""The decision of whether to export, which is what went wrong.

The guard used to be `not CSV_DIR.exists()`. A directory that exists says nothing about
whether the export inside it finished, so an empty or partial one was read as "already
done" and DuckDB was then told to read a file that was never written.
"""

import sys

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


# --- a download that changed under the files made from it --------------------------------


def test_each_release_records_what_its_derived_files_came_from(tmp_path, monkeypatch):
    monkeypatch.delenv("DPM2_DB", raising=False)
    here = fetch_dpm2.paths_for("4.4", tmp_path)
    assert here.stamp == tmp_path / "dpm2_4_4.accdb.sha256"
    assert here.stamp != here.accdb


def test_the_stamp_is_distinct_per_release(tmp_path, monkeypatch):
    monkeypatch.delenv("DPM2_DB", raising=False)
    stamps = {fetch_dpm2.paths_for(release, tmp_path).stamp for release in ("4.2.1", "4.3", "4.4")}
    assert len(stamps) == 3


def test_a_changed_download_redoes_the_unpack_and_the_export(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("DPM2_DB", raising=False)
    """The failure this prevents: the EBA revises a draft in place, the recorded hash is
    updated, the stale zip is deleted, and the next run downloads the new file and then
    reuses the old draft's .accdb and CSVs - a database labelled 4.4 holding the draft
    before it. Every step here keys on a file existing, so only the digest can say."""
    redone = []
    here = fetch_dpm2.paths_for("4.4", tmp_path)
    tmp_path.mkdir(exist_ok=True)
    here.zip.write_bytes(b"the new draft")
    here.accdb.write_bytes(b"the old draft")
    here.csv_dir.mkdir(parents=True)
    (here.csv_dir / "Cell.csv").write_text("CellID\n1\n", encoding="utf-8")
    here.stamp.write_text("a-hash-from-the-draft-before-this-one\n", encoding="utf-8")

    monkeypatch.setattr(fetch_dpm2, "paths_for", lambda release, directory=tmp_path: here)
    monkeypatch.setattr(fetch_dpm2, "DIR", tmp_path)
    monkeypatch.setattr(fetch_dpm2, "unpack", lambda archive, target: redone.append("unpack"))
    monkeypatch.setattr(fetch_dpm2, "table_names", lambda accdb: ("Cell",))
    monkeypatch.setattr(fetch_dpm2, "export", lambda accdb, names, out: redone.append(("export", tuple(names))))
    monkeypatch.setattr(fetch_dpm2, "load", lambda csv_dir, names, db: {"Cell": 1})
    monkeypatch.setattr(fetch_dpm2, "SOURCES", {"4.4": fetch_dpm2.Source(url="https://example/x.zip", sha256="")})
    monkeypatch.setattr(sys, "argv", ["fetch_dpm2.py", "--release", "4.4"])
    here.db.write_bytes(b"")

    fetch_dpm2.main()

    assert "unpack" in redone, "the new download was not unpacked"
    assert ("export", ("Cell",)) in redone, "the old draft's CSVs were reused"
    assert here.stamp.read_text(encoding="utf-8").strip() == fetch_dpm2.digest(here.zip)


def test_an_unchanged_download_leaves_the_derived_files_alone(tmp_path, monkeypatch):
    monkeypatch.delenv("DPM2_DB", raising=False)
    """The other half: re-running must not re-export 72 tables for nothing."""
    redone = []
    here = fetch_dpm2.paths_for("4.4", tmp_path)
    here.zip.write_bytes(b"the same draft")
    here.accdb.write_bytes(b"unpacked already")
    here.csv_dir.mkdir(parents=True)
    (here.csv_dir / "Cell.csv").write_text("CellID\n1\n", encoding="utf-8")
    here.stamp.write_text(fetch_dpm2.digest(here.zip) + "\n", encoding="utf-8")

    monkeypatch.setattr(fetch_dpm2, "paths_for", lambda release, directory=tmp_path: here)
    monkeypatch.setattr(fetch_dpm2, "DIR", tmp_path)
    monkeypatch.setattr(fetch_dpm2, "unpack", lambda archive, target: redone.append("unpack"))
    monkeypatch.setattr(fetch_dpm2, "table_names", lambda accdb: ("Cell",))
    monkeypatch.setattr(fetch_dpm2, "export", lambda accdb, names, out: redone.append("export"))
    monkeypatch.setattr(fetch_dpm2, "load", lambda csv_dir, names, db: {"Cell": 1})
    monkeypatch.setattr(fetch_dpm2, "SOURCES", {"4.4": fetch_dpm2.Source(url="https://example/x.zip", sha256="")})
    monkeypatch.setattr(sys, "argv", ["fetch_dpm2.py", "--release", "4.4"])
    here.db.write_bytes(b"")

    fetch_dpm2.main()
    assert redone == [], f"nothing had changed, but it redid {redone}"


def test_a_hash_that_does_not_match_says_what_to_do(tmp_path, monkeypatch):
    monkeypatch.delenv("DPM2_DB", raising=False)
    here = fetch_dpm2.paths_for("4.4", tmp_path)
    here.zip.write_bytes(b"not what was recorded")
    monkeypatch.setattr(fetch_dpm2, "paths_for", lambda release, directory=tmp_path: here)
    monkeypatch.setattr(fetch_dpm2, "DIR", tmp_path)
    monkeypatch.setattr(fetch_dpm2, "SOURCES", {"4.4": fetch_dpm2.Source(url="https://example/x.zip", sha256="0" * 64)})
    monkeypatch.setattr(sys, "argv", ["fetch_dpm2.py", "--release", "4.4"])
    with pytest.raises(SystemExit, match="record") as refused:
        fetch_dpm2.main()
    assert "delete" in str(refused.value), "the other remedy is not named"
