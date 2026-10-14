"""The rule evaluator, on trees built by hand rather than read from the database.

The property worth protecting is the refusal: this implements four of the model's
thirty-eight operators, and a rule it cannot evaluate must say so. A validator that
silently skips what it cannot do reports a clean run over a report it never checked.
"""

import pytest

import check_instance
import dpm_lookup
from check_instance import Node, Rule, Unsupported, evaluate, verdicts
from conftest import needs_dpm2


def tree(root_symbol, *, leaves, root_children, nested=None):
    """A rule of one comparison over leaves, each leaf naming cells or holding a scalar."""
    nodes = {0: Node(parent=None, is_leaf=False, symbol=root_symbol, scalar=None)}
    children = {0: list(root_children)}
    cells = {}
    for nid, spec in leaves.items():
        if isinstance(spec, (int, float)):
            nodes[nid] = Node(parent=0, is_leaf=True, symbol=None, scalar=float(spec))
        else:
            nodes[nid] = Node(parent=0, is_leaf=True, symbol=None, scalar=None)
            cells[nid] = list(spec)
    for nid, (symbol, kids) in (nested or {}).items():
        nodes[nid] = Node(parent=0, is_leaf=False, symbol=symbol, scalar=None)
        children[nid] = list(kids)
    return Rule("test_rule", "warning", 0, nodes, children, cells)


C = ("0010", "0010", "0010")  # row, column, sheet


def test_a_sum_that_holds():
    rule = tree(
        "=",
        leaves={1: [C], 3: [("0030", "0010", "0010")], 4: [("0040", "0010", "0010")]},
        root_children=[2, 1],
        nested={2: ("+", [3, 4])},
    )
    values = {C: 100.0, ("0030", "0010", "0010"): 40.0, ("0040", "0010", "0010"): 60.0}
    assert evaluate(rule, values, "0010", "0010") is True


def test_a_sum_that_does_not():
    rule = tree(
        "=",
        leaves={1: [C], 3: [("0030", "0010", "0010")], 4: [("0040", "0010", "0010")]},
        root_children=[2, 1],
        nested={2: ("+", [3, 4])},
    )
    values = {C: 99.0, ("0030", "0010", "0010"): 40.0, ("0040", "0010", "0010"): 60.0}
    assert evaluate(rule, values, "0010", "0010") is False


def test_an_unreported_cell_of_a_sum_counts_as_zero():
    """What `default: 0` on the rule's scope means."""
    rule = tree(
        "=",
        leaves={1: [C], 3: [("0030", "0010", "0010")], 4: [("0040", "0010", "0010")]},
        root_children=[2, 1],
        nested={2: ("+", [3, 4])},
    )
    values = {C: 40.0, ("0030", "0010", "0010"): 40.0}  # row 0040 absent
    assert evaluate(rule, values, "0010", "0010") is True


def test_a_rule_that_does_not_reach_this_column_answers_nothing():
    rule = tree("=", leaves={1: [C], 2: [("0030", "0010", "0010")]}, root_children=[1, 2])
    assert evaluate(rule, {C: 1.0}, "0020", "0010") is None


@pytest.mark.parametrize(
    ("symbol", "total", "holds"), [("<=", 100.0, True), ("<=", 101.0, False), (">=", 100.0, True), (">=", 99.0, False)]
)
def test_the_other_two_comparisons(symbol, total, holds):
    rule = tree(symbol, leaves={1: [C], 2: 100.0}, root_children=[1, 2])
    assert evaluate(rule, {C: total}, "0010", "0010") is holds


def test_a_scalar_is_compared_against_every_cell_the_other_side_names():
    """How a sign rule over twenty-two rows is expressed: {(r0010, ..., r0220)} >= 0."""
    many = [("0010", "0010", "0010"), ("0020", "0010", "0010"), ("0030", "0010", "0010")]
    rule = tree(">=", leaves={1: many, 2: 0.0}, root_children=[1, 2])
    assert evaluate(rule, dict.fromkeys(many, 5.0), "0010", "0010") is True
    assert evaluate(rule, {**dict.fromkeys(many, 5.0), many[1]: -1.0}, "0010", "0010") is False


