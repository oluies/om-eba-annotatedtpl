"""What the pack extracted against what the model says, where the two look like they differ.

The pack's dimension members come from the annotated table layout; the DPM 2.0 database is
the EBA's own model of the same cells. Two derivations of one thing, so they can be held
against each other - and the place to do it is where the layout reads as if the pack got
it wrong.

Y_04.01 is that place. Row 0040 narrows to `Of which initiated via remote payment channel`
and twenty-two rows sit under it, but only fourteen of them carry a `Type of payment
channel` member. The eight that do not are exactly the ones beneath the abstract heading
0190, `Of which fraudulent card payments by fraud types:`.

That reads like an extraction losing an inherited member, and it is not: the model omits it
too, on the same eight rows. Which is the point of these tests. A reader who walks the row
hierarchy and concludes the extractor has a bug would "fix" it by inheriting the channel,
and would then be wrong about eight rows of every variant of this template. The row
hierarchy is a layout, not a dimension derivation.
"""

import csv

import pytest

import dpm_lookup
from conftest import REPO, needs_dpm2

TEMPLATE = "Y_04.01"
CHANNEL = "Type of payment channel"
GEOGRAPHY = "Payment transactions geographical breakdown"

# The rows under 0040, split by whether the model gives them a channel member. Written out
# rather than derived, because a test that computes its own expectation from the data it is
# checking asserts nothing.
WITH_CHANNEL = (
    "0100",
    "0110",
    "0120",
    "0130",
    "0140",
    "0150",
    "0160",
    "0170",
    "0180",
    "0290",
    "0300",
    "0310",
    "0320",
    "0330",
)
WITHOUT_CHANNEL = ("0200", "0210", "0220", "0230", "0240", "0250", "0260", "0270")


def datapoints() -> dict[tuple[str, str, str], dict[str, str]]:
    with (REPO / "05-datapoints.csv").open(encoding="utf-8", newline="") as handle:
        return {
            (row["row_code"], row["column_code"], row["variant"]): row
            for row in csv.DictReader(handle)
            if row["template"] == TEMPLATE
        }


def pack_members(row: dict[str, str]) -> set[str]:
    """Every member the pack gives one datapoint, in the model's own shape.

    Geography is folded back in: the pack keeps it in a column of its own because it varies
    by variant, while the model carries it as one dimension among the rest.
    """
    members = {
        part.strip()
        for cell in (row["row_dimensions"], row["column_dimensions"])
        for part in cell.split(";")
        if part.strip()
    }
    return members | {f"{GEOGRAPHY}={row['geography']}"}


def model_members(row_code: str) -> set[str]:
    answer = dpm_lookup.lookup_dpm_cell(TEMPLATE, row_code, "0020", sheet="0010")
    assert answer["found"] is True, f"no cell for r{row_code}: {answer.get('message')}"
    return {f"{m['dimension']}={m['member']}" for m in answer["dimensions"]}


@needs_dpm2
@pytest.mark.parametrize("row_code", WITH_CHANNEL + WITHOUT_CHANNEL)
def test_the_packs_members_are_the_models_members(row_code):
    """Two derivations of one cell, held against each other. All 22 agree exactly."""
    row = datapoints()[(row_code, "0020", "0010")]
    assert pack_members(row) == model_members(row_code)


@needs_dpm2
@pytest.mark.parametrize("row_code", WITHOUT_CHANNEL)
def test_a_row_under_a_narrowing_heading_need_not_carry_that_narrowing(row_code):
    """The eight rows beneath the abstract heading, in the model itself.

    Not an extraction gap to be repaired: inheriting the channel here would contradict the
    EBA's own model of these cells.
    """
    assert not any(member.startswith(CHANNEL) for member in model_members(row_code))


@needs_dpm2
@pytest.mark.parametrize("row_code", WITH_CHANNEL)
def test_their_cousins_under_the_same_heading_do_carry_it(row_code):
    """The control. Without it the test above would pass on a template that never uses the
    axis at all, which would say nothing about inheritance."""
    assert any(member.startswith(CHANNEL) for member in model_members(row_code))
