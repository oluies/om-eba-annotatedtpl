"""Resolving a warehouse column name, and the two DPM lookups.

The column-name split is the one piece of parsing everything else depends on: landing one
row off yields a correct-looking description of the wrong datapoint, and nothing detects
it. So the shapes it must and must not match are pinned here.
"""

import ast
import datetime
import decimal
import json
import textwrap
from pathlib import Path

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


NEW_DPM_TOOLS = {
    "lookup_dpm_dimensions",
    "lookup_dpm_cells",
    "lookup_dpm_sums",
    "check_report",
    "lookup_dpm_datapoint",
    "lookup_dpm_property",
    "explain_report",
    "lookup_dpm_rule",
}


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


# --- two queries must not share one name -----------------------------------------------


def overwritten_at_module_level(source: str) -> set[str]:
    """Top-level names rebound to a value that does not derive from the old one.

    The second binding silently wins, so two different queries under one name is a bug no
    amount of exercising either caller reveals - both callers get the survivor. That is
    how DIMENSIONS_SQL shipped twice, with lookup_dpm_cell passing a VariableVID to a
    query filtering on TableVID and getting an empty list back.

    Extending a name from itself - `X = (*X, "more")`, with a comment saying why - is not
    that bug: nothing is lost. So a rebinding counts only when the new value never reads
    the name, which is what makes the old value unreachable.
    """
    overwritten: set[str] = set()
    bound: set[str] = set()
    for node in ast.parse(source).body:
        if not isinstance(node, ast.Assign):
            continue
        reads = {n.id for n in ast.walk(node.value) if isinstance(n, ast.Name)}
        for target in (t for t in node.targets if isinstance(t, ast.Name)):
            if target.id in bound and target.id not in reads:
                overwritten.add(target.id)
            bound.add(target.id)
    return overwritten


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("A = 1\nA = 2\n", {"A"}),
        ("A = 1\nA = (*A, 2)\n", set()),  # extended from itself, nothing lost
        ("A = 1\nB = 2\n", set()),
        ("A = B = 1\nB = 2\n", {"B"}),
    ],
)
def test_the_rebinding_detector_separates_losing_a_value_from_extending_one(source, expected):
    assert overwritten_at_module_level(source) == expected


@pytest.mark.parametrize("module", [dpm_lookup, pay42_lookup, agent_tools])
def test_no_module_level_name_is_overwritten(module):
    path = Path(module.__file__)
    assert overwritten_at_module_level(path.read_text()) == set(), f"{path.name} loses a value"


@needs_dpm2
def test_a_cell_carries_its_own_dimension_members():
    """The members of one cell, not of its template: seven for this one, and the query is
    keyed on the cell's VariableVID. An empty list here is the collision above."""
    answer = dpm_lookup.lookup_dpm_cell("F 12.01.a", "0015", "0010")
    assert answer["found"] is True
    members = {row["dimension"]: row["member"] for row in answer["dimensions"]}
    assert members, "a reportable cell has dimension members"
    assert members["Counterparty sector"] == "Central banks and credit institutions"
    assert members["Calculation method"] == "Accumulated"


@needs_dpm2
def test_a_cell_and_its_table_answer_different_questions():
    """lookup_dpm_dimensions counts cells per member across the template; lookup_dpm_cell
    names the members of one cell. The two must not return the same shape."""
    cell = dpm_lookup.lookup_dpm_cell("F 12.01.a", "0015", "0010")
    table = dpm_lookup.lookup_dpm_dimensions("F 12.01.a", "FINREP9")
    assert set(cell["dimensions"][0]) == {"dimension", "member", "definition"}
    assert set(table["dimensions"][0]) == {"dimension", "members"}
    assert "cells" in table["dimensions"][0]["members"][0]