# --- the refusal ----------------------------------------------------------------------


def test_an_operator_the_evaluator_does_not_implement_raises():
    """`isnull`, which DORA needs. Never silently skipped, never counted as passing."""
    rule = tree("isnull", leaves={1: [C]}, root_children=[1])
    with pytest.raises(Unsupported, match="isnull"):
        evaluate(rule, {C: 1.0}, "0010", "0010")


def test_an_unsupported_operator_inside_an_arm_raises_too():
    rule = tree(
        "=",
        leaves={1: [C], 3: [("0030", "0010", "0010")], 4: [("0040", "0010", "0010")]},
        root_children=[2, 1],
        nested={2: ("*", [3, 4])},
    )
    with pytest.raises(Unsupported, match=r"\*"):
        evaluate(rule, {C: 1.0, ("0030", "0010", "0010"): 1.0, ("0040", "0010", "0010"): 1.0}, "0010", "0010")


# --- against the real model -------------------------------------------------------------


@needs_dpm2
def test_every_psd_frp_rule_for_y_01_01_can_be_evaluated():
    """The claim the docstring makes: four operators cover that module completely."""
    from check_instance import load

    grid, rules = load("Y_01.01", "PSD_FRP", "1.1.0")
    assert len(grid) == 324, "the pack has 324 datapoints for Y_01_01"
    values = dict.fromkeys(grid.values(), 1.0)
    for rule in rules:
        for col, sheet in sorted({(c, s) for _, c, s in values})[:1]:
            evaluate(rule, values, col, sheet)  # raises Unsupported if any operator is missing


# --- the whole run, as the tool answers it ---------------------------------------------


def test_each_rule_lands_in_exactly_one_bucket():
    """verdicts separates three things a caller must not confuse. A rule the checker
    cannot evaluate is in `skipped` and in neither of the others: counting it as passing
    would report a clean run over a report that was never checked."""
    holds = tree(
        "=",
        leaves={1: [C], 3: [("0030", "0010", "0010")], 4: [("0040", "0010", "0010")]},
        root_children=[2, 1],
        nested={2: ("+", [3, 4])},
    )._replace(code="holds")
    fails = holds._replace(code="fails")
    cannot = holds._replace(code="cannot", nodes=holds.nodes | {0: Node(None, False, "*", None)})
    values = {C: 100.0, ("0030", "0010", "0010"): 40.0, ("0040", "0010", "0010"): 60.0}

    passed, failed, skipped = verdicts([holds, cannot], values)
    assert set(passed) == {"holds"}
    assert failed == {}
    assert set(skipped) == {"cannot"}

    passed, failed, skipped = verdicts([fails], {**values, C: 99.0})
    assert set(failed) == {"fails"}
    assert passed == {} and skipped == {}


def test_a_rule_naming_no_reported_axis_is_counted_nowhere():
    """An empty report evaluates nothing, which is not the same as everything holding."""
    rule = tree("=", leaves={1: [C], 2: 0}, root_children=[1, 2])
    assert verdicts([rule], {}) == ({}, {}, {})


def test_a_missing_report_names_the_file_and_not_its_content(tmp_path, monkeypatch):
    """A wrong path is a typo to correct. Echoing a file a model named is how a lookup
    tool becomes a way to read one, so only the name comes back."""
    monkeypatch.setattr(check_instance, "DB", tmp_path / "dpm2.duckdb")
    (tmp_path / "dpm2.duckdb").write_text("not really a database")
    answer = check_instance.check_report("Y_01.01", "PSD_FRP", "1.1.0", str(tmp_path / "absent.csv"))
    assert answer["found"] is False
    assert "absent.csv" in answer["message"]


