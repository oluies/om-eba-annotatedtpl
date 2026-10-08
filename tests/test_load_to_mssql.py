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


# --- the indexes -----------------------------------------------------------------------


def test_a_unique_key_becomes_the_clustered_index():
    """Cell also joins out through TableID, RowID, ColumnID and SheetID, so the clustered
    one is the first of several rather than the only one."""
    plan = L.index_plan({("Cell", "CellID")}, ["Cell"])
    assert plan[0] == L.Index("Cell", ("CellID",), unique=True)
    assert "UNIQUE CLUSTERED" in plan[0].statement("dpm")
    assert sum(1 for i in plan if i.unique) == 1


def test_a_join_column_becomes_a_non_clustered_index():
    plan = L.index_plan(set(), ["ContextComposition"])
    columns = {i.columns[0] for i in plan if i.table == "ContextComposition"}
    assert {"ContextID", "ItemID", "PropertyID"} <= columns
    assert not any(i.unique for i in plan)


def test_a_column_that_is_both_is_indexed_once():
    """Property.PropertyID is its own identity and a join into Item."""
    plan = L.index_plan({("Property", "PropertyID")}, ["Property"])
    on_propertyid = [i for i in plan if i.columns == ("PropertyID",)]
    assert len(on_propertyid) == 1
    assert on_propertyid[0].unique


def test_nothing_is_planned_for_a_table_that_was_not_loaded():
    assert L.index_plan({("Cell", "CellID")}, ["Concept"]) == []


def test_the_clustered_index_comes_before_its_tables_others():
    """Creating it afterwards rebuilds every non-clustered index already there."""
    plan = L.index_plan({("VariableVersion", "VariableVID")}, ["VariableVersion"])
    first = next(i for i, ix in enumerate(plan) if ix.unique)
    others = [i for i, ix in enumerate(plan) if not ix.unique and ix.table == "VariableVersion"]
    assert all(first < o for o in others)


def test_a_reserved_word_column_is_bracketed():
    """The model has columns called Table, Row, Column and Order."""
    statement = L.Index("OperandReferenceLocation", ("Table",), unique=False).statement("dpm")
    assert "([Table])" in statement


def test_the_statement_is_a_no_op_the_second_time():
    statement = L.Index("Cell", ("CellID",), unique=True).statement("dpm")
    assert statement.startswith("IF NOT EXISTS (SELECT 1 FROM sys.indexes")
    assert "OBJECT_ID('[dpm].[Cell]')" in statement


def test_the_schema_reaches_the_statement():
    assert "[other].[Cell]" in L.Index("Cell", ("CellID",), unique=True).statement("other")


@needs_dpm2
def test_the_whole_plan_is_valid_t_sql():
    """Sixty-two statements that will be sent to a server, parsed before they are."""
    import sqlfluff

    con = L.open_source(DPM2_DB)
    try:
        tables = list(L.source_tables(con))
        plan = L.index_plan(L.unique_parent_keys(con, tables), tables)
    finally:
        con.close()
    assert len(plan) > 50
    for index in plan:
        sqlfluff.parse(index.statement("dpm"), dialect="tsql")


@needs_dpm2
def test_every_identity_column_measures_unique():
    """The plan calls them unique, so a unique index would fail the load if they were not."""
    con = L.open_source(DPM2_DB)
    try:
        tables = list(L.source_tables(con))
        found = L.unique_parent_keys(con, tables)
    finally:
        con.close()
    assert len(found) == 21


# --- the two things only a real server found -------------------------------------------


def test_a_text_column_is_narrowed_before_it_is_indexed():
    """CTAS maps a DuckDB VARCHAR to nvarchar(max), and SQL Server answers error 1919:
    a MAX type cannot be an index key. sqlfluff parses the CREATE INDEX happily, because
    the statement is fine and only the column type is wrong, so only a server found it."""
    assert L.narrowing("dpm", "TableVersion", "Code", 64) == (
        "ALTER TABLE [dpm].[TableVersion] ALTER COLUMN [Code] nvarchar(64)"
    )


def test_a_reserved_word_column_is_bracketed_when_narrowed_too():
    assert "[Table] nvarchar(" in L.narrowing("dpm", "OperandReferenceLocation", "Table", 64)


@needs_dpm2
def test_only_the_indexed_text_columns_are_narrowed(monkeypatch):
    con = L.open_source(DPM2_DB)
    try:
        tables = list(L.source_tables(con))
        plan = L.index_plan(L.unique_parent_keys(con, tables), tables)
        widths = L.string_widths(con, plan)
    finally:
        con.close()
    # Seven of the sixty-three indexed columns hold text; the rest are bigint or date.
    assert len(widths) == 7
    assert widths[("TableVersionCell", "CellCode")] >= 32, "the longest cell code is 32 characters"
    assert all(64 <= w <= L.MAX_KEY_CHARS for w in widths.values())


@needs_dpm2
def test_a_width_leaves_room_but_stays_inside_the_index_key_limit():
    """Doubled with a floor, so a later release with longer codes still loads; capped, so
    the key stays inside SQL Server's limit at two bytes a character."""
    con = L.open_source(DPM2_DB)
    try:
        plan = [L.Index("TableVersionCell", ("CellCode",), unique=False)]
        width = L.string_widths(con, plan)[("TableVersionCell", "CellCode")]
    finally:
        con.close()
    assert width == 64, "32 characters doubled"
    assert width * 2 < 1700, "two bytes a character, inside the non-clustered key limit"
