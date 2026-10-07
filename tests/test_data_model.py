"""The data model in README_DPM2.md: the cardinality it draws and the queries it publishes.

The document's claim is that nothing in it is guessed. These tests hold it to that: the
cardinality has to come from a measurement, and every published query has to run.
"""

import re

import pytest

import gen_dpm2_doc as gen
from conftest import REPO, needs_dpm2
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


@needs_dpm2
@pytest.mark.skipif(not README.exists(), reason="README_DPM2.md has not been generated")
def test_every_published_query_runs():
    """Ten worked queries, and the counts the prose quotes for nine of them."""
    import duckdb

    expected = {1: 5, 2: 14, 3: 14, 4: 39, 5: 3, 6: 1, 7: 114, 8: 36, 9: 0}
    blocks = re.findall(r"```sql\n(.*?)```", README.read_text(), re.S)
    assert len(blocks) >= 10

    con = duckdb.connect(str(gen.DPM2), read_only=True)
    con.execute(f"ATTACH '{REPO / 'pay42.duckdb'}' AS pack (READ_ONLY)")
    try:
        for n, sql in enumerate(blocks, 1):
            # The ATTACH is shown in the prose for the reader; it is already done here.
            body = "\n".join(line for line in sql.splitlines() if not line.startswith("ATTACH"))
            rows = con.execute(body).fetchall()
            if n in expected:
                assert len(rows) == expected[n], f"query {n} answered {len(rows)}, not {expected[n]}"
    finally:
        con.close()


@needs_dpm2
def test_every_relationship_still_holds_in_this_release():
    """What the generator asserts at build time, asserted again as a test."""
    import duckdb

    con = duckdb.connect(str(gen.DPM2), read_only=True)
    try:
        shapes = gen.verify(con)  # raises SystemExit on an orphan
    finally:
        con.close()
    assert set(shapes) == set(gen.REL)


@needs_dpm2
def test_an_excluded_cell_is_exactly_a_cell_with_no_variable():
    """The claim the document makes, measured rather than repeated."""
    import duckdb

    con = duckdb.connect(str(gen.DPM2), read_only=True)
    try:
        disagreeing = con.execute(
            "SELECT count(*) FROM TableVersionCell WHERE (IsExcluded <> 0) <> (VariableVID IS NULL)"
        ).fetchone()
    finally:
        con.close()
    assert disagreeing == (0,)
