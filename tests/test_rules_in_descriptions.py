"""The validation rules as they reach a catalogue description.

Two things have to hold. A rule that constrains a variant this table does not hold must
not be named - that was a real bug: it was listed with an empty variant list. And nothing
generated may contain a character OpenMetadata's viewer mangles, which is why the
expressions are not inlined at all.
"""

import pytest

import describe_table as d
from describe_table import Rule, rule_count_sentence, rules_of_table, rules_sentence


def rule(code, sheet="", severity="warning", table="Y_01_01", row="0010", column="0010"):
    return Rule(
        module="PSD_FRP 1.1.0",
        rule_code=code,
        severity=severity,
        table_name=table,
        row_code=row,
        column_code=column,
        sheet_code=sheet,
        expression="with {tY_01.01, c*, s*}: {r0020} <= {r0010}",
    )


SIX = ("0010", "0020", "0030", "0040", "0050", "0060")


def test_no_rules_says_nothing():
    assert rules_sentence([]) == ""


def test_a_rule_on_every_variant_is_named_without_qualification():
    said = rules_sentence([rule("v1", s) for s in SIX], SIX)
    assert said.strip() == "Validation rules (EBA DPM, warning): v1."


def test_a_rule_on_some_variants_says_which():
    rules = [rule("v1", s) for s in SIX] + [rule("v2", "0030")]
    said = rules_sentence(rules, SIX)
    assert "v1, v2." in said
    assert "v2 reaches only variant(s) 0030." in said


def test_a_rule_for_another_variant_is_dropped_not_listed_empty():
    """The bug: with the table holding 0010, a rule scoped to 0030 was still named."""
    said = rules_sentence([rule("v2", "0030")], ("0010",))
    assert said == ""


def test_a_rule_for_this_variant_survives_the_filter():
    said = rules_sentence([rule("v2", "0030"), rule("v3", "0010")], ("0010",))
    assert "v3" in said and "v2" not in said


@pytest.mark.parametrize("sheet", ["", "*"])
def test_no_sheet_axis_or_the_whole_axis_reaches_every_variant(sheet):
    assert "v1." in rules_sentence([rule("v1", sheet)], SIX)


def test_mixed_severities_are_not_claimed_to_be_one():
    said = rules_sentence([rule("v1", "0010", "warning"), rule("v2", "0010", "error")], ("0010",))
    assert "(EBA DPM):" in said
    assert "warning" not in said and "error" not in said


def test_the_expression_is_never_inlined():
    """A plus sign renders as a literal &#43; in the viewer, so none may appear."""
    said = rules_sentence([rule("v1", "0010")], ("0010",))
    assert "{r0020}" not in said
    assert not any(c in said for c in "+<>&")


def test_rule_count_sentence_is_empty_at_zero():
    assert rule_count_sentence(0) == ""
    assert "21 EBA validation rule(s)" in rule_count_sentence(21)


def test_rules_of_table_counts_distinct_codes_for_that_table_only():
    index = {
        ("Y_01_01", "0010", "0010"): [rule("v1"), rule("v1", "0020"), rule("v2")],
        ("Y_01_01", "0020", "0010"): [rule("v2")],
        ("Y_02_01", "0010", "0010"): [rule("v9", table="Y_02_01")],
    }
    assert rules_of_table(index, "Y_01_01") == 2
    assert rules_of_table(index, "Y_02_01") == 1
    assert rules_of_table(index, "Y_99_99") == 0


# --- against the real pack data, when it is in the checkout --------------------------


@pytest.mark.skipif(not d.DATAPOINTS.exists(), reason="05-datapoints.csv is not in this checkout")
def test_every_generated_description_is_viewer_safe():
    """All 2249 of them, because the build guard only covers markdown files.

    Guarded on the file: load_datapoints() opens it without an exists() check, unlike
    load_rules() and load_dora(), so an absent CSV raises rather than returning nothing.
    """
    index, by_column = d.load_rules(), d.load_datapoints()
    texts = [
        d.pay_column_description(dp, axis, False, index, by_column)
        for dps in by_column.values()
        for dp in dps
        for axis in (None, "Open_Axis_1")
    ]
    offenders = [t for t in texts if any(c in t for c in "+<>&")]
    assert offenders == [], offenders[:1]
    assert sum("Validation rules" in t for t in texts) > 0