def test_a_file_that_is_not_an_xbrl_csv_report_says_so(tmp_path, monkeypatch):
    monkeypatch.setattr(check_instance, "DB", tmp_path / "dpm2.duckdb")
    (tmp_path / "dpm2.duckdb").write_text("not really a database")
    report = tmp_path / "wrong.csv"
    report.write_text("a,b\n1,2\n", encoding="utf-8")
    answer = check_instance.check_report("Y_01.01", "PSD_FRP", "1.1.0", str(report))
    assert answer["found"] is False
    assert "factValue" in answer["message"]
    assert "1,2" not in answer["message"], "the content of the file must not come back"


def test_without_the_database_it_says_what_to_run(tmp_path, monkeypatch):
    monkeypatch.setattr(check_instance, "DB", tmp_path / "absent.duckdb")
    answer = check_instance.check_report("Y_01.01", "PSD_FRP", "1.1.0", str(tmp_path / "any.csv"))
    assert answer["found"] is False
    assert "fetch_dpm2.py" in answer["message"]


@needs_dpm2
def test_a_report_of_ones_fails_the_sums_and_skips_nothing(tmp_path):
    """Against PSD_FRP 1.1.0 every rule is evaluable, so not_evaluated must be empty -
    the claim the module docstring makes, checked through the tool rather than around it.
    A report where every cell is 1.0 cannot satisfy a sum, so the failures are expected."""
    from check_instance import load

    grid, _ = load("Y_01.01", "PSD_FRP", "1.1.0")
    report = tmp_path / "ones.csv"
    rows = "\n".join(f"dp{dp},1.0" for dp in sorted(grid))
    report.write_text(f"datapoint,factValue\n{rows}\n", encoding="utf-8")

    answer = check_instance.check_report("Y_01.01", "PSD_FRP", "1.1.0", str(report))
    assert answer["found"] is True
    assert answer["module"] == "PSD_FRP 1.1.0"
    assert answer["facts"] == answer["mapped"] == len(grid)
    assert answer["unmapped"] == 0
    assert answer["not_evaluated"] == [], "four operators cover this module"
    assert answer["fail"], "a report of ones does not add up"
    assert {bad["severity"] for bad in answer["fail"]} <= {"error", "warning"}


def test_an_unreadable_database_answers_rather_than_raising(tmp_path, monkeypatch):
    """A traceback out of a tool call loses the turn; a message is something to act on."""
    monkeypatch.setattr(check_instance, "DB", tmp_path / "dpm2.duckdb")
    (tmp_path / "dpm2.duckdb").write_text("not really a database")
    report = tmp_path / "ok.csv"
    report.write_text("datapoint,factValue\ndp1,1.0\n", encoding="utf-8")
    answer = check_instance.check_report("Y_01.01", "PSD_FRP", "1.1.0", str(report))
    assert answer["found"] is False
    assert "could not be read" in answer["message"]


# --- open tables, and literals that are not numbers ------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (0, 0.0),
        ("12.5", 12.5),
        (None, None),
        ("^[A-Z0-9]{18}[0-9]{2}$", "^[A-Z0-9]{18}[0-9]{2}$"),  # DORA checks an LEI this way
        ("2024-01-01", "2024-01-01"),
    ],
)
def test_a_literal_is_a_number_where_it_is_one_and_itself_where_it_is_not(raw, expected):
    assert check_instance.scalar(raw) == expected


def test_a_non_numeric_literal_is_unsupported_rather_than_a_crash():
    """Loading DORA raised ValueError on a regular expression, taking the whole module
    down. A literal with no arithmetic belongs in not_evaluated with everything else."""
    rule = tree("=", leaves={1: [C], 2: 0}, root_children=[1, 2])
    rule = rule._replace(nodes=rule.nodes | {2: Node(parent=0, is_leaf=True, symbol=None, scalar="^[A-Z]{2}$")})
    with pytest.raises(Unsupported, match=r"\^\[A-Z\]"):
        evaluate(rule, {C: 1.0}, "0010", "")


def test_records_of_an_open_table_are_counted_even_though_one_is_checked():
    """An open table's report has one row per record, all carrying the same datapoint
    ids. The dict keeps the last; the count is how a caller learns the rest existed."""
    rows = [
        {"datapoint": "dp1", "factValue": "10"},
        {"datapoint": "dp2", "factValue": "20"},
        {"datapoint": "dp1", "factValue": "30"},
    ]
    facts, read = check_instance.facts_by_datapoint(rows)
    assert facts == {1: 30.0, 2: 20.0}
    assert read == 3


