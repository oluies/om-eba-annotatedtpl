"""Resolving a warehouse column name, and the two DPM lookups.

The column-name split is the one piece of parsing everything else depends on: landing one
row off yields a correct-looking description of the wrong datapoint, and nothing detects
it. So the shapes it must and must not match are pinned here.
"""

import json

import pytest

import agent_tools
import dpm_lookup
import pay42_lookup
from conftest import needs_dpm2, needs_store

# --- the column name -------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "template", "row", "col"),
    [
        ("Y0101_r0010_c0010", "Y0101", "0010", "0010"),
        ("B0101_r999_c0020", "B0101", "999", "0020"),  # a DORA row is a record ordinal
        ("B9901_r0040_c0030", "B9901", "0040", "0030"),  # except B_99.01, which is fixed
    ],
)
def test_a_datapoint_column_splits_into_its_coordinates(name, template, row, col):
    parts = pay42_lookup.split_column_name(name)
    assert parts is not None
    assert (parts["prefix"] + parts["major"] + parts["minor"], parts["row"], parts["col"]) == (template, row, col)


@pytest.mark.parametrize(
    "name",
    ["Period_SK", "Company_BK", "Taxonomy_Name", "Y0101_r0010", "Y0101_c0010", "Y0101_r0010_c001", "", "Open_Axis_1"],
)
def test_warehouse_context_columns_do_not_split(name):
    """They carry no framework meaning, so resolving one at all would be the bug."""
    assert pay42_lookup.split_column_name(name) is None


# --- the rules the lookup hands an agent -----------------------------------------------


def rule_row(code, sheets, severity="warning"):
    return {"rule_code": code, "severity": severity, "expression": "{r0020} <= {r0010}", "sheets": sheets}


SIX = ["0010", "0020", "0030", "0040", "0050", "0060"]


def test_fold_rules_keeps_the_expression_verbatim():
    """It goes to a model as JSON, not through the sanitiser, so the operators survive."""
    (folded,) = pay42_lookup.fold_rules([rule_row("v1", [""])])
    assert folded["expression"] == "{r0020} <= {r0010}"


def test_fold_rules_drops_a_rule_for_another_variant():
    assert pay42_lookup.fold_rules([rule_row("v1", ["0030"])], variant="0010") == []


def test_fold_rules_keeps_a_rule_with_no_sheet_whatever_the_variant():
    assert len(pay42_lookup.fold_rules([rule_row("v1", [""])], variant="0010")) == 1


def test_fold_rules_says_which_variants_when_it_is_only_some():
    (folded,) = pay42_lookup.fold_rules([rule_row("v1", ["0030"])], variants=SIX)
    assert folded["variants"] == ["0030"]


def test_fold_rules_stays_quiet_when_a_rule_covers_them_all():
    (folded,) = pay42_lookup.fold_rules([rule_row("v1", SIX)], variants=SIX)
    assert "variants" not in folded


# --- the DPM lookups -------------------------------------------------------------------


@needs_dpm2
@pytest.mark.parametrize("name", ["Period_SK", "Y_01", "Y_01_01_01", "", "Taxonomy_Name"])
def test_a_name_that_is_not_a_template_is_refused_at_the_lookup(name):
    """Where the refusal moved to. The old parser decided this itself and got F_12.01.a
    wrong; the key now reduces anything and the database says whether it is a template."""
    answer = dpm_lookup.lookup_dpm_table(name)
    assert not answer["found"]
    assert "No template matching" in answer["message"] or "not a template code" in answer["message"]


def test_cell_code_is_written_as_the_model_writes_it():
    assert dpm_lookup.cell_code("Y_01.01", "0010", "0010", "0010") == "{Y_01.01, r0010, c0010, s0010}"
    assert dpm_lookup.cell_code("B_01.01", "*", "0020") == "{B_01.01, r*, c0020}"


def test_dpm_fold_rules_keeps_one_entry_per_module_version():
    """v09247_s is a warning in 1.1.0 and an error in 1.2.0; that is not a duplicate."""
    rows = [
        {"rule_code": "v09247_s", "severity": "warning", "expression": "a", "module": "PSD_FRP 1.1.0"},
        {"rule_code": "v09247_s", "severity": "error", "expression": "a", "module": "PSD_FRP 1.2.0"},
        {"rule_code": "v1", "severity": "warning", "expression": "b", "module": "PSD_FRP 1.1.0"},
        {"rule_code": "v1", "severity": "warning", "expression": "b", "module": "PSD_FRP 1.2.0"},
    ]
    folded = dpm_lookup.fold_rules(rows)
    by_code = {(r["rule_code"], r["severity"]): r["modules"] for r in folded}
    assert by_code[("v09247_s", "warning")] == ["PSD_FRP 1.1.0"]
    assert by_code[("v09247_s", "error")] == ["PSD_FRP 1.2.0"]
    # Same severity and expression in both: one entry, both versions on it.
    assert by_code[("v1", "warning")] == ["PSD_FRP 1.1.0", "PSD_FRP 1.2.0"]


