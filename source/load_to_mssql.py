"""Load the local DPM 2.0 database into SQL Server, through DuckDB's mssql extension.

Why bother, when the dictionary is already queryable in DuckDB: a warehouse's reported
figures live in SQL Server, and `dp<N>` in an xBRL-CSV report is `VariableID` in the
model. With both in one database the join from a reported value to the cell it reports,
and to the rules constraining it, is a view rather than an export.

    uv run source/load_to_mssql.py                      # what it would do, contacting nothing
    uv run source/load_to_mssql.py --commit             # create what is missing
    uv run source/load_to_mssql.py --commit --replace   # and drop what is already there
    uv run source/load_to_mssql.py --tables Cell Concept --commit

Nothing is written without `--commit`, and an existing table is left alone unless
`--replace` says otherwise: this writes to someone else's database, and a silent DROP
there is not recoverable from here.

A CTAS leaves a heap, so the load also creates 62 indexes - 21 clustered on the identity
columns and 41 on everything the queries in README_DPM2.md join or filter through. Without
them every one of those joins is a table scan over up to 1.7 million rows. `--no-indexes`
skips that if you would rather index by hand.

The extension speaks TDS directly, so no ODBC driver is needed. With `MSSQL_SERVER` set
and nothing else, it authenticates with your Kerberos ticket - `Trusted_Connection=yes`
resolves to `authenticator=krb5` on POSIX - which is the same ticket `ba_form_cell.py`
uses. Run `kinit` first.
"""

import argparse
import os
import sys
from collections.abc import Collection
from pathlib import Path
from typing import NamedTuple

import duckdb
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from gen_dpm2_doc import REL

REPO = Path(__file__).resolve().parent.parent
DIR = Path(os.environ.get("DPM2_DIR") or REPO / "source" / "dpm2")
DPM2 = Path(os.environ.get("DPM2_DB") or DIR / "dpm2.duckdb")


class Settings(BaseSettings):
    """Where to load, and how to authenticate. Only the server has no sensible default."""

    model_config = SettingsConfigDict(env_prefix="MSSQL_", env_file=".env", extra="ignore")

    server: str | None = None
    port: int = 1433
    database: str = "DPM2"
    # `schema` is taken by Pydantic, so the field is db_schema - but MSSQL_SCHEMA is the
    # name anyone would reach for, and without the alias it is accepted and ignored.
    db_schema: str = Field("dpm", validation_alias=AliasChoices("MSSQL_SCHEMA", "MSSQL_DB_SCHEMA"))
    # Kerberos by default: the same ticket the warehouse overlay uses, and no password to
    # keep anywhere. Set MSSQL_TRUSTED_CONNECTION=false to use a SQL login instead.
    trusted_connection: bool = True
    username: str | None = None
    password: str | None = None
    encrypt: bool = True
    trust_server_certificate: bool = False


SETTINGS = Settings()


class Loaded(BaseModel):
    """What one table's load came to, as both sides counted it."""

    model_config = ConfigDict(frozen=True)

    table: str
    source_rows: int
    target_rows: int
    action: str

    @property
    def agrees(self) -> bool:
        return self.source_rows == self.target_rows


def connection_string(settings: Settings) -> str:
    """The ATTACH string. Pure, so what would be sent can be shown without sending it."""
    if not settings.server:
        raise SystemExit("MSSQL_SERVER is not set - there is nothing to connect to")
    parts = [f"Server={settings.server},{settings.port}", f"Database={settings.database}"]
    if settings.trusted_connection:
        parts.append("Trusted_Connection=yes")
    else:
        if not (settings.username and settings.password):
            raise SystemExit("MSSQL_TRUSTED_CONNECTION is false, so MSSQL_USERNAME and MSSQL_PASSWORD are needed")
        parts += [f"User Id={settings.username}", f"Password={settings.password}"]
    parts.append(f"Encrypt={'yes' if settings.encrypt else 'no'}")
    if settings.trust_server_certificate:
        parts.append("TrustServerCertificate=yes")
    return ";".join(parts)


def redacted(connection: str) -> str:
    """The same string with the password removed, for printing."""
    return ";".join("Password=***" if p.lower().startswith("password=") else p for p in connection.split(";"))


# The dictionary is attached under this name rather than opened as the main database.
SOURCE = "src"