# --- a host serialises what dispatch returns -------------------------------------------


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (datetime.date(2022, 12, 31), "2022-12-31"),
        (datetime.datetime(2022, 12, 31, 9, 30), "2022-12-31T09:30:00"),
        (decimal.Decimal("1.5"), 1.5),
        ({"a": [datetime.date(2026, 3, 30)]}, {"a": ["2026-03-30"]}),
        (("x", 1), ["x", 1]),
        ({"keep": None, "flag": True, "n": 3}, {"keep": None, "flag": True, "n": 3}),
    ],
)
def test_only_what_json_refuses_is_converted(value, expected):
    assert agent_tools.jsonable(value) == expected
    json.dumps(agent_tools.jsonable(value))


@needs_dpm2
def test_every_dpm_answer_survives_a_plain_json_dumps():
    """A host hands the answer back to the model with json.dumps and no `default=`. The
    DPM's module validity window arrives from DuckDB as two dates, which raises there -
    losing the turn rather than the answer."""
    calls = {
        "lookup_dpm_table": {"table": "F 12.01.a"},
        "lookup_dpm_cell": {"table": "F 12.01.a", "row": "0015", "column": "0010", "sheet": None},
        "lookup_dpm_dimensions": {"table": "F 12.01.a", "module": "FINREP9", "version": None},
    }
    for name, args in calls.items():
        answer = agent_tools.dispatch(name, args)
        assert answer["found"] is True, name
        json.dumps(answer)


# --- a null version must still scope the recursive query -------------------------------


@needs_dpm2
def test_sums_without_a_version_resolve_to_one_and_say_which():
    """A null version left the recursive query scoped to every version of the module at
    once: over two minutes for FINREP9, against 0.05s for one. It also left the caller
    unable to tell which framework it had been answered about."""
    newest = dpm_lookup.lookup_dpm_sums("F 12.01.a", "FINREP9")
    assert newest["found"] is True
    module, _, version = newest["module"].partition(" ")
    assert module == "FINREP9"
    assert version, "the answer must name the version it resolved to"
    assert newest["sums"] == dpm_lookup.lookup_dpm_sums("F 12.01.a", "FINREP9", version)["sums"]


@needs_dpm2
def test_a_template_in_a_module_carries_the_module_version_it_was_found_in():
    with dpm_lookup._connect() as con:
        found = dpm_lookup._table_version(con, "F 12.01.a", "FINREP9")
    assert found["module_version"]


# --- trying a tool from a shell --------------------------------------------------------


@pytest.mark.parametrize(
    ("pairs", "expected"),
    [
        (["table=F 12.01.a", "module=FINREP9"], {"table": "F 12.01.a", "module": "FINREP9"}),
        (["version=null"], {"version": None}),  # what the schemas offer for "newest"
        (["member=Credit institutions"], {"member": "Credit institutions"}),
        (["expression=a=b"], {"expression": "a=b"}),  # split once: a value may carry one
        ([], {}),
    ],
)
def test_key_value_arguments_become_a_tool_call(pairs, expected):
    assert agent_tools.parse_arguments(pairs) == expected


def test_an_argument_without_a_value_is_refused_rather_than_guessed():
    with pytest.raises(SystemExit, match="key=value"):
        agent_tools.parse_arguments(["table"])


# --- the enum, the arms and the definitions must agree ---------------------------------


def tool_names_named_in(source: str) -> set[str]:
    """Every `ToolName.X` the module mentions, by member name."""
    return {
        node.attr
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "ToolName"
    }


def test_every_tool_name_has_an_arm_and_every_arm_a_name():
    """A tool lives in the enum, in a `case` arm and in TOOLS. Removing it from the enum
    alone is the half-edit that hurts: match evaluates arms in order, so the first arm
    naming a member that is gone raises AttributeError and every tool dispatched after it
    fails with `type object 'ToolName' has no attribute ...`, however healthy it is."""
    named = tool_names_named_in(Path(agent_tools.__file__).read_text())
    assert named == {member.name for member in agent_tools.ToolName}


