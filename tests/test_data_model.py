"""The data model in README_DPM2.md: the cardinality it draws and the queries it publishes.

The document's claim is that nothing in it is guessed. These tests hold it to that: the
cardinality has to come from a measurement, and every published query has to run.
"""

import re

import pytest

import gen_dpm2_doc as gen
from conftest import DPM2_DB, PAY42_DB, REPO, needs_dpm2, needs_store
from gen_dpm2_doc import Shape, cardinality

README = REPO / "README_DPM2.md"


@pytest.mark.parametrize(
    ("shape", "drawn"),
    [
        (Shape(nullable=False, unique=False), ("||", "o{")),  # every child has one parent, many children
        (Shape(nullable=True, unique=False), ("|o", "o{")),  # the parent is optional
        (Shape(nullable=False, unique=True), ("||", "o|")),  # 1:1 - Item to Property
        (Shape(nullable=True, unique=True), ("|o", "o|")),
    ],
)
def test_cardinality_comes_from_the_measurement(shape, drawn):
    assert cardinality(shape) == drawn


def test_a_unique_child_key_is_never_drawn_as_one_to_many():
    """The review finding: Item ||--o{ Property claimed an item can have many properties."""
    _, child_side = cardinality(Shape(nullable=False, unique=True))
    assert child_side != "o{"


def test_every_relationship_belongs_to_a_diagram():
    assert {rel.group for rel in gen.REL} <= set(gen.GROUPS)


def test_no_relationship_is_listed_twice():
    pairs = [(rel.child, rel.key, rel.parent, rel.parent_key) for rel in gen.REL]
    assert len(pairs) == len(set(pairs))


def test_every_relationship_says_what_it_means():
    assert all(rel.note for rel in gen.REL)


def test_every_drawn_table_is_a_table_of_the_model():
    """ATTRS is hand-curated, so a typo there would silently draw an empty entity."""
    drawn = {rel.child for rel in gen.REL} | {rel.parent for rel in gen.REL}
    assert set(gen.ATTRS) <= drawn, set(gen.ATTRS) - drawn


# --- the generated document ------------------------------------------------------------


@pytest.mark.skipif(not README.exists(), reason="README_DPM2.md has not been generated")
def test_the_document_has_one_diagram_per_group():
    assert len(re.findall(r"```mermaid\n(.*?)```", README.read_text(), re.S)) == len(gen.GROUPS)


@pytest.mark.skipif(not README.exists(), reason="README_DPM2.md has not been generated")
def test_the_document_draws_the_two_one_to_one_relationships():
    text = README.read_text()
    assert 'Item ||--o| Property : "PropertyID"' in text
    assert 'OperandReference ||--o| OperandReferenceLocation : "OperandReferenceID"' in text


# What each published query must answer, keyed by a phrase only that query contains.
# Not by position: inserting a query in the middle used to renumber every expectation
# after it, so a correct edit broke assertions that had nothing to do with it.
EXPECTED_ROWS = {
    "f.Code = 'PAY'": 5,  # module versions of one framework
    "mv.VersionNumber = '1.1.0'\nORDER BY tv.Code": 14,  # templates in the module version
    "count(*) FILTER (WHERE c.IsExcluded <> 0)": 14,  # cells per template
    "h.Direction = 'Y'": 39,  # rows of Y_01.01, pinned to one module version
    "dimension.Name AS dimension": 3,  # what one cell measures
    "lower(p.PeriodType)": 1,  # its data type
    "o.Code, os.Severity, ov.Expression": 114,  # rules in scope
    "o.Code = 'v09123_m'": 36,  # the cells one rule reaches
    "FULL OUTER JOIN pack.datapoints": 0,  # the pack against the model
    "tc.tbl = 'F_12.01.a'\nGROUP BY t.rule_code, tc.row_code\nORDER": 6,  # how F 12.01.a adds up
    "tl.Direction = 'Y'": 6,  # the same, with the axis labels joined back on
    "vv.VariableID = 149866": 5,  # a sample instance's datapoint id, resolved to its cell
}


