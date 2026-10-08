"""The rule evaluator, on trees built by hand rather than read from the database.

The property worth protecting is the refusal: this implements four of the model's
thirty-eight operators, and a rule it cannot evaluate must say so. A validator that
silently skips what it cannot do reports a clean run over a report it never checked.
"""

import pytest

from check_instance import Node, Rule, Unsupported, evaluate
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
