"""The EBA's between-release validation rule updates.

They arrive as SQL over the internet. The property worth protecting is that it is parsed
and never executed: only one statement shape is recognised, and a file with anything else
in it stops rather than applying half a batch of rule deactivations.
"""

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "source"))

import apply_vr_updates  # noqa: E402

DEACTIVATION = (
    "UPDATE OperationScope SET IsActive = 0, Severity = 'warning', "
    "FromSubmissionDate = '13/09/2026' WHERE OperationScopeID IN (11637, 11657);"
)


def test_the_statement_the_eba_publishes_is_understood():
    (update,) = apply_vr_updates.parse(DEACTIVATION)
    assert update.active is False
    assert update.severity == "warning"
    assert update.from_submission_date == date(2026, 9, 13)
    assert update.scope_ids == (11637, 11657)


def test_a_reactivation_is_the_same_statement_the_other_way():
    (update,) = apply_vr_updates.parse(DEACTIVATION.replace("IsActive = 0", "IsActive = 1"))
    assert update.active is True


def test_the_date_is_read_as_the_eba_writes_it():
    """13/09/2026 is the thirteenth of September, not the ninth of the thirteenth."""
    (update,) = apply_vr_updates.parse(DEACTIVATION)
    assert (update.from_submission_date.day, update.from_submission_date.month) == (13, 9)


def test_comments_and_blank_lines_are_not_statements():
    text = f"-- Sync OperationScope IsActive, Severity and FromSubmissionDate\n\n{DEACTIVATION}\n\n"
    assert len(apply_vr_updates.parse(text)) == 1


def test_several_statements_in_one_file():
    assert len(apply_vr_updates.parse(DEACTIVATION * 3)) == 3


@pytest.mark.parametrize(
    "statement",
    [
        "DROP TABLE OperationScope;",
        "UPDATE Operation SET Code = 'x' WHERE OperationID = 1;",
        "UPDATE OperationScope SET IsActive = 0 WHERE OperationScopeID IN (1);",  # no severity, no date
        "UPDATE OperationScope SET IsActive = 0, Severity = 'warning', FromSubmissionDate = '13/09/2026' "
        "WHERE OperationScopeID IN (SELECT OperationScopeID FROM OperationScope);",
        DEACTIVATION + " DELETE FROM Operation;",
    ],
)
def test_anything_else_stops_the_file(statement):
    """Handing fetched SQL to a database is how a dictionary acquires a statement nobody
    read. A half-applied batch is worse than none, so this refuses the whole file."""
    with pytest.raises(SystemExit, match="not a statement this applies"):
        apply_vr_updates.parse(statement)


def test_the_zip_must_hold_exactly_one_script(tmp_path):
    import zipfile

    archive = tmp_path / "two.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("one.sql", DEACTIVATION)
        zf.writestr("two.sql", DEACTIVATION)
    with pytest.raises(SystemExit, match="expected one"):
        apply_vr_updates.read_source(str(archive))


@pytest.mark.parametrize("suffix", [".sql", ".txt"])
def test_either_name_the_eba_uses(tmp_path, suffix):
    """Some packages name the script .sql and others .txt."""
    import zipfile

    archive = tmp_path / f"one{suffix}.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr(f"script{suffix}", DEACTIVATION)
    assert len(apply_vr_updates.parse(apply_vr_updates.read_source(str(archive)))) == 1


def test_a_plain_file_is_read_as_it_is(tmp_path):
    script = tmp_path / "script.sql"
    script.write_text(DEACTIVATION, encoding="utf-8")
    assert apply_vr_updates.read_source(str(script)).strip() == DEACTIVATION


def test_applying_to_a_database_that_is_not_there_says_so(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["apply_vr_updates.py", str(tmp_path / "s.sql"), "--db", str(tmp_path / "no.db")])
    with pytest.raises(SystemExit, match="does not exist"):
        apply_vr_updates.main()


def test_the_effect_is_measured_against_either_spelling_of_true():
    """Release 4.2.1 stores the Access boolean as -1 and later releases as 1. Comparing
    to 1 would report every active scope in 4.2.1 as about to change."""
    import duckdb

    con = duckdb.connect()
    con.execute("CREATE TABLE OperationScope (OperationScopeID INT, IsActive INT, Severity VARCHAR)")
    con.execute("INSERT INTO OperationScope VALUES (1, -1, 'warning'), (2, 1, 'warning'), (3, 0, 'warning')")
    update = apply_vr_updates.Update(True, "warning", date(2026, 9, 13), (1, 2, 3))
    assert apply_vr_updates.effect(con, update) == {"asked": 3, "present": 3, "already": 2}