def open_source(path: Path) -> duckdb.DuckDBPyConnection:
    """A writable in-memory connection with the dictionary attached read-only.

    Not a read-only connection to the file, which was the first attempt: a read-only
    DuckDB instance refuses to attach any writable catalog, so the SQL Server side came
    back `cannot execute mssql_exec: catalog ms is attached in read only mode`. In memory,
    the source being read-only is stated about the source rather than inherited from how
    the connection happened to be opened - which is what it was meant to say all along.
    """
    con = duckdb.connect()
    con.execute(f"ATTACH '{path}' AS {SOURCE} (READ_ONLY)")
    return con


def source_tables(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    """Every table in the local copy, with its row count."""
    return dict(
        con.execute(
            "SELECT table_name, estimated_size FROM duckdb_tables() WHERE database_name = ? ORDER BY table_name",
            [SOURCE],
        ).fetchall()
    )


# Columns the documented queries filter on rather than join through, so the relationship
# model does not know about them. Each one is in a WHERE in README_DPM2.md.
LOOKUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("TableVersion", ("Code",)),
    ("ModuleVersion", ("Code", "VersionNumber")),
    ("Operation", ("Code",)),
    ("TableVersionCell", ("CellCode",)),
    ("OperandReferenceLocation", ("Table",)),
    ("Header", ("Direction",)),
)


class Index(NamedTuple):
    """One index to create. Clustered where the column is the table's identity."""

    table: str
    columns: tuple[str, ...]
    unique: bool

    @property
    def name(self) -> str:
        return f"{'CX' if self.unique else 'IX'}_{self.table}_{'_'.join(self.columns)}"[:128]

    def statement(self, schema: str) -> str:
        """T-SQL, guarded so a second run is a no-op. Columns are bracketed because the
        model has columns called Table, Row, Column and Order, all reserved words."""
        cols = ", ".join(f"[{c}]" for c in self.columns)
        kind = "UNIQUE CLUSTERED" if self.unique else "NONCLUSTERED"
        target = f"[{schema}].[{self.table}]"
        return (
            f"IF NOT EXISTS (SELECT 1 FROM sys.indexes "
            f"WHERE name = '{self.name}' AND object_id = OBJECT_ID('{target}')) "
            f"CREATE {kind} INDEX [{self.name}] ON {target} ({cols})"
        )


def index_plan(unique_keys: set[tuple[str, str]], tables: Collection[str]) -> list[Index]:
    """What to index, derived from the verified relationship model rather than guessed.

    Pure. A parent key that measures unique and not null becomes the clustered index -
    the table's physical order - and every column something joins through becomes a
    non-clustered one. Clustered first per table: creating it afterwards would rebuild
    every non-clustered index that already existed.

    A unique index rather than a primary key, because CTAS leaves every column nullable
    and a PK would need an ALTER COLUMN first. SQL Server permits one NULL in a unique
    index, and these columns have none.
    """
    planned: list[Index] = [
        Index(table, (column,), unique=True) for table, column in sorted(unique_keys) if table in tables
    ]
    already = {(i.table, i.columns) for i in planned}
    for rel in sorted({(r.child, r.key) for r in REL}):
        candidate = Index(rel[0], (rel[1],), unique=False)
        if rel[0] in tables and (candidate.table, candidate.columns) not in already:
            planned.append(candidate)
            already.add((candidate.table, candidate.columns))
    for table, columns in LOOKUPS:
        candidate = Index(table, columns, unique=False)
        if table in tables and (candidate.table, candidate.columns) not in already:
            planned.append(candidate)
            already.add((candidate.table, candidate.columns))
    return planned


