"""Run a module's validation rules against a reported xBRL-CSV instance.

The DPM stores each rule as an expression tree, not only as the DPM-XL string, and it has
already resolved every leaf to the cells it names. So checking a report is an evaluation
over that tree rather than a parser: a leaf is the cells it names or a literal, and an
inner node applies its operator to its children.

    uv run check_instance.py Y_01.01 PSD_FRP 1.1.0 path/to/y_01.01.csv

The instance keys each fact by a datapoint id and nothing else. `dp<N>` is
`VariableVersion.VariableID` - not CellID and not VariableVID - which is what joins a
reported value back to a cell of a template.

**This covers four of the model's thirty-eight operators**: addition, and the three
comparisons PSD_FRP 1.1.0 uses. That is every rule of that module, and nowhere near every
rule of the model - DORA alone needs `isnull` and `if-then-else`. A rule using anything
else is reported as not evaluated, with the operator named. It is never counted as passing,
because a validator that quietly skips what it cannot do is worse than one that cannot do
it: the silence reads as a clean report.

A caveat on the EBA's published sample instances: they are structural, not valid. Their
values are uniform noise, so every arithmetic rule fails against them by construction.
They are good for checking that the datapoint mapping works and useless for checking
arithmetic.
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, NamedTuple

import duckdb

PACK = Path(__file__).parent
DIR = Path(os.environ.get("DPM2_DIR") or PACK / "source" / "dpm2")
DB = Path(os.environ.get("DPM2_DB") or DIR / "dpm2.duckdb")

# A cell of one template, as both the model and the instance can be keyed on it.
Cell = tuple[str, str, str]  # row, column, sheet


class Node(NamedTuple):
    """One node of a rule's expression tree."""

    parent: int | None
    is_leaf: bool
    symbol: str | None
    scalar: float | None


class Rule(NamedTuple):
    """One rule, ready to evaluate: its tree, and the cells each leaf names."""

    code: str
    severity: str
    root: int
    nodes: dict[int, Node]
    children: dict[int, list[int]]
    cells: dict[int, list[Cell]]


class Unsupported(Exception):
    """The tree uses an operator this evaluator does not implement."""


# Four of the model's operators. Comparisons are applied elementwise when one side is a
# single value and the other names several cells, which is how a sign rule covering
# twenty-two rows is expressed: `{(r0010, ..., r0220)} >= 0`.
COMPARISONS = {
    "=": lambda a, b: a == b,
    "<=": lambda a, b: a <= b,
    ">=": lambda a, b: a >= b,
}


def operand(rule: Rule, node_id: int, values: dict[Cell, float], col: str, sheet: str) -> list[float] | None:
    """A node's value here: a literal, a sum, or the cells it names. None if out of scope.

    Pure. An unreported cell counts as zero, which is what `default: 0` on the rule's
    scope means; a leaf that names no cell in this column and sheet puts the whole rule
    out of scope here rather than contributing nothing to it.
    """
    node = rule.nodes[node_id]
    if node.is_leaf:
        if node.scalar is not None:
            return [node.scalar]
        here = [c for c in rule.cells.get(node_id, []) if c[1] == col and c[2] == sheet]
        return [values.get(c, 0.0) for c in here] if here else None
    if node.symbol == "+":
        # A loop rather than a comprehension: `any(p is None for p in parts)` does not
        # narrow the optional away for a type checker, and the narrowing is the point.
        total = 0.0
        for child in rule.children[node_id]:
            part = operand(rule, child, values, col, sheet)
            if part is None:
                return None
            total += sum(part)
        return [total]
    raise Unsupported(node.symbol or "?")