def test_dropping_a_member_but_not_its_arm_is_what_the_test_above_catches():
    """The failure reproduced: an arm outliving its member takes the later tools with it."""
    source = textwrap.dedent("""
        class ToolName:
            A = "a"

        def run(name):
            match name:
                case ToolName.B:
                    return 1
    """)
    assert tool_names_named_in(source) == {"B"}


@needs_dpm2
@pytest.mark.parametrize(
    ("call", "args"),
    [
        (dpm_lookup.lookup_dpm_table, ("F 12.01.a",)),
        (dpm_lookup.lookup_dpm_cell, ("F 12.01.a", "0015", "0010")),
        (dpm_lookup.lookup_dpm_dimensions, ("F 12.01.a", "FINREP9")),
        (dpm_lookup.lookup_dpm_sums, ("F 12.01.a", "FINREP9")),
    ],
)
def test_a_lookup_reached_past_dispatch_is_serialisable_too(call, args):
    """A host that imports the lookups rather than the dispatcher gets no conversion from
    jsonable(), so the module's validity window is cast to a string in the query itself.
    Reported as `TypeError: Object of type date is not JSON serializable` from inside a
    chainlit handler's json.dumps."""
    json.dumps(call(*args), ensure_ascii=False)


# --- reading a report back to the model ------------------------------------------------


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("dp1010005012", 1010005012),
        ("DP152217", 152217),
        ("152217", 152217),
        (152217, 152217),
        ("  dp152217 ", 152217),
        ("d152217", 152217),  # the prefix the taxonomy writes is optional either way
        ("dp", None),
        ("F_04.04.1", None),
        ("", None),
    ],
)
def test_a_reported_datapoint_id_is_read_with_or_without_its_prefix(given, expected):
    assert dpm_lookup.datapoint_id(given) == expected


@needs_dpm2
def test_a_datapoint_resolves_to_the_cell_it_is():
    answer = dpm_lookup.lookup_dpm_datapoint("dp152217")
    assert answer["found"] is True
    cell = answer["cells"][0]
    assert cell["table_code"] == "F_04.04.1"
    assert (cell["row_code"], cell["column_code"]) == ("0040", "0010")
    assert cell["row_label"] == "Credit institutions"
    assert {m["module"] for m in answer["modules"]} == {"FINREP9", "FINREP9DP"}


@needs_dpm2
def test_an_id_above_the_release_says_newer_release_rather_than_nothing():
    """An empty answer cannot tell a caller whether the id is wrong or the file is newer,
    and that is the whole question when a report will not resolve."""
    answer = dpm_lookup.lookup_dpm_datapoint("dp1010005012")
    assert answer["found"] is False
    assert answer["max_datapoint"] < 1010005012
    assert "newer release" in answer["message"]


@needs_dpm2
def test_an_id_within_range_is_not_blamed_on_the_release():
    answer = dpm_lookup.lookup_dpm_datapoint("dp999999999")
    assert answer["found"] is False
    assert "newer release" not in answer["message"]


@needs_dpm2
@pytest.mark.parametrize(
    ("code", "property_name"),
    [
        ("qGDF", "Name of Holding entity"),
        ("qBBE", "Location of activity"),
        ("ei1452", "Country where a service/activity is provided"),
    ],
)
def test_a_report_column_header_resolves_to_its_property(code, property_name):
    """The headers of the EBA's own sample file. They are property codes, and they live
    in the model rather than only in the taxonomy files."""
    answer = dpm_lookup.lookup_dpm_property(code)
    assert answer["found"] is True
    assert answer["properties"][0]["property"] == property_name


@needs_dpm2
def test_a_property_code_carries_the_releases_it_was_current_in():
    """A code is release-scoped: x21 through release 4.2, qx2013 after it. A header that
    resolves to nothing is more often the wrong release than the wrong file."""
    answer = dpm_lookup.lookup_dpm_property("qGDF")
    assert answer["properties"][0]["from_release"] == "4.0"
    assert answer["properties"][0]["until_release"] is None