def unique_parent_keys(con: duckdb.DuckDBPyConnection, tables: Collection[str]) -> set[tuple[str, str]]:
    """Which identity columns are actually unique and never null, measured not assumed."""
    found = set()
    for table, column in sorted({(r.parent, r.parent_key) for r in REL}):
        if table not in tables:
            continue
        counted = con.execute(
            f'SELECT count(*), count(DISTINCT "{column}"), count(*) FILTER (WHERE "{column}" IS NULL) '
            f'FROM {SOURCE}."{table}"'
        ).fetchone()
        if counted and counted[0] == counted[1] and counted[2] == 0:
            found.add((table, column))
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true", help="write for real; dry run only without it")
    parser.add_argument(
        "--replace", action="store_true", help="drop a table that already exists instead of skipping it"
    )
    parser.add_argument("--tables", nargs="*", help="only these tables; all of them by default")
    parser.add_argument("--no-indexes", action="store_true", help="load the data and index nothing")
    args = parser.parse_args()

    if not DPM2.exists():
        raise SystemExit(f"{DPM2} does not exist - run source/fetch_dpm2.py first")

    connection = connection_string(SETTINGS)
    con = open_source(DPM2)
    available = source_tables(con)
    wanted = args.tables or sorted(available)
    if unknown := [t for t in wanted if t not in available]:
        raise SystemExit(f"not in {DPM2.name}: {', '.join(unknown)}")

    target = f"{SETTINGS.database}.{SETTINGS.db_schema}"
    print(f"{DPM2.name}: {len(wanted)} table(s), {sum(available[t] for t in wanted):,} rows".replace(",", " "))
    print(f"into {target} on {SETTINGS.server} as {redacted(connection)}")

    if not args.commit:
        print("\nwould create, in this order:")
        for table in wanted:
            print(f"  {target}.{table:28} {available[table]:>9,} rows".replace(",", " "))
        if not args.no_indexes:
            planned = index_plan(unique_parent_keys(con, wanted), wanted)
            clustered = sum(1 for i in planned if i.unique)
            print(f"\nand then {len(planned)} index(es): {clustered} clustered, {len(planned) - clustered} not")
            for index in planned[:3]:
                print(f"  {index.statement(SETTINGS.db_schema)[:150]}")
            if len(planned) > 3:
                print(f"  ... and {len(planned) - 3} more")
        also = "" if args.replace else " (and --replace to drop tables that already exist)"
        print(f"\nNothing written. Re-run with --commit{also}.")
        return

    con.execute("LOAD mssql")
    con.execute(f"ATTACH '{connection}' AS ms (TYPE mssql)")
    # The schema has to exist before a three-part CTAS can land in it, and the extension
    # has no DDL for that - mssql_exec is the way to send plain T-SQL.
    con.execute(
        "SELECT mssql_exec('ms', ?)",
        [f"IF SCHEMA_ID('{SETTINGS.db_schema}') IS NULL EXEC('CREATE SCHEMA {SETTINGS.db_schema}')"],
    )

    existing = {
        row[0]
        for row in con.execute(
            "SELECT table_name FROM duckdb_tables() WHERE database_name = 'ms' AND schema_name = ?",
            [SETTINGS.db_schema],
        ).fetchall()
    }

    results: list[Loaded] = []
    for table in wanted:
        qualified = f'ms.{SETTINGS.db_schema}."{table}"'
        if table in existing:
            if not args.replace:
                print(f"  {table:28} exists, left alone")
                continue
            con.execute(f"DROP TABLE {qualified}")
        # CTAS streams through the extension's bulk path; an INSERT above 1000 rows goes
        # through BCP, so there is nothing to batch by hand.
        con.execute(f'CREATE TABLE {qualified} AS SELECT * FROM {SOURCE}."{table}"')
        counted = con.execute(f"SELECT count(*) FROM {qualified}").fetchone()
        results.append(
            Loaded(
                table=table,
                source_rows=available[table],
                target_rows=counted[0] if counted else -1,
                action="replaced" if table in existing else "created",
            )
        )
        print(f"  {table:28} {results[-1].action:9} {results[-1].target_rows:>9,} rows".replace(",", " "))

    # Indexes after the data, and the clustered one before the rest of its table's:
    # creating it afterwards rebuilds every non-clustered index already there. CTAS leaves
    # a heap, so without this every join in README_DPM2.md is a scan.
    if not args.no_indexes and results:
        planned = index_plan(unique_parent_keys(con, wanted), [r.table for r in results])
        for index in planned:
            con.execute("SELECT mssql_exec('ms', ?)", [index.statement(SETTINGS.db_schema)])
        clustered = sum(1 for i in planned if i.unique)
        print(f"  {len(planned)} index(es) in place: {clustered} clustered, {len(planned) - clustered} not")

    con.close()

    # Counted on both sides rather than assumed: a CTAS that lands short is the failure
    # this is most likely to have, and it does not raise.
    disagreed = [r for r in results if not r.agrees]
    print(f"\n{len(results)} table(s) loaded, {sum(r.target_rows for r in results):,} rows".replace(",", " "))
    for r in disagreed:
        print(f"  x {r.table}: {r.source_rows} rows locally, {r.target_rows} landed")
    sys.exit(1 if disagreed else 0)


if __name__ == "__main__":
    main()
