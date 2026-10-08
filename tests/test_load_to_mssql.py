"""The connection string, and that a password never reaches a log.

Everything else in the loader talks to a server. These two are pure, and one of them is
the difference between a readable run log and a credential in someone's terminal history.
"""

import pytest

import load_to_mssql as L
from conftest import DPM2_DB, needs_dpm2
from load_to_mssql import Settings, connection_string, redacted


def settings(**over):
    return Settings(server="dbhost.example", **over)


def test_kerberos_is_the_default_and_needs_no_credentials():
    assert connection_string(settings()) == (
        "Server=dbhost.example,1433;Database=DPM2;Trusted_Connection=yes;Encrypt=yes"
    )


def test_a_sql_login_is_used_when_the_trusted_connection_is_turned_off():
    got = connection_string(settings(trusted_connection=False, username="u", password="p"))
    assert "User Id=u;Password=p" in got
    assert "Trusted_Connection" not in got


def test_a_sql_login_without_credentials_is_refused_rather_than_attempted():
    with pytest.raises(SystemExit, match="MSSQL_USERNAME and MSSQL_PASSWORD"):
        connection_string(settings(trusted_connection=False))


def test_no_server_is_refused():
    with pytest.raises(SystemExit, match="MSSQL_SERVER is not set"):
        connection_string(Settings(server=None))


@pytest.mark.parametrize(
    ("over", "expected"),
    [
        ({"port": 1444}, "Server=dbhost.example,1444"),
        ({"database": "Model"}, "Database=Model"),
        ({"encrypt": False}, "Encrypt=no"),
        ({"trust_server_certificate": True}, "TrustServerCertificate=yes"),
    ],
)
def test_the_settings_reach_the_string(over, expected):
    assert expected in connection_string(settings(**over))


def test_the_password_is_not_printed():
    """The loader prints the string it will use; this is what makes that safe."""
    secret = "hunter2-not-in-a-log"  # noqa: S105 - a test value, not a credential
    full = connection_string(settings(trusted_connection=False, username="u", password=secret))
    assert secret in full
    assert secret not in redacted(full)
    assert "Password=***" in redacted(full)


def test_redacting_leaves_everything_else_alone():
    assert redacted("Server=a,1433;Database=b;Encrypt=yes") == "Server=a,1433;Database=b;Encrypt=yes"


def test_the_schema_setting_is_not_called_schema():
    """`schema` shadows Pydantic's own, so the field is db_schema."""
    assert "db_schema" in Settings.model_fields
    assert L.Settings.model_config["env_prefix"] == "MSSQL_"


@pytest.mark.parametrize("name", ["MSSQL_SCHEMA", "MSSQL_DB_SCHEMA"])
def test_both_names_for_the_schema_work(monkeypatch, name):
    """MSSQL_SCHEMA is what anyone would reach for, and before the alias it was accepted
    and ignored - the loader wrote to dpm while the environment said otherwise."""
    monkeypatch.setenv("MSSQL_SERVER", "dbhost.example")
    monkeypatch.setenv(name, "chosen")
    assert Settings().db_schema == "chosen"


def test_the_schema_defaults_to_dpm():
    assert settings().db_schema == "dpm"


# --- the connection, which is where this went wrong -----------------------------------


@needs_dpm2
def test_the_source_is_attached_read_only_but_the_instance_is_not(tmp_path):
    """The reported failure: `cannot execute mssql_exec: catalog ms is attached in read
    only mode`. A read-only DuckDB instance refuses to attach any writable catalog, so
    opening the dictionary read-only made the SQL Server side read-only too.

    SQL Server is not needed to pin this down - the refusal came from DuckDB. Attaching a
    writable catalog and writing to it is the capability that was missing.
    """
    con = L.open_source(DPM2_DB)
    try:
        con.execute(f"ATTACH '{tmp_path / 'target.duckdb'}' AS target")
        con.execute("CREATE TABLE target.t AS SELECT 1 AS a")
        assert con.execute("SELECT count(*) FROM target.t").fetchone() == (1,)
    finally:
        con.close()


@needs_dpm2
def test_the_source_itself_stays_read_only():
    """The property the read-only connection was there for, kept deliberately."""
    con = L.open_source(DPM2_DB)
    try:
        with pytest.raises(Exception, match="read.only|Cannot execute statement"):
            con.execute(f"CREATE TABLE {L.SOURCE}.scribble AS SELECT 1 AS a")
    finally:
        con.close()


@needs_dpm2
def test_the_dictionary_is_visible_under_its_alias():
    con = L.open_source(DPM2_DB)
    try:
        tables = L.source_tables(con)
    finally:
        con.close()
    assert len(tables) == 73, "the DPM 2.0 release has 73 tables"
    assert tables["Cell"] > 0
