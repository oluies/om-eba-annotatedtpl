"""Short axis names, and the guard that keeps them attached to the framework.

An alias is keyed on the DPM's own wording. Get that key wrong by a word and nothing
fails: the lookup misses, the long name is returned, and the rename quietly stops
happening. So the table is checked against the axes the framework actually has, the same
way the cited datapoint ids are.
"""

import csv

import pytest

from aliases import AXIS, FRAMEWORK_AXIS, METRIC_AXIS, VALUE, axis, labelled, taxonomy, value, value_type
from conftest import REPO

DATAPOINTS = REPO / "05-datapoints.csv"


def rows():
    with DATAPOINTS.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def axes_of_the_framework() -> set[str]:
    """Every dimension name the pack's own datapoints use, plus the geographical axis.

    Geography is a column of the CSV rather than a dimension pair, so it never appears in
    `row_dimensions`; its axis name is the one the glossary gives it.
    """
    found = {
        part.partition("=")[0].strip()
        for row in rows()
        for cell in (row["row_dimensions"], row["column_dimensions"])
        for part in cell.split(";")
        if "=" in part
    }
    return found | {"Payment transactions geographical breakdown"}


def test_every_aliased_axis_is_an_axis_of_the_framework():
    """The guard. A key that matches nothing renames nothing, and says so nowhere."""
    unknown = sorted(set(AXIS) - axes_of_the_framework())
    assert not unknown, f"{unknown} are not axes of this framework, so these aliases never apply"


def test_every_aliased_value_is_a_member_of_its_own_axis():
    """Same for the value aliases, which are scoped to one axis each."""
    pairs = {
        (part.partition("=")[0].strip(), part.partition("=")[2].strip())
        for row in rows()
        for cell in (row["row_dimensions"], row["column_dimensions"])
        for part in cell.split(";")
        if "=" in part
    }
    unknown = sorted(set(VALUE) - pairs)
    assert not unknown, f"{unknown} are not assignments this framework makes"


def test_an_alias_that_says_the_same_thing_is_not_an_alias():
    """One more name to keep in step, for no reading gained."""
    assert not [k for k, v in AXIS.items() if k == v]
    assert not [k for k, v in VALUE.items() if k[1] == v]


@pytest.mark.parametrize(
    ("dimension", "short"),
    [
        ("Type of authentication", "Authentication"),
        ("Type of payment channel", "Remote/non-remote"),
        ("Payment transactions geographical breakdown", "Geographical breakdown"),
    ],
)
def test_an_aliased_axis_reads_short(dimension, short):
    assert axis(dimension) == short


def test_an_axis_the_target_kept_is_returned_as_the_dpm_spells_it():
    """The target wrote this one out in full, so there is deliberately no entry."""
    long = "Reasons for authentication via non-strong customer authentication"
    assert long not in AXIS
    assert axis(long) == long


def test_a_value_alias_is_scoped_to_its_axis():
    assert value("Type of payment transaction", "Fraudulent payment transaction") == "Fraud"
    # The same words on another axis are not renamed, because member labels repeat.
    assert value("Form of payment", "Fraudulent payment transaction") == "Fraudulent payment transaction"


def test_the_framework_wording_is_kept_beside_the_short_one():
    """What makes this a table of aliases rather than a rewrite."""
    one = labelled("Type of payment transaction=Fraudulent payment transaction")[0]
    assert (one.axis, one.value) == ("Transaction type", "Fraud")
    assert (one.axis_source, one.value_source) == ("Type of payment transaction", "Fraudulent payment transaction")
    assert one.renamed is True


def test_an_unaliased_assignment_is_not_marked_renamed():
    one = labelled("Form of payment=Credit transfers")[0]
    assert (one.axis, one.value) == ("Form of payment", "Credit transfers")
    assert one.renamed is False


def test_the_target_column_reads_the_way_the_target_asked():
    """End to end on the column the target wording was written for, from the CSV itself."""
    row = next(r for r in rows() if r["column_name"] == "Y0101_r0190_c0020")
    reading = {one.axis: one.value for one in labelled(row["row_dimensions"] + "; " + row["column_dimensions"])}
    assert reading == {
        "Form of payment": "Credit transfers",
        "Authentication": "Authenticated via non-strong customer authentication",
        "Electronic / Non-electronic": "Initiated electronically",
        "Reasons for authentication via non-strong customer authentication": "Trusted beneficiary",
        "Remote/non-remote": "Initiated via remote payment channel",
        "Transaction type": "Fraud",
    }


def test_the_two_axes_the_layout_carries_as_its_own_columns():
    metric = value_type("Amount of payment")
    assert (metric.axis, metric.value) == (METRIC_AXIS, "Amount of payment")
    tax = taxonomy("EBA PAY", "4.2")
    assert (tax.axis, tax.value) == (FRAMEWORK_AXIS, "EBA PAY 4.2")