def evaluate(rule: Rule, values: dict[Cell, float], col: str, sheet: str) -> bool | None:
    """Whether the rule holds for one column and sheet, or None where it does not reach.

    Raises Unsupported rather than guessing, so the caller can report the rule as
    unevaluated instead of counting it as passed.
    """
    symbol = rule.nodes[rule.root].symbol
    if symbol not in COMPARISONS:
        raise Unsupported(symbol or "?")
    sides = rule.children[rule.root]
    if len(sides) != 2:
        return None
    left = operand(rule, sides[0], values, col, sheet)
    right = operand(rule, sides[1], values, col, sheet)
    if left is None or right is None:
        return None
    holds = COMPARISONS[symbol]
    if len(right) == 1 and len(left) > 1:
        return all(holds(x, right[0]) for x in left)
    if len(left) == 1 and len(right) > 1:
        return all(holds(left[0], x) for x in right)
    return holds(left[0], right[0])


# --------------------------------------------------------------------------------------
# Loading. Everything above is pure; everything below reads a file or the database.
# --------------------------------------------------------------------------------------

GRID_SQL = """
SELECT vv.VariableID AS dp, hr.Code AS row_code, hc.Code AS col, coalesce(hs.Code, '') AS sheet
FROM   ModuleVersionComposition mvc
JOIN   TableVersion tv USING (TableVID)
JOIN   ModuleVersion mv USING (ModuleVID)
JOIN   TableVersionCell c ON c.TableVID = tv.TableVID
JOIN   VariableVersion vv ON vv.VariableVID = c.VariableVID
JOIN   Cell cc ON cc.CellID = c.CellID
JOIN   TableVersionHeader tr ON tr.TableVID = tv.TableVID AND tr.HeaderID = cc.RowID
JOIN   HeaderVersion hr ON hr.HeaderVID = tr.HeaderVID
JOIN   TableVersionHeader tc ON tc.TableVID = tv.TableVID AND tc.HeaderID = cc.ColumnID
JOIN   HeaderVersion hc ON hc.HeaderVID = tc.HeaderVID
LEFT JOIN TableVersionHeader ts ON ts.TableVID = tv.TableVID AND ts.HeaderID = cc.SheetID
LEFT JOIN HeaderVersion hs ON hs.HeaderVID = ts.HeaderVID
WHERE  tv.Code = ? AND mv.Code = ? AND mv.VersionNumber = ?
"""

NODES_SQL = """
SELECT op.Code AS code, os.Severity AS severity, n.NodeID AS node_id,
       n.ParentNodeID AS parent, n.IsLeaf <> 0 AS is_leaf, o.Symbol AS symbol, n.Scalar AS scalar
FROM   Operation op
JOIN   OperationVersion ov ON ov.OperationID = op.OperationID
JOIN   OperationScope os ON os.OperationVID = ov.OperationVID
JOIN   OperationScopeComposition osc ON osc.OperationScopeID = os.OperationScopeID
JOIN   ModuleVersion mv ON mv.ModuleVID = osc.ModuleVID
JOIN   OperationNode n ON n.OperationVID = ov.OperationVID
LEFT JOIN Operator o ON o.OperatorID = n.OperatorID
WHERE  mv.Code = ? AND mv.VersionNumber = ?
"""

LEAF_SQL = """
SELECT r.NodeID AS node_id, l."Row" AS row_code, l."Column" AS col, coalesce(l.Sheet, '') AS sheet
FROM   OperandReference r
JOIN   OperandReferenceLocation l USING (OperandReferenceID)
WHERE  l."Table" = ?
"""


def read_facts(path: Path) -> dict[int, float]:
    """The instance, as datapoint id to value."""
    with path.open(encoding="utf-8") as fh:
        return {int(r["datapoint"].removeprefix("dp")): float(r["factValue"]) for r in csv.DictReader(fh)}