def test_the_dpm_lookups_say_so_when_the_database_is_absent(monkeypatch, tmp_path):
    monkeypatch.setattr(dpm_lookup, "DB", tmp_path / "nothing.duckdb")
    answer = dpm_lookup.lookup_dpm_table("Y_01_01")
    assert answer["found"] is False
    assert "fetch_dpm2.py" in answer["message"]
    assert dpm_lookup.lookup_dpm_cell("Y_01_01", "0010", "0010", "0010")["found"] is False


# --- dispatch --------------------------------------------------------------------------


def test_dispatch_names_what_it_has_for_an_unknown_tool():
    answer = agent_tools.dispatch("no_such_tool", "{}")
    assert "no such tool" in answer["error"]
    assert "lookup_datapoint" in answer["available"]


@pytest.mark.parametrize("arguments", ["{not json", "", "1" * 4400])
def test_dispatch_survives_arguments_that_are_not_usable_json(arguments):
    """A 4300-digit integer trips CPython's conversion limit with a plain ValueError,
    which a handler written for JSONDecodeError alone would have let escape."""
    assert "not usable JSON" in agent_tools.dispatch("lookup_datapoint", arguments)["error"]


def test_dispatch_takes_a_dict_as_readily_as_a_string(monkeypatch):
    monkeypatch.setattr(dpm_lookup, "DB", dpm_lookup.DB.with_name("absent.duckdb"))
    for arguments in ({"table": "Y_01_01"}, json.dumps({"table": "Y_01_01"})):
        assert agent_tools.dispatch("lookup_dpm_table", arguments)["found"] is False


def registered_names() -> set[str]:
    """The names TOOLS actually offers the model.

    The definitions are plain literal dicts, so ty infers one wide union for their
    values: `"type": "function"` sits beside the `function` object, and inside that,
    `name` sits beside `strict` and the parameter schema. Hence the isinstance to reach
    the function object and the str() to read its name - a second subscript, or an
    unguarded one, is what ty rejects.
    """
    functions = [tool["function"] for tool in agent_tools.TOOLS]
    return {str(f["name"]) for f in functions if isinstance(f, dict)}


def test_every_registered_tool_is_dispatchable():
    """A definition registered but not dispatched is a turn the model cannot recover from."""
    names = registered_names()
    assert len(names) == len(agent_tools.TOOLS), "every definition must carry a distinct name"
    assert names <= {name.value for name in agent_tools.ToolName}


# --- against the real stores ------------------------------------------------------------


@needs_store
def test_a_real_column_resolves_with_its_rules():
    answer = pay42_lookup.lookup_datapoint("Y0101_r0010_c0010", "0010")
    assert answer["found"] is True
    assert answer["common"]["table_name"] == "Y_01_01"
    assert answer["validation_rules"], "the store has rules; the lookup should return them"


@needs_store
def test_a_context_column_is_refused_rather_than_guessed():
    answer = pay42_lookup.lookup_datapoint("Period_SK")
    assert answer["found"] is False
    assert "warehouse context" in answer["message"]


@needs_dpm2
def test_a_corep_template_resolves_even_though_the_pack_does_not_cover_it():
    answer = dpm_lookup.lookup_dpm_table("C_01.00")
    assert answer["found"] is True
    assert answer["rows"], "C_01.00 has rows in the model"
    assert any(m["framework"].startswith("COREP") or m["module"].startswith("COREP") for m in answer["modules"])


@needs_dpm2
def test_a_cell_with_a_sheet_axis_needs_its_sheet():
    missing = dpm_lookup.lookup_dpm_cell("Y_01_01", "0010", "0010")
    assert missing["found"] is False
    assert "sheet axis" in missing["message"]
    assert dpm_lookup.lookup_dpm_cell("Y_01_01", "0010", "0010", "0010")["found"] is True


# --- the three tools for querying a template's structure --------------------------------


@pytest.mark.parametrize(
    ("spelling", "resolved"),
    [
        ("F_12.01.a", "F1201A"),
        ("F1201A", "F1201A"),
        ("F 12.01.a", "F1201A"),
        ("f_12_01_a", "F1201A"),
        ("F_04.04.1", "F04041"),
        ("F04041", "F04041"),
        ("Y_01_01", "Y0101"),
        ("C_01.00", "C0100"),
    ],
)
def test_every_spelling_of_a_code_reduces_to_one_key(spelling, resolved):
    """The regex this replaced could not read F_12.01.a at all: it wanted exactly two pairs
    of digits and nothing after them, so a FINREP variant suffix was 'not a template code'."""
    assert dpm_lookup.code_key(spelling) == resolved


def test_a_context_column_reduces_to_something_no_template_matches():
    assert dpm_lookup.code_key("Period_SK") == "PERIODSK"