@needs_dpm2
def test_a_key_header_carries_the_property_a_report_heads_its_column_with():
    """An open table is keyed on the headers the model marks IsKey, and their property
    codes are what a report writes beside datapoint and factValue."""
    answer = dpm_lookup.lookup_dpm_table("B_01.01")
    headers = answer["columns"] + answer["rows"]
    keys = [header for header in headers if header["is_key"]]
    assert keys, "every DORA template is keyed"
    assert all(header["property_code"] for header in keys)
    assert {header["property_code"] for header in keys} == {"ERI"}


@needs_dpm2
def test_a_header_appears_once_however_often_its_property_has_been_recoded():
    """The join to ItemCategory was unscoped, and 233 properties carry more than one code
    across releases, so a header came back once per code it had ever had - 11022
    duplicated headers, each putting a retired code into what a report is compared
    against. EndReleaseID IS NULL is the code in force, and there is exactly one."""
    for table in ("B_01.01", "F_04.04.1", "F_12.01.a", "Y_01_01"):
        answer = dpm_lookup.lookup_dpm_table(table)
        for axis in ("rows", "columns", "sheets"):
            codes = [header["code"] for header in answer[axis]]
            assert len(codes) == len(set(codes)), f"{table} {axis} repeats a header"


# --- a validation outcome, back to the rule --------------------------------------------


@needs_dpm2
def test_a_rule_code_is_one_rule_per_module_version():
    """A validation report names a code and a failing cell. v0174_m is the same check in
    every COREP_OF version that has it and an error in two of them and a warning in the
    third, so an outcome means nothing until the version it was raised under is known."""
    answer = dpm_lookup.lookup_dpm_rule("v0174_m")
    assert answer["found"] is True
    assert answer["tables"] == ["C_01.00"]
    by_version = {scope["version"]: scope for scope in answer["scopes"]}
    assert {scope["module"] for scope in answer["scopes"]} == {"COREP_OF"}
    assert by_version["3.1.0"]["severity"] == "error"
    assert by_version["4.1.0"]["severity"] == "warning"
    assert "not the same in all of them" in answer["message"]


@needs_dpm2
def test_a_rule_carries_the_cells_it_names_and_when_it_starts_applying():
    """The DPM resolved every leaf of the expression to a location, so the cells are a
    join rather than a parse of the DPM-XL in `expression`."""
    scope = dpm_lookup.lookup_dpm_rule("v0174_m")["scopes"][0]
    assert scope["from_submission_date"] == "2023-06-30"
    assert {(cell["row_code"], cell["column_code"]) for cell in scope["cells"]} == {
        ("0070", "0010"),
        ("0080", "0010"),
        ("0090", "0010"),
        ("0091", "0010"),
    }
    assert "{r0070} = {r0080}" in scope["expression"]


@needs_dpm2
@pytest.mark.parametrize("given", ["v23845_h", "V23845_H", "  v23845_h  "])
def test_a_rule_code_is_matched_however_it_is_written(given):
    """It arrives pasted out of a validation report, with whatever case and spacing."""
    assert dpm_lookup.lookup_dpm_rule(given)["tables"] == ["F_12.01.a"]


@needs_dpm2
def test_an_unknown_rule_code_points_at_the_release():
    """A rule retired before this release, or added after it, is simply not here - which
    is a different thing from a mistyped code and the answer says so."""
    answer = dpm_lookup.lookup_dpm_rule("v9999_x")
    assert answer["found"] is False
    assert "check the release before the code" in answer["message"]


def test_the_rule_lookup_is_dispatchable_and_says_what_is_missing(monkeypatch):
    monkeypatch.setattr(dpm_lookup, "DB", dpm_lookup.DB.with_name("absent.duckdb"))
    answer = agent_tools.dispatch("lookup_dpm_rule", {"rule_code": "v0174_m"})
    assert answer["found"] is False
    assert "fetch_dpm2" in answer["message"]