def load(table: str, module: str, version: str) -> tuple[dict[int, Cell], list[Rule]]:
    """The template's cells by datapoint id, and every rule that can reach the template."""
    if not DB.exists():
        raise SystemExit(f"{DB} does not exist - run source/fetch_dpm2.py first")
    con = duckdb.connect(str(DB), read_only=True)
    try:
        grid = {
            dp: (row, col, sheet) for dp, row, col, sheet in con.execute(GRID_SQL, [table, module, version]).fetchall()
        }
        leaves: dict[int, list[Cell]] = defaultdict(list)
        for node_id, row, col, sheet in con.execute(LEAF_SQL, [table]).fetchall():
            leaves[node_id].append((row, col, sheet))
        raw = con.execute(NODES_SQL, [module, version]).fetchall()
    finally:
        con.close()

    nodes: dict[str, dict[int, Node]] = defaultdict(dict)
    severity: dict[str, str] = {}
    for code, sev, node_id, parent, is_leaf, symbol, scalar in raw:
        nodes[code][node_id] = Node(parent, bool(is_leaf), symbol, None if scalar is None else float(scalar))
        severity[code] = sev

    rules = []
    for code, tree in nodes.items():
        cells = {nid: leaves[nid] for nid in tree if nid in leaves}
        if not cells:
            continue  # the rule names no cell of this template
        children: dict[int, list[int]] = defaultdict(list)
        root = None
        for nid, node in tree.items():
            if node.parent is None:
                root = nid
            else:
                children[node.parent].append(nid)
        if root is not None:
            rules.append(Rule(code, severity[code], root, tree, children, cells))
    return grid, rules


def verdicts(rules: list[Rule], values: dict[Cell, float]) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    """Each rule evaluated over every column/sheet the report carries: held, failed, skipped.

    Pure over what was loaded, so it is testable without a database or a file. A rule the
    checker cannot evaluate lands in `skipped` and never in `passed`: a validator that
    quietly skips what it cannot do reads as a clean report, which is worse than refusing.
    """
    axes = sorted({(col, sheet) for _, col, sheet in values})
    passed: dict[str, Any] = {}
    failed: dict[str, Any] = {}
    skipped: dict[str, str] = {}
    for rule in rules:
        outcome = [0, 0]
        try:
            for col, sheet in axes:
                verdict = evaluate(rule, values, col, sheet)
                if verdict is not None:
                    outcome[0 if verdict else 1] += 1
        except Unsupported as exc:
            skipped[rule.code] = str(exc)
            continue
        if sum(outcome) == 0:
            continue
        (failed if outcome[1] else passed)[rule.code] = (rule.severity, outcome)
    return passed, failed, skipped


def check_report(table: str, module: str, version: str, instance: str) -> dict[str, Any]:
    """Every rule of one module version, run against one reported file.

    The answer separates three things a caller must not confuse: rules that hold, rules
    that fail, and rules this checker cannot evaluate - four of the model's thirty-eight
    operators. An unevaluated rule is named with the operator it needs, never counted as
    passing.

    `unmapped` is the count of facts whose datapoint id is not a cell of this template:
    a large one usually means the file is for another module version, not that the report
    is wrong.
    """
    path = Path(instance)
    if not DB.exists():
        return {"found": False, "message": f"{DB} does not exist - run source/fetch_dpm2.py first"}
    if not path.is_file():
        # The name only, never the content: a wrong path is a typo to correct, and echoing
        # a file a model named is how a tool becomes a way to read one.
        return {"found": False, "message": f"No such report file: {path.name}"}
    # The report first: it is the cheap check, and a bad path or a wrong file should not
    # cost a database load to find out about.
    try:
        facts = read_facts(path)
    except (OSError, UnicodeDecodeError, csv.Error, KeyError, ValueError) as exc:
        return {
            "found": False,
            "message": (
                f"{path.name} is not an xBRL-CSV report this can read ({type(exc).__name__}). "
                "It wants a datapoint column of dp<N> ids and a factValue column."
            ),
        }
    try:
        grid, rules = load(table, module, version)
    except duckdb.Error as exc:
        # An unreadable or half-downloaded database, which a traceback out of a tool call
        # turns into a lost turn rather than something the caller can act on.
        return {"found": False, "message": f"{DB} could not be read ({type(exc).__name__}): {exc}"}

    values = {grid[dp]: value for dp, value in facts.items() if dp in grid}
    passed, failed, skipped = verdicts(rules, values)
    return {
        "found": True,
        "table": table,
        "module": f"{module} {version}",
        "facts": len(facts),
        "mapped": len(values),
        "unmapped": len(facts) - len(values),
        "hold": sorted(passed),
        "fail": [
            {"rule_code": code, "severity": severity, "fails": bad, "of": ok + bad}
            for code, (severity, (ok, bad)) in sorted(failed.items())
        ],
        "not_evaluated": [{"rule_code": code, "needs": needs} for code, needs in sorted(skipped.items())],
        "message": (
            "fail lists rules that do not hold, with how many column/sheet combinations of how "
            "many. not_evaluated is this checker's limit, not a pass: it implements four of the "
            "model's thirty-eight operators and names the one each skipped rule needs. A large "
            "unmapped count means the file is probably for another module version."
        ),
    }