@needs_dpm2
def test_an_open_template_has_cells_and_every_rule_refuses(tmp_path):
    """Every DORA template is open-rowed, so its cells carry no row header and the DPM
    writes the coordinate `r*`. An inner join on that header dropped all fourteen
    templates silently - a report checked against nothing reads as a report that passed."""
    from check_instance import load

    grid, rules = load("B_01.01", "DORA", "1.1.0")
    assert grid, "an open template still has cells"
    assert {row for row, _, _ in grid.values()} == {"*"}
    assert rules, "DORA's rules reach the template"

    report = tmp_path / "records.csv"
    records = "\n".join(f"dp{dp},{1000 + n}" for n in range(3) for dp in sorted(grid))
    report.write_text(f"datapoint,factValue\n{records}\n", encoding="utf-8")

    answer = check_instance.check_report("B_01.01", "DORA", "1.1.0", str(report))
    assert answer["mapped"] == len(grid) and answer["unmapped"] == 0
    assert answer["records"] == 3 * len(grid)
    assert "open axis" in answer["message"]
    assert answer["hold"] == [] and answer["fail"] == [], "DORA's rules are not arithmetic"
    assert {skipped["needs"] for skipped in answer["not_evaluated"]} >= {"if-then-else"}


# --- what a file is, before whether it holds -------------------------------------------


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        (["datapoint", "factValue"], []),
        (["datapoint", "factValue", "qGDF", "qBBE", "ei1452"], ["qGDF", "qBBE", "ei1452"]),
        (["factValue", "datapoint", "CPS"], ["CPS"]),
        ([], []),
    ],
)
def test_the_columns_after_the_fixed_two_are_the_open_dimensions(header, expected):
    assert check_instance.open_dimension_columns(header) == expected


@needs_dpm2
def test_a_file_from_another_release_says_so_rather_than_mapping_nothing(tmp_path):
    """The EBA's own sample, whose datapoints are above this release. check_report would
    call this 'nothing mapped', which reads like a bad report rather than a newer file."""
    report = tmp_path / "sample.csv"
    report.write_text(
        "datapoint,factValue,qCDF,qBBE,ei1452\n"
        "dp1010005012,58994,pipwgiwl,eba_GA:AL,eba_GA:AL\n"
        "dp1010005011,76396,pipwgiwl,eba_GA:AL,eba_GA:AL\n"
        "dp1010005012,58994,hhpgygtl,eba_GA:AT,eba_GA:AT\n"
        "dp1010005011,76396,hhpgygtl,eba_GA:AT,eba_GA:AT\n",
        encoding="utf-8",
    )
    answer = check_instance.explain_report(str(report))
    assert answer["found"] is True
    assert answer["records"] == 4 and answer["facts"] == 2
    assert answer["tables"] == [] and answer["modules"] == []
    assert "None of the" in answer["message"]
    assert "one row per record" in answer["message"]
    headers = {column["code"]: column for column in answer["columns"]}
    assert headers["qCDF"]["properties"][0]["property"] == "Name of entity"
    assert headers["ei1452"]["properties"][0]["property"] == "Country where a service/activity is provided"


@needs_dpm2
def test_a_file_of_this_release_names_its_template_and_modules(tmp_path):
    from check_instance import load

    grid, _ = load("Y_01.01", "PSD_FRP", "1.1.0")
    report = tmp_path / "y0101.csv"
    rows = "\n".join(f"dp{dp},1.0" for dp in sorted(grid))
    report.write_text(f"datapoint,factValue\n{rows}\n", encoding="utf-8")

    answer = check_instance.explain_report(str(report), limit=3)
    assert answer["tables"] == ["Y_01.01"]
    assert any(module.startswith("PSD_FRP") for module in answer["modules"])
    assert answer["columns"] == [], "this template has no open dimension"
    assert len(answer["datapoints"]) == 3, "limit is a sample, not the whole file"


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        ({}, "not both and not neither"),
        ({"instance": "a.csv", "text": "datapoint,factValue\n"}, "not both and not neither"),
    ],
)
def test_a_report_comes_from_a_path_or_from_text_but_not_both(kwargs, expected):
    """Guessing which of two sources was meant is how the wrong report gets explained."""
    assert expected in check_instance.explain_report(**kwargs)["message"]


