"""What a description says, and what it deliberately does not.

Two rules the pack committed to and that are easy to regress: the row and column labels
are the display name, so a description must not open by repeating them; and with the
variant unknown a description must state neither a datapoint id nor a unit, because
picking one of six would be inventing five sixths of an answer.
"""

import pytest

from conftest import needs_store
from describe_table import (
    Datapoint,
    DoraDatapoint,
    column_fqn,
    dora_table_description,
    dora_terms_by_column,
    find_open_axis,
    split_column_name,
)


def datapoint(**over):
    return Datapoint.model_validate(
        {
            "column_name": "Y0101_r0010_c0010",
            "table_name": "Y_01_01",
            "datapoint_id": "3264309",
            "template": "Y_01.01",
            "template_name": "Credit transfers transactions",
            "variant": "0010",
            "variant_label": "0010 Domestic amount of payments",
            "metric": "Amount of payment",
            "geography": "Domestic",
            "row_code": "0010",
            "row_label": "Credit transfers",
            "column_code": "0010",
            "column_label": "Payment transactions",
            "row_dimensions": "Form of payment=Credit transfers",
            "column_dimensions": "Type of payment transaction=Payment transactions",
            "unit": "monetary",
            "sign": "positive",
        }
        | over
    )


def test_a_description_does_not_open_by_repeating_the_display_name():
    text = datapoint().description()
    assert not text.startswith("Credit transfers - Payment transactions")
    assert text.startswith("Amount of payment, domestic.")


def test_the_labels_can_be_put_back_for_a_catalogue_without_display_names():
    """Note the separator: an em dash here, a hyphen in the display name. Deliberate or
    not, it is what ships, and the two fields are never compared to each other."""
    assert datapoint().description(keep_labels=True).startswith("Credit transfers \u2014 Payment transactions.")


def test_a_resolved_description_carries_the_datapoint_id_and_the_unit():
    text = datapoint().description()
    assert "Datapoint 3264309" in text
    assert "Unit: monetary amount, positive." in text


def test_a_count_is_called_a_count():
    assert "Unit: count" in datapoint(unit="#").description()


def test_without_a_variant_neither_the_id_nor_the_unit_is_stated():
    """The table holds all six as rows, so stating either would pick one of them."""
    text = datapoint().description_without_variant("Open_Axis_1")
    assert "3264309" not in text
    assert "Unit:" not in text
    assert "`Open_Axis_1` on each row" in text


def test_the_dimension_members_are_spelled_out():
    text = datapoint().description()
    assert "Form of payment = Credit transfers" in text
    assert "Type of payment transaction = Payment transactions" in text


def test_the_glossary_terms_follow_the_members():
    terms = datapoint().glossary_terms()
    assert "PAY_4_2.Domains.Payment transaction characteristics.Credit transfers" in terms
    assert len(terms) == len(set(terms)), "a repeated member must not become a repeated term"


# --- DORA --------------------------------------------------------------------------------


def dora(**over):
    return DoraDatapoint.model_validate(
        {
            "column_name_pattern": "B0101_r*_c0020",
            "table_name": "B_01_01",
            "template": "B_01.01",
            "template_name": "Entity maintaining the register of information",
            "row_code": "*",
            "row_label": "",
            "column_code": "0020",
            "column_label": "Name of the entity",
            "datapoint_id": "3287126",
            "row_kind": "open",
        }
        | over
    )


def test_an_open_row_is_said_to_be_an_ordinal():
    text = dora().description()
    assert "ordinal, not a framework code" in text
    assert "Datapoint 3287126" in text


def test_a_fixed_row_is_named_because_it_tells_the_columns_apart():
    text = dora(row_kind="fixed", row_code="0040", row_label="Low").description()
    assert "row 0040 (Low)" in text


def test_a_dora_display_name_is_the_column_label_alone_on_an_open_row():
    assert dora().display_name() == "Name of the entity"


def test_a_fixed_row_contributes_to_the_display_name():
    name = dora(row_kind="fixed", row_code="0040", row_label="Low").display_name()
    assert name == "Low - Name of the entity"


def test_the_dora_table_description_says_how_the_rows_work():
    text = dora_table_description({"B0101_r*_c0020": dora()})
    assert "One row per record" in text
    assert "B_01.01" in text


def test_dora_terms_map_a_property_and_a_member_onto_the_column():
    rows = [
        {"template": "B_01.02", "column_code": "0060", "kind": "property", "name": "LEI", "domain": ""},
        {
            "template": "B_01.02",
            "column_code": "0060",
            "kind": "member",
            "name": "Direct parent",
            "domain": "Related parties",
        },
        {"template": "B_01.02", "column_code": "0060", "kind": "member", "name": "Nameless", "domain": ""},
    ]
    assert dora_terms_by_column(rows) == {
        ("B_01.02", "0060"): [
            "DORA_1_1_0.Properties.LEI",
            "DORA_1_1_0.Domains.Related parties.Direct parent",
        ]
    }


# --- addressing --------------------------------------------------------------------------


def test_split_column_name_gives_the_row_and_column():
    assert split_column_name("Y0101_r0010_c0020") == {"prefix": "Y0101", "row": "0010", "col": "0020"}


@pytest.mark.parametrize("name", ["Period_SK", "Open_Axis_1", "Y0101_r0010"])
def test_split_column_name_refuses_a_context_column(name):
    assert split_column_name(name) is None


def test_find_open_axis_spots_the_variant_column():
    columns = [
        {"fullyQualifiedName": "s.d.Y_01_01.Period_SK"},
        {"fullyQualifiedName": "s.d.Y_01_01.Open_Axis_1"},
    ]
    assert find_open_axis(columns) == "Open_Axis_1"


def test_find_open_axis_answers_nothing_when_the_table_holds_one_variant():
    assert find_open_axis([{"fullyQualifiedName": "s.d.Y_01_01.Period_SK"}]) is None


def test_a_column_name_with_a_dot_is_quoted_in_the_fqn():
    """FullyQualifiedName.quoteName quotes a part containing a dot; the table FQN is not."""
    assert column_fqn("a.b.c.Y_01_01", "odd.name") == 'a.b.c.Y_01_01."odd.name"'
    assert column_fqn("a.b.c.Y_01_01", "Y0101_r0010_c0010") == "a.b.c.Y_01_01.Y0101_r0010_c0010"


# --- against the real pack ---------------------------------------------------------------


@needs_store
def test_no_two_columns_of_a_table_share_a_display_name():
    """63 of 214 PAY label pairs collide before the rule is applied; none may after."""
    import duckdb

    from conftest import PAY42_DB
    from display_names import display_names

    con = duckdb.connect(str(PAY42_DB), read_only=True)
    try:
        tables = [r[0] for r in con.execute("SELECT DISTINCT table_name FROM datapoints").fetchall()]
        for table in tables:
            result = con.execute(
                "SELECT DISTINCT column_name, row_code, row_label, column_label, row_dimensions, "
                "template, template_name FROM datapoints WHERE table_name = ?",
                [table],
            )
            names = [d[0] for d in result.description]
            rows = [dict(zip(names, row, strict=True)) for row in result.fetchall()]
            labels = display_names(rows)
            assert len(set(labels.values())) == len(labels), f"{table} has a collision"
    finally:
        con.close()