CHECK_REPORT_TOOL_NAME = "check_report"

CHECK_REPORT_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": CHECK_REPORT_TOOL_NAME,
        "description": (
            "Run a module version's validation rules against a reported xBRL-CSV file and say "
            "which hold, which fail and which could not be evaluated. Use it to check a figure "
            "or an aggregate against the EBA's own rules rather than against arithmetic you "
            "wrote. Covers four of the model's thirty-eight operators - addition and three "
            "comparisons - and names the operator a rule it skipped would need. A skipped rule "
            "is never a passing rule. Needs the DPM database and a file on this machine."
        ),
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "table": {
                    "type": "string",
                    "description": "Template code as the model writes it, e.g. Y_01.01 or F_04.04.1.",
                },
                "module": {"type": "string", "description": "Module code, e.g. PSD_FRP or FINREP9."},
                "version": {
                    "type": "string",
                    "description": "Module version, e.g. 1.1.0. Required: a rule belongs to one version.",
                },
                "instance": {"type": "string", "description": "Path to the xBRL-CSV report file."},
            },
            "required": ["table", "module", "version", "instance"],
            "additionalProperties": False,
        },
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("table", help="template code as the model writes it, e.g. Y_01.01")
    parser.add_argument("module", help="module code, e.g. PSD_FRP")
    parser.add_argument("version", help="module version, e.g. 1.1.0")
    parser.add_argument("instance", type=Path, help="an xBRL-CSV report file, e.g. y_01.01.csv")
    args = parser.parse_args()

    # The same answer the tool returns, printed: one implementation, so the CLI cannot
    # drift from what an agent is told.
    answer = check_report(args.table, args.module, args.version, str(args.instance))
    if not answer["found"]:
        raise SystemExit(answer["message"])

    print(f"{answer['facts']} fact(s) in the instance, {answer['mapped']} of them cells of {args.table}")
    if answer["unmapped"]:
        print(f"  {answer['unmapped']} did not map; is the instance for {args.module} {args.version}?")

    evaluated = len(answer["hold"]) + len(answer["fail"])
    print(f"\n{evaluated} rule(s) evaluated: {len(answer['hold'])} hold, {len(answer['fail'])} do not")
    for bad in answer["fail"]:
        print(
            f"  {bad['rule_code']:12} {bad['severity']:8} fails {bad['fails']} of {bad['of']} "
            "column/sheet combination(s)"
        )
    if answer["not_evaluated"]:
        print(f"\n{len(answer['not_evaluated'])} rule(s) NOT evaluated - this checker implements four operators:")
        for skipped in answer["not_evaluated"]:
            print(f"  {skipped['rule_code']:12} needs {skipped['needs']!r}")
    sys.exit(1 if answer["fail"] else 0)


if __name__ == "__main__":
    main()