def test_the_header_and_the_facts_are_read_in_one_pass():
    lines = [
        "datapoint,factValue,qGDF",
        "dp1,10,pipwgiwl",
        "dp2,20,pipwgiwl",
        "dp1,30,hhpgygtl",
    ]
    header, facts, records = check_instance.header_and_facts(lines)
    assert header == ["datapoint", "factValue", "qGDF"]
    assert facts == {1: 30.0, 2: 20.0}
    assert records == 3


@needs_dpm2
def test_pasted_text_is_read_like_a_file(tmp_path):
    """A report arrives in a conversation as often as on disk."""
    report = "datapoint,factValue\ndp152217,1.0\n"
    path = tmp_path / "one.csv"
    path.write_text(report, encoding="utf-8")

    pasted = check_instance.explain_report(text=report)
    on_disk = check_instance.explain_report(str(path))
    assert pasted["file"] == "pasted text" and on_disk["file"] == "one.csv"
    assert pasted["datapoints"] == on_disk["datapoints"]
    assert pasted["tables"] == on_disk["tables"] == ["F_04.04.1"]


# --- the report's columns against the template's keys ----------------------------------


@pytest.mark.parametrize(
    ("header", "expected", "unexpected", "missing"),
    [
        (["datapoint", "factValue", "qCDF"], ["qCDF"], [], []),
        (["datapoint", "factValue", "qGDF"], ["qCDF"], ["qGDF"], ["qCDF"]),
        (["datapoint", "factValue"], ["qCDF"], [], ["qCDF"]),
        (["datapoint", "factValue", "qCDF"], [], ["qCDF"], []),
        (["datapoint", "factValue", "qCDF"], [None, "qCDF"], [], []),  # a header with no property
    ],
)
def test_a_near_miss_in_a_column_code_is_the_only_thing_that_catches_it(header, expected, unexpected, missing):
    """qCDF is Name of entity and qGDF is Name of Holding entity. Both resolve, so a
    header resolving to a property proves nothing about which template it belongs to."""
    answer = check_instance.key_columns(header, expected)
    assert answer["unexpected"] == unexpected
    assert answer["missing"] == missing


@needs_dpm2
def test_a_closed_template_has_nothing_to_compare():
    """A closed template is keyed on nothing, so there is no comparison to report - not
    an empty one, which would read as "checked, and the report carries no keys"."""
    from check_instance import load

    grid, _ = load("Y_01.01", "PSD_FRP", "1.1.0")
    rows = "\n".join(f"dp{dp},1.0" for dp in sorted(grid)[:3])
    answer = check_instance.explain_report(text=f"datapoint,factValue\n{rows}\n", limit=3)
    assert answer["tables"] == ["Y_01.01"]
    assert answer["key_dimensions"] is None


@needs_dpm2
def test_a_template_the_model_gives_no_key_is_not_compared(monkeypatch):
    """`expected: []` would make every dimension column unexpected and the message would
    blame the report - "keyed on  and the report carries qCDF" - for what the model never
    said. No keys, no comparison."""
    monkeypatch.setattr(
        dpm_lookup,
        "lookup_dpm_table",
        lambda table: {"found": True, "columns": [], "rows": []},
    )
    monkeypatch.setattr(
        dpm_lookup,
        "lookup_dpm_datapoint",
        lambda dp: {"found": True, "cells": [{"table_code": "X_01.01"}], "modules": [], "datapoint": dp},
    )
    answer = check_instance.explain_report(text="datapoint,factValue,qCDF\ndp1,1.0,abc\n")
    assert answer["tables"] == ["X_01.01"]
    assert answer["key_dimensions"] is None
    assert "does not line up" not in answer["message"]
