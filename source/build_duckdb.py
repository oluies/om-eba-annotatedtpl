"""Build pay42.duckdb from the generated CSVs.

Derived, so it is gitignored: run this after gen_pack.py. DuckDB reads the CSVs directly,
so this is mostly about giving the lookup tool an indexed store and a place for the
precomputed column-to-glossary-term mapping.
"""

import os
from pathlib import Path

import duckdb

REPO = Path(__file__).resolve().parent.parent
# Same environment variables the lookup reads, so a build and a read agree on the path.
DB = Path(os.environ.get("PAY42_DB") or REPO / "pay42.duckdb")
TEMP_DIR = os.environ.get("PAY42_TEMP_DIR")

# Which glossary domain a dimension's members live under. Mirrors DOMAIN_NAMES in
# gen_pack.py; every dimension not listed draws on the payment-characteristics domain.
DOMAIN_OF_DIMENSION = {
    "Event Type": "Fraud event types",
    "Payment related parties": "Payment related parties",
    "Relationships": "Payment related parties",
    "Type of user": "Payment related parties",
    "Payment transactions geographical breakdown": "Geographical breakdown",
}

# Compression is automatic and per column - DuckDB picks Dictionary for these strings on
# its own, and there is no "maximum" to turn up. What does matter at this size is the
# block size: at the 256 KiB default a 1830-row database rounds up to 1.8 MiB, larger
# than the CSV it came from. 16 KiB blocks bring it to about 270 KiB.
#
# A database written with a non-default block size needs a DuckDB new enough to read it,
# which any version that can write one is.
BLOCK_SIZE = 16384

DB.unlink(missing_ok=True)
con = duckdb.connect()
if TEMP_DIR:
    # SET is fine here: this is a one-shot process. The lookup uses connect-time config
    # instead, because SET is global to the instance and would leak across connections.
    Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)
    con.execute(f"SET temp_directory = '{TEMP_DIR}'")
con.execute(f"ATTACH '{DB}' AS pay42 (BLOCK_SIZE {BLOCK_SIZE})")
con.execute("USE pay42")

con.execute(f"CREATE TABLE datapoints AS SELECT * FROM read_csv('{REPO / '05-datapoints.csv'}', header=true)")
con.execute(f"CREATE TABLE terms AS SELECT * FROM read_csv('{REPO / '06-openmetadata-glossary.csv'}', header=true)")
con.execute(
    f"CREATE TABLE dora AS SELECT * FROM read_csv('{REPO / 'source' / 'dpm-dora-1.1.0-datapoints.csv'}', header=true)"
)

# The validation rules, one row per rule and the cell it reaches. all_varchar because
# every code in here is a code: '0010' is a row, not the number ten. An empty axis code
# survives the CSV round trip as NULL, so it is folded back to '' on the way in - the
# lookups match on it, and NULL would never match anything.
con.execute(
    f"""CREATE TABLE rules AS
        SELECT module, rule_code, severity, table_name,
               coalesce(row_code, '')    AS row_code,
               coalesce(column_code, '') AS column_code,
               coalesce(sheet_code, '')  AS sheet_code,
               expression
        FROM   read_csv('{REPO / "09-validation-rules.csv"}', header=true, all_varchar=true)"""
)

# Column to glossary term, flattened out of the two dimension strings so the lookup tool
# does not have to parse them at call time.
mapping: list[tuple[str, int, str]] = []
for column_name, row_dims, col_dims in con.execute(
    "SELECT DISTINCT column_name, row_dimensions, column_dimensions FROM datapoints"
).fetchall():
    seen: list[str] = []
    for chunk in (row_dims or "", col_dims or ""):
        for part in filter(None, (p.strip() for p in chunk.split(";"))):
            dimension, _, member = part.partition("=")
            if not member:
                continue
            domain = DOMAIN_OF_DIMENSION.get(dimension.strip(), "Payment transaction characteristics")
            fqn = f"PAY_4_2.Domains.{domain}.{member.strip()}"
            if fqn not in seen:
                seen.append(fqn)
    mapping.extend((column_name, i, fqn) for i, fqn in enumerate(seen))

con.execute("CREATE TABLE column_terms (column_name VARCHAR, ordinal INTEGER, term_fqn VARCHAR)")
con.executemany("INSERT INTO column_terms VALUES (?, ?, ?)", mapping)

con.execute("CREATE INDEX idx_dp_column ON datapoints(column_name)")
con.execute("CREATE INDEX idx_dp_id ON datapoints(datapoint_id)")
con.execute("CREATE INDEX idx_ct_column ON column_terms(column_name)")
con.execute("CREATE INDEX idx_dora ON dora(template, column_code)")
con.execute("CREATE INDEX idx_rules ON rules(table_name, row_code, column_code)")


def rows_in(name: str) -> int:
    """How many rows a table has. fetchone() types as optional and a count always answers,
    so this is where that is said once rather than subscripted in a comprehension."""
    row = con.execute(f"SELECT count(*) FROM {name}").fetchone()  # noqa: S608 - fixed names below
    return row[0] if row else 0


counts = {name: rows_in(name) for name in ("datapoints", "terms", "column_terms", "dora", "rules")}
con.execute("CHECKPOINT")  # compress and compact before the handle closes
con.close()
size = DB.stat().st_size / 1024
print(f"{DB.name}: " + ", ".join(f"{n} {c}" for n, c in counts.items()) + f"  ({size:.0f} KiB)")