def test_the_warehouse_column_name_is_the_shape_a_warehouse_uses():
    assert dpm_lookup.warehouse_name("F_04.04.1", "0040", "0015") == "F04041_r0040_c0015"
    assert dpm_lookup.warehouse_name("Y_01.01", "0010", "0010") == "Y0101_r0010_c0010"


@needs_dpm2
def test_a_template_breaks_down_by_the_dimensions_a_hand_written_hierarchy_encodes():
    """F_04.04.1 is the template the gist maintains a structure.yaml for. The counterparty
    breakdown it maps by hand is a dimension of the model."""
    answer = dpm_lookup.lookup_dpm_dimensions("F04041")
    assert answer["found"] and answer["table"] == "F_04.04.1"
    by_name = {d["dimension"]: {m["member"] for m in d["members"]} for d in answer["dimensions"]}
    assert "Counterparty sector" in by_name
    assert {"Credit institutions", "Households", "General governments"} <= by_name["Counterparty sector"]
    assert "Type of financial instruments" in by_name


@needs_dpm2
def test_a_member_resolves_to_the_cells_that_make_up_the_aggregate():
    answer = dpm_lookup.lookup_dpm_cells("F04041", "Counterparty sector", "Credit institutions")
    assert answer["found"]
    assert len(answer["cells"]) == len(answer["datapoints"]) == 24
    assert "F04041_r0040_c0015" in {c["warehouse_column"] for c in answer["cells"]}
    # The same member in two blocks of the template, with the same row label in each.
    assert sorted({c["row_code"] for c in answer["cells"]}) == ["0040", "0100"]


@needs_dpm2
def test_a_member_is_matched_without_regard_to_case_or_trailing_space():
    """The model's item names carry trailing spaces inconsistently - the member on these
    cells is "Credit institutions " - so an exact match found nothing for a name copied
    straight out of lookup_dpm_dimensions."""
    loose = dpm_lookup.lookup_dpm_cells("f04041", "counterparty sector", "  credit institutions  ")
    assert loose["found"]
    assert len(loose["cells"]) == 24


@needs_dpm2
def test_a_member_that_does_not_exist_says_so_and_says_where_to_look():
    answer = dpm_lookup.lookup_dpm_cells("F04041", "Counterparty sector", "Martians")
    assert not answer["found"]
    assert "lookup_dpm_dimensions" in answer["message"]


@needs_dpm2
def test_the_sums_of_f_12_01_a_including_the_column_that_differs():
    answer = dpm_lookup.lookup_dpm_sums("F1201A", "FINREP9", "3.3.0")
    assert answer["roots"] == ["0520"], "0520 is the total nothing else breaks down into"
    by_rule = {s["rule_code"]: s for s in answer["sums"]}
    # The same total, two rules: one column of twelve leaves the POCI row out.
    assert by_rule["v5051_m"]["addend_rows"] == ["0010", "0180", "0360", "0600"]
    assert by_rule["v09604_m"]["addend_rows"] == ["0010", "0180", "0360"]
    assert by_rule["v09604_m"]["columns"] == ["0020"]
    assert len(by_rule["v5051_m"]["columns"]) == 11


@needs_dpm2
def test_the_sums_are_scoped_to_a_module_version():
    """A rule code is reissued per module version, so an unscoped answer would mix them."""
    assert len(dpm_lookup.lookup_dpm_sums("Y_01_01", "PSD_FRP", "1.1.0")["sums"]) == 18


@needs_dpm2
def test_a_module_whose_rules_are_not_arithmetic_answers_nothing_rather_than_guessing():
    answer = dpm_lookup.lookup_dpm_sums("B_99_01", "DORA", "1.1.0")
    assert answer["sums"] == []
    assert "not arithmetic" in answer["message"] or "No sum rule" in answer["message"]


NEW_DPM_TOOLS = {"lookup_dpm_dimensions", "lookup_dpm_cells", "lookup_dpm_sums"}


def test_the_three_new_tools_are_dispatchable_whether_or_not_they_are_registered():
    """TOOLS carries the DPM tools only when the database is there, so asserting they are
    in it needs the guard below. dispatch knows them either way, which is the property that
    matters: a host that registered them before the file moved gets an explanation."""
    assert {name.value for name in agent_tools.ToolName} >= NEW_DPM_TOOLS
    for name in sorted(NEW_DPM_TOOLS):
        answer = agent_tools.dispatch(
            name,
            {
                "table": "F1201A",
                "module": "FINREP9",
                "version": "3.3.0",
                "dimension": "Counterparty sector",
                "member": "Credit institutions",
            },
        )
        assert "no such tool" not in str(answer)


@needs_dpm2
def test_the_three_new_tools_are_registered_when_the_database_is_there():
    names = registered_names()
    assert names >= NEW_DPM_TOOLS
    assert names <= {name.value for name in agent_tools.ToolName}
