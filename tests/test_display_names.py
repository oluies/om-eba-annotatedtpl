"""The rule for what a table and its columns are called.

The whole point of display_names() is that two columns of one table can never end up with
the same label, because the EBA layout nests its rows and repeats a label at every level.
"""

import pytest

from display_names import base_name, display_names, members, table_name


def row(
    column_name, row_label, column_label, dims="", template="Y_01.01", template_name="Credit transfers", row_code="0010"
):
    return {
        "column_name": column_name,
        "row_label": row_label,
        "column_label": column_label,
        "row_dimensions": dims,
        "template": template,
        "template_name": template_name,
        "row_code": row_code,
    }


def test_members_parses_the_dimension_string():
    assert members("Form of payment=Credit transfers; Event Type=Phishing") == {
        "Form of payment": "Credit transfers",
        "Event Type": "Phishing",
    }


@pytest.mark.parametrize("text", ["", "   ", ";;", "no equals sign"])
def test_members_ignores_anything_that_is_not_a_pair(text):
    assert members(text) == {}


def test_base_name_is_row_then_column_with_no_codes():
    assert base_name(row("c", "Credit transfers", "Payment transactions")) == "Credit transfers - Payment transactions"


def test_table_name_spells_the_template_as_the_dpm_does():
    assert table_name(row("c", "r", "c")) == "Y 01.01 Credit transfers"


def test_distinct_labels_are_left_alone():
    rows = [row("A", "Credit transfers", "Payment transactions"), row("B", "Direct debits", "Payment transactions")]
    assert display_names(rows) == {
        "A": "Credit transfers - Payment transactions",
        "B": "Direct debits - Payment transactions",
    }


def test_a_collision_is_broken_by_the_dimension_that_differs():
    """Two nested rows share a label; only the member that differs is added."""
    rows = [
        row(
            "A", "Of which fraudulent", "Payment transactions", "Form of payment=Credit transfers; Event Type=Phishing"
        ),
        row(
            "B",
            "Of which fraudulent",
            "Payment transactions",
            "Form of payment=Credit transfers; Event Type=Stolen card",
        ),
    ]
    names = display_names(rows)
    assert len(set(names.values())) == 2, names
    assert "Phishing" in names["A"] and "Stolen card" in names["B"]
    # The member they share must not be repeated - it tells the two apart from nothing.
    assert "Credit transfers" not in names["A"]


def test_a_collision_with_nothing_to_tell_it_apart_falls_back_to_the_row_code():
    rows = [
        row("A", "Of which", "Payment transactions", row_code="0020"),
        row("B", "Of which", "Payment transactions", row_code="0030"),
    ]
    names = display_names(rows)
    assert len(set(names.values())) == 2, names
    assert "0020" in names["A"] and "0030" in names["B"]


def test_the_same_column_twice_is_one_column():
    """Callers pass every datapoint row, and a multi-variant column appears six times."""
    rows = [row("A", "Credit transfers", "Payment transactions")] * 6
    assert display_names(rows) == {"A": "Credit transfers - Payment transactions"}
