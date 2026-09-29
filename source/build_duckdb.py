"""Build pay42.duckdb from the generated CSVs.

Derived, so it is gitignored: run this after gen_pack.py. DuckDB reads the CSVs directly,
so this is mostly about giving the lookup tool an indexed store and a place for the
precomputed column-to-glossary-term mapping.
"""

from pathlib import Path

import duckdb

REPO = Path(__file__).resolve().parent.parent
DB = REPO / "pay42.duckdb"

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
con.execute(f"ATTACH '{DB}' AS pay42 (BLOCK_SIZE {BLOCK_SIZE})")
con.execute("USE pay42")

con.execute(f"CREATE TABLE datapoints AS SELECT * FROM read_csv('{REPO / '05-datapoints.csv'}', header=true)")
con.execute(f"CREATE TABLE terms AS SELECT * FROM read_csv('{REPO / '06-openmetadata-glossary.csv'}', header=true)")

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

counts = {
    name: con.execute(f"SELECT count(*) FROM {name}").fetchone()[0]  # noqa: S608 - fixed names above
    for name in ("datapoints", "terms", "column_terms")
}
con.execute("CHECKPOINT")  # compress and compact before the handle closes
con.close()
size = DB.stat().st_size / 1024
print(f"{DB.name}: " + ", ".join(f"{n} {c}" for n, c in counts.items()) + f"  ({size:.0f} KiB)")