@needs_dpm2
@needs_store  # query 9 joins pack.datapoints, so this needs both stores, not just the model
@pytest.mark.skipif(not README.exists(), reason="README_DPM2.md has not been generated")
def test_every_published_query_runs():
    """Every worked query in the document, and the counts its prose quotes."""
    import duckdb

    blocks = re.findall(r"```sql\n(.*?)```", README.read_text(), re.S)
    assert len(blocks) >= len(EXPECTED_ROWS)

    con = duckdb.connect(str(DPM2_DB), read_only=True)
    try:
        # Inside the try: an ATTACH of a store that is not there must close the connection
        # it was opened on, not leak it.
        con.execute(f"ATTACH '{PAY42_DB}' AS pack (READ_ONLY)")
        matched = set()
        for sql in blocks:
            # The ATTACH is shown in the prose for the reader; it is already done here.
            body = "\n".join(line for line in sql.splitlines() if not line.startswith("ATTACH"))
            rows = con.execute(body).fetchall()
            for phrase, count in EXPECTED_ROWS.items():
                if phrase in body:
                    assert len(rows) == count, f"the query containing {phrase!r} answered {len(rows)}, not {count}"
                    matched.add(phrase)
    finally:
        con.close()

    # A phrase that matches nothing means the document moved and the expectation is stale,
    # which would otherwise pass silently as "nothing to check".
    assert matched == set(EXPECTED_ROWS), f"no query contains: {sorted(set(EXPECTED_ROWS) - matched)}"


@pytest.mark.skipif(not README.exists(), reason="README_DPM2.md has not been generated")
def test_every_published_t_sql_block_parses():
    """The T-SQL variants cannot be run here - there is no SQL Server to point at - so
    this is the only thing standing between them and a reader pasting broken SQL into a
    server. sqlfluff.parse raises on an unparsable section, which is the whole check.
    """
    import sqlfluff

    blocks = re.findall(r"```tsql\n(.*?)```", README.read_text(), re.S)
    assert len(blocks) >= 7, "the T-SQL section is missing or shrank"
    for n, sql in enumerate(blocks, 1):
        sqlfluff.parse(sql, dialect="tsql")  # raises APIParsingError if it does not parse
        # The one mistake already made here: writing `&#43;` out of habit, to dodge a build
        # guard this document is exempt from. It renders literally inside a code block.
        assert "&#" not in sql, f"block {n} contains an HTML entity"


@pytest.mark.skipif(not README.exists(), reason="README_DPM2.md has not been generated")
def test_the_t_sql_blocks_are_not_run_against_duckdb():
    """They are tagged tsql precisely so the DuckDB runner leaves them alone."""
    text = README.read_text()
    duck = re.findall(r"```sql\n(.*?)```", text, re.S)
    assert not any("STRING_AGG" in q or "CREATE OR ALTER VIEW" in q for q in duck)


@needs_dpm2
def test_every_relationship_still_holds_in_this_release():
    """What the generator asserts at build time, asserted again as a test."""
    import duckdb

    con = duckdb.connect(str(DPM2_DB), read_only=True)
    try:
        shapes = gen.verify(con)  # raises SystemExit on an orphan
    finally:
        con.close()
    assert set(shapes) == set(gen.REL)


@needs_dpm2
def test_an_excluded_cell_is_exactly_a_cell_with_no_variable():
    """The claim the document makes, measured rather than repeated."""
    import duckdb

    con = duckdb.connect(str(DPM2_DB), read_only=True)
    try:
        disagreeing = con.execute(
            "SELECT count(*) FROM TableVersionCell WHERE (IsExcluded <> 0) <> (VariableVID IS NULL)"
        ).fetchone()
    finally:
        con.close()
    assert disagreeing == (0,)
