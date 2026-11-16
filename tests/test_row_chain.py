"""Where a row sits, and the line that says so.

The chain is the one thing in the pack that reads like a dimension derivation and is not,
so the tests say both: that it reproduces the path the layout draws, and that nothing here
claims it accounts for a row's members.
"""

import pytest

import dpm_lookup
import row_chain
from conftest import needs_dpm2
from row_chain import ChainError, ancestry, breadcrumb

# Headers as HEADERS_SQL returns them, trimmed to what the chain reads.
TREE = [
    {"direction": "Y", "code": "0010", "label": "Credit transfers", "parent_code": None, "is_abstract": False},
    {
        "direction": "Y",
        "code": "0040",
        "label": "Of which Initiated electronically",
        "parent_code": "0010",
        "is_abstract": False,
    },
    {
        "direction": "Y",
        "code": "0160",
        "label": "Of which broken down by reason",
        "parent_code": "0040",
        "is_abstract": True,
    },
    {
        "direction": "Y",
        "code": "0190",
        "label": "Trusted beneficiary (Art.13 RTS)",
        "parent_code": "0160",
        "is_abstract": False,
    },
    # A column with a code that collides with a row's, which is why direction is filtered.
    {"direction": "X", "code": "0010", "label": "Payment transactions", "parent_code": None, "is_abstract": False},
]

TARGET = (
    "Credit transfers, Fraudulent payment transactions, Of which Initiated electronically, "
    "Of which initiated via remote payment channel, "
    "Of which authenticated via non-strong customer authentication, "
    "Of which broken down by reason for authentication via non-strong customer authentication, "
    "Trusted beneficiary (Art.13 RTS)"
)


def test_the_chain_runs_root_first_and_the_row_last():
    assert [s.code for s in ancestry(TREE, "0190")] == ["0010", "0040", "0160", "0190"]


def test_a_row_code_is_not_a_column_code():
    """Both axes use 0010 in this template. Reading the wrong one would root the chain in a
    column, which is a different axis entirely."""
    assert [s.label for s in ancestry(TREE, "0010")] == ["Credit transfers"]
    assert [s.label for s in ancestry(TREE, "0010", direction="X")] == ["Payment transactions"]


def test_an_abstract_level_is_carried_and_marked():
    """It belongs in the label - the target wording includes it - and a consumer that wants
    only reportable levels needs to be able to tell."""
    steps = ancestry(TREE, "0190")
    assert [s.abstract for s in steps] == [False, False, True, False]


def test_a_missing_parent_raises_rather_than_shortening_the_chain():
    orphan = [{"direction": "Y", "code": "0200", "label": "x", "parent_code": "9999", "is_abstract": False}]
    with pytest.raises(ChainError, match="no header 9999"):
        ancestry(orphan, "0200")


def test_a_cycle_raises():
    loop = [
        {"direction": "Y", "code": "a", "label": "a", "parent_code": "b", "is_abstract": False},
        {"direction": "Y", "code": "b", "label": "b", "parent_code": "a", "is_abstract": False},
    ]
    with pytest.raises(ChainError, match="cycle"):
        ancestry(loop, "a")


def test_the_column_is_read_after_the_root():
    line = breadcrumb(ancestry(TREE, "0190"), "Fraudulent payment transactions")
    assert line.startswith("Credit transfers, Fraudulent payment transactions, Of which Initiated")


def test_without_a_column_the_line_is_the_rows_alone():
    assert breadcrumb(ancestry(TREE, "0190")) == (
        "Credit transfers, Of which Initiated electronically, "
        "Of which broken down by reason, Trusted beneficiary (Art.13 RTS)"
    )


def test_an_empty_chain_is_an_empty_line():
    assert breadcrumb(()) == ""


def test_labels_are_kept_as_the_layout_spells_them():
    """`Of which Initiated electronically` has that capital I in the source. Correcting it
    would break a search against the framework's own wording."""
    assert "Of which Initiated electronically" in breadcrumb(ancestry(TREE, "0190"))


def test_the_module_says_it_is_not_a_derivation():
    """The one thing a reader has to take from the docstring, so it is held in place."""
    assert row_chain.__doc__ and "not a derivation" in row_chain.__doc__


@needs_dpm2
def test_the_target_wording_for_y0101_r0190_c0020():
    """End to end against the model: the line the target asked for, verbatim.

    The target as typed lowercased `credit transfers` and `of which broken down`; the
    labels here are the layout's own casing, which is what a search has to match.
    """
    answer = dpm_lookup.lookup_dpm_cell("Y_01.01", "0190", "0020", sheet="0020")
    assert answer["found"] is True
    assert answer["breadcrumb"] == TARGET
    assert [s["code"] for s in answer["row_chain"]] == ["0010", "0040", "0050", "0110", "0160", "0190"]
    assert [s["abstract"] for s in answer["row_chain"]] == [False, False, False, False, True, False]
