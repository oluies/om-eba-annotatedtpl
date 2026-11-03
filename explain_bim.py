"""Explain an SSAS tabular model whose measures name DPM coordinates.

A `.bim` file is the JSON of a tabular model - Microsoft's Tabular Model Scripting
Language, TMSL - and plenty of tools will already tell you its tables, its relationships
and the size of its columns. None of them can tell you what the model *means*, because the
meaning is in strings like this, inside the DAX of a measure:

    CALCULATE (
        SUM ( 'Fakta_Motpartsexponering'[_VardeDecimal] ),
        'Dim_C'[TabellKod] = "C 28.00",
        'Dim_C'[RadKod]    = "999",
        'Dim_C'[KolumnKod] = "330"
    )

That is a cell of a supervisory reporting template, and the EBA's data point model knows
what it is, whether it still exists, what its row says in Swedish, and which validation
rules will reject a report that gets it wrong. This resolves every such coordinate in a
model against the DPM and says so.

    uv run explain_bim.py Model.bim                      # what the model is
    uv run explain_bim.py Model.bim --coordinates        # every coordinate, resolved
    uv run explain_bim.py Model.bim --unresolved         # only the ones the DPM does not have
    uv run explain_bim.py Model.bim --measure "Exponering efter CRM"
    uv run explain_bim.py Model.bim --release 4.3        # ask an older release
    uv run explain_bim.py Model.bim --coordinates --csv  # for a spreadsheet

The unresolved list is the point of the exercise. A model is written by hand against the
release that was current when someone wrote it, and a coordinate that has since been
withdrawn, moved or renumbered goes on returning a number - the wrong one, or none - with
nothing anywhere saying so.

The file is read and never written. A `.bim` holds a connection string, so nothing here
prints the data source's address unless asked with --source.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

import dpm_lookup

# The statement that says what a cell is lives beside the generators, and this reads it
# from there rather than writing a second one: the DPM's own schema does not hold a row
# code next to a column code, and the join that produces them is the kind of thing that is
# right in one place and subtly wrong in two.
sys.path.insert(0, str(Path(__file__).resolve().parent / "source"))

import gen_wasm_data  # noqa: E402

# `'Dim_C'[TabellKod] = "C 28.00"`. The dimension table differs per framework - Dim_C,
# Dim_F, Dim_M, Dim_R - so the table name is not anchored; what is anchored is the three
# column names, which are the convention this model uses for a DPM coordinate.
TEMPLATE = re.compile(r"\[TabellKod\]\s*=\s*\"([^\"]+)\"")
ROW = re.compile(r"\[RadKod\]\s*=\s*\"([^\"]+)\"")
COLUMN = re.compile(r"\[KolumnKod\]\s*=\s*\"([^\"]+)\"")
# `IN { "C 01.00", "C 02.00" }` is a different shape and is counted rather than guessed at.
IN_LIST = re.compile(r"\[(?:TabellKod|RadKod|KolumnKod)\]\s*IN\s*\{")


class BimMeasure(BaseModel):
    """One measure of a tabular model, as much of it as this reads.

    TMSL is a large and loosely specified document and this reads five fields of it, so
    extra keys are ignored rather than rejected - the alternative is a model that breaks
    on every version of Analysis Services that adds a property. What is validated is that
    the five are the shape they claim to be, once, here at the edge.
    """

    model_config = ConfigDict(frozen=True, extra="ignore", populate_by_name=True)

    name: str = ""
    # TMSL writes a long expression as a list of lines and a short one as a string.
    expression: str | list[str] | None = None
    description: str | list[str] | None = None
    folder: str = Field("", alias="displayFolder")


class BimPartitionSource(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    type: str = ""


class BimPartition(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    source: BimPartitionSource = BimPartitionSource()


class BimTable(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    name: str = ""
    columns: list[dict[str, Any]] = []
    measures: list[BimMeasure] = []
    partitions: list[BimPartition] = []

    def kinds(self) -> set[str]:
        """How the table is filled: `m` for Power Query, `calculated`, `calculationGroup`."""
        return {partition.source.type for partition in self.partitions}


class BimModel(BaseModel):
    """The model object of a .bim, which is where everything in TMSL hangs."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    culture: str = ""
    tables: list[BimTable] = []
    relationships: list[dict[str, Any]] = []
    roles: list[dict[str, Any]] = []
    dataSources: list[dict[str, Any]] = []  # noqa: N815 - TMSL's own spelling


def read(path: Path) -> BimModel:
    """The model, validated once, here at the edge."""
    return BimModel.model_validate(json.loads(path.read_text(encoding="utf-8")).get("model", {}))


@dataclass(frozen=True)
class Coordinate:
    """A cell as the model writes it, before anything is known about whether it exists."""

    template: str
    row: str
    column: str

    def __str__(self) -> str:
        return f"{self.template} r{self.row} c{self.column}"


@dataclass(frozen=True)
class Measure:
    """One measure, with the table it hangs off and the DAX that defines it."""

    table: str
    name: str
    folder: str
    description: str
    expression: str
    coordinates: tuple[Coordinate, ...]
    unpaired: bool


def flat(value: str | list[str] | None) -> str:
    """TMSL writes a long expression as a list of lines and a short one as a string."""
    match value:
        case None:
            return ""
        case list() as lines:
            return "\n".join(str(line) for line in lines)
        case _:
            return str(value)


def coordinates_in(expression: str) -> tuple[tuple[Coordinate, ...], bool]:
    """Every coordinate the expression names, and whether the three lists paired up.

    Pairing is by document order, which is only sound because the three appear the same
    number of times in each measure - measured across 2 131 measures of the model this was
    written for, where 1 284 name exactly one coordinate and the rest name two to twenty,
    always in balanced threes. A measure where they do not balance is reported rather than
    paired on a guess.
    """
    templates, rows, columns = TEMPLATE.findall(expression), ROW.findall(expression), COLUMN.findall(expression)
    if not templates:
        return (), False
    if not len(templates) == len(rows) == len(columns):
        return (), True
    return tuple(
        Coordinate(t.strip(), r.strip(), c.strip()) for t, r, c in zip(templates, rows, columns, strict=True)
    ), False


def measured(table: BimTable, measure: BimMeasure) -> Measure:
    """One measure, with its coordinates already parsed out of the DAX."""
    expression = flat(measure.expression)
    coordinates, unpaired = coordinates_in(expression)
    return Measure(
        table=table.name,
        name=measure.name,
        folder=measure.folder,
        description=flat(measure.description),
        expression=expression,
        coordinates=coordinates,
        unpaired=unpaired,
    )


def measures_of(model: BimModel) -> list[Measure]:
    """Every measure in the model, in the order the file holds them."""
    return [measured(table, measure) for table in model.tables for measure in table.measures]


def as_dpm(code: str) -> str:
    """`C 28.00` is how a human writes what the model calls `C_28.00`."""
    return code.strip().replace(" ", "_")


def template_variants(code: str) -> list[str]:
    """What a template code might be, given what someone typed.

    The variants of a template are `.a`, `.b`, `.w` in the DPM and this model writes them
    `.A`, `.B`, `.W`. That one letter accounted for 476 of 559 coordinates that looked
    withdrawn and were not - which is why the report says how a coordinate matched, and
    not only that it did.
    """
    written = as_dpm(code)
    tried = [written]
    head, dot, tail = written.rpartition(".")
    if dot and tail.isalpha() and tail.lower() != tail:
        tried.append(f"{head}.{tail.lower()}")
    return tried


def variants(code: str) -> list[str]:
    """What a row or column code might be, given what someone typed.

    The DPM is not consistent about width and neither are the people writing DAX against
    it: FINREP rows are `0090`, COREP large exposure columns are `330`, and a model may
    carry either. The first form that resolves is the answer, and which one it was is
    reported - a coordinate that only matches after padding is still a coordinate someone
    wrote differently from the model.
    """
    code = code.strip()
    tried = [code]
    digits = code.lstrip("0") or "0"
    for width in (3, 4):
        padded = digits.rjust(width, "0")
        if padded not in tried:
            tried.append(padded)
    if digits not in tried:
        tried.append(digits)
    return tried


def published(release: str | None) -> dict[tuple[str, str, str], dict[str, Any]]:
    """Every cell of every template in one release, keyed by coordinate.

    One query and a dictionary rather than a lookup per coordinate: a model names upwards
    of a thousand of them, and `lookup_dpm_cell` opens its own connection each time. The
    single-measure view still goes through that lookup, which knows about dimensions and
    validation rules as well.
    """
    cells = gen_wasm_data.lookup("cells")
    with dpm_lookup._connect() as con:  # noqa: SLF001 - the one connection helper the lookups have
        con.execute(
            f"SELECT table_code, row_code, column_code, row_label, column_label, datapoint FROM ({cells.sql})",
            gen_wasm_data.release_parameters(cells, release),
        )
        names = [column[0] for column in con.description or []]
        rows = con.fetchall()
    found = (dict(zip(names, row, strict=True)) for row in rows)
    return {(cell["table_code"], cell["row_code"], cell["column_code"]): cell for cell in found}


@dataclass(frozen=True)
class Resolved:
    """What the DPM says about a coordinate, or that it says nothing."""

    coordinate: Coordinate
    found: dict[str, Any] | None
    matched_as: tuple[str, str, str] | None

    @property
    def exact(self) -> bool:
        """Whether it resolved as written, rather than after padding a code."""
        if not self.matched_as:
            return False
        return self.matched_as == (as_dpm(self.coordinate.template), self.coordinate.row, self.coordinate.column)

    @property
    def how(self) -> str:
        """How it matched, where that differs from what the model wrote."""
        if not self.matched_as or self.exact:
            return ""
        return "/".join(self.matched_as)


# An open table has no row codes: the reporter files one row per exposure, per contract,
# per entity, and the DPM writes the row as `*`. A model still has to name something, and
# this one names `999` - so a literal match fails on a coordinate that is not wrong.
OPEN = "*"


def resolve(coordinate: Coordinate, cells: dict[tuple[str, str, str], dict[str, Any]]) -> Resolved:
    """The coordinate as the DPM has it, trying the forms a human might have written.

    Literal forms first, and only then the open-table form, so that a template with both a
    real row and an open one is never reported as open when the row exists.
    """
    for template in template_variants(coordinate.template):
        for row in [*variants(coordinate.row), OPEN]:
            for column in [*variants(coordinate.column), OPEN]:
                key = (template, row, column)
                if key in cells:
                    return Resolved(coordinate, cells[key], key)
    return Resolved(coordinate, None, None)


def is_open(found: Resolved) -> bool:
    """Whether it only matched because the template's row or column is filed, not fixed."""
    return bool(found.matched_as) and OPEN in found.matched_as


def wording(templates: set[str]) -> dict[tuple[str, str], dict[str, str]]:
    """The regulation's own Swedish for a row, where it has one.

    Read from `source/its_labels.csv` rather than from the DPM, because the DPM is English
    only: the templates are an annex to an Implementing Regulation and a regulation is
    published in every official language. Keyed by (template, row), which is what the
    Journal's grid gives - a column has its own wording but the row is what a measure is
    usually named after.
    """
    labels = Path(__file__).resolve().parent / "source" / "its_labels.csv"
    if not labels.exists():
        return {}
    with labels.open(encoding="utf-8") as handle:
        return {(row["template"], row["row"]): row for row in csv.DictReader(handle) if row["template"] in templates}


def summarise(model: BimModel, found: list[Measure], show_source: bool) -> list[str]:
    """What the model is, before anything is said about what it means."""
    tables = model.tables
    calculated = [table.name for table in tables if "calculated" in table.kinds()]
    groups = [table.name for table in tables if "calculationGroup" in table.kinds()]
    with_coordinates = [measure for measure in found if measure.coordinates]
    distinct = {coordinate for measure in with_coordinates for coordinate in measure.coordinates}
    frameworks: dict[str, int] = {}
    for coordinate in (c for measure in with_coordinates for c in measure.coordinates):
        letter = coordinate.template.strip()[:1].upper()
        frameworks[letter] = frameworks.get(letter, 0) + 1

    lines = [
        f"{len(tables)} tables, {sum(len(table.columns) for table in tables):,} columns, "
        f"{len(found):,} measures, {len(model.relationships):,} relationships",
        f"culture {model.culture or '?'}, roles: {', '.join(role.get('name', '?') for role in model.roles) or 'none'}",
    ]
    if calculated:
        lines.append(f"calculated tables: {', '.join(calculated)}")
    if groups:
        lines.append(f"calculation groups: {', '.join(groups)}")
    if show_source:
        for source in model.dataSources:
            where = source.get("connectionDetails", {}).get("address", {})
            lines.append(
                f"data source {source.get('name', '?')}: {where.get('server', '?')} / {where.get('database', '?')}"
            )
    else:
        # A .bim carries a connection string. Printing where someone's warehouse lives is
        # not something a summary should do without being asked.
        lines.append(f"{len(model.dataSources)} data source(s) - pass --source to print the address")

    lines += [
        "",
        f"{len(with_coordinates):,} of {len(found):,} measures name a DPM coordinate, "
        f"{len(distinct):,} of them distinct",
        "  by framework: " + ", ".join(f"{letter} {count:,}" for letter, count in sorted(frameworks.items())),
    ]
    unpaired = [measure for measure in found if measure.unpaired]
    if unpaired:
        lines.append(f"  {len(unpaired)} measure(s) name a template but not a matching row and column; see --unpaired")
    lists = sum(len(IN_LIST.findall(measure.expression)) for measure in found)
    if lists:
        lines.append(f"  {lists} filter(s) use `IN {{...}}`, which this does not read apart")
    return lines


def elsewhere(coordinate: Coordinate, every: dict[tuple[str, str, str], dict[str, Any]]) -> str:
    """Whether a coordinate the chosen release lacks exists in any release at all.

    The distinction is what makes the missing list worth reading. A coordinate that exists
    in an older release is a template that moved or was withdrawn, and the measure needs
    rewriting against whatever replaced it. One that exists in no release is a typo, or a
    coordinate someone invented, and it has never returned anything.
    """
    found = resolve(coordinate, every)
    if not found.found:
        return "in no release this database carries"
    return f"in an older release: {found.found['row_label']} / {found.found['column_label']}"[:96]


def report(
    resolved: list[Resolved],
    swedish: dict[tuple[str, str], dict[str, str]],
    only_missing: bool,
    every: dict[tuple[str, str, str], dict[str, Any]] | None = None,
) -> list[str]:
    """One line per coordinate, with what the DPM calls it."""
    lines = []
    for item in sorted(resolved, key=lambda r: (r.coordinate.template, r.coordinate.row, r.coordinate.column)):
        if only_missing and item.found:
            continue
        if not item.found:
            lines.append(f"{str(item.coordinate):34} NOT IN THIS RELEASE")
            if every is not None:
                lines.append(f"{'':34} {elsewhere(item.coordinate, every)}")
            continue
        label = f"{item.found['row_label']} / {item.found['column_label']}"
        note = f"  (written {item.coordinate.template}, matched {item.how})" if item.how else ""
        lines.append(f"{str(item.coordinate):34} {label[:76]}{note}")
        says = swedish.get((item.found["table_code"], item.found["row_code"]))
        if says and says.get("sv"):
            lines.append(f"{'':34} sv: {says['sv'][:76]}")
    return lines


def explain_measure(
    measure: Measure, cells: dict[tuple[str, str, str], dict[str, Any]], release: str | None
) -> list[str]:
    """One measure in full: what it computes, and what each cell it names is.

    This is the view that goes through `lookup_dpm_cell`, because for a single coordinate
    the dimensions and the validation rules are worth the extra queries - a measure whose
    cell is checked by a rule that was switched off is a different thing to maintain from
    one whose rule is live.
    """
    lines = [f"{measure.name}   [{measure.table}]"]
    if measure.folder:
        lines.append(f"  folder: {measure.folder}")
    lines += ["", "  " + measure.expression.replace("\n", "\n  "), ""]
    for coordinate in measure.coordinates:
        item = resolve(coordinate, cells)
        if not item.found:
            lines.append(f"  {coordinate} - not in {release or 'any release this database carries'}")
            continue
        label = f"{item.found['row_label'] or '(the filed row)'} / {item.found['column_label']}"
        lines.append(f"  {coordinate} - {label}")
        lines.append(f"      datapoint: {item.found['datapoint']}")
        # Bound rather than reached for twice: the axis that matched as open decides both
        # halves of the sentence, and a type checker cannot see through the helper.
        matched = item.matched_as
        if matched and OPEN in matched:
            axis, wrote = ("rows", coordinate.row) if matched[1] == OPEN else ("columns", coordinate.column)
            lines.append(
                f"      an open table: {matched[0]} has no fixed {axis}, and the DPM writes that axis "
                f"as `*`. The model's {wrote} is its own convention for what the reporter files."
            )
        cell = dpm_lookup.lookup_dpm_cell(item.found["table_code"], item.found["row_code"], item.found["column_code"])
        rules = cell.get("validation_rules") or []
        off = [r for r in rules if not r.get("active", True)]
        if rules:
            lines.append(f"      {len(rules)} validation rule(s) reach it, {len(off)} switched off")
            for rule in rules[:5]:
                state = "" if rule.get("active", True) else "  (switched off)"
                lines.append(f"        {rule.get('rule_code', '?')}  {rule.get('severity', '?')}{state}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bim", type=Path, help="the .bim file to read")
    parser.add_argument("--coordinates", action="store_true", help="every DPM coordinate the measures name, resolved")
    parser.add_argument("--unresolved", action="store_true", help="only the coordinates the DPM does not have")
    parser.add_argument(
        "--unpaired", action="store_true", help="measures naming a template without a matching row and column"
    )
    parser.add_argument("--measure", help="one measure, in full, with its cells resolved")
    parser.add_argument("--release", default=None, help="which DPM release to resolve against, e.g. 4.3")
    parser.add_argument("--source", action="store_true", help="print the data source's address, which a .bim carries")
    parser.add_argument("--csv", action="store_true", help="write the coordinates as CSV instead of text")
    args = parser.parse_args()

    if not args.bim.exists():
        raise SystemExit(f"{args.bim} does not exist")
    model = read(args.bim)
    found = measures_of(model)

    if args.unpaired:
        for measure in (m for m in found if m.unpaired):
            print(f"{measure.name}   [{measure.table}]")
        return

    if not dpm_lookup.available():
        raise SystemExit(dpm_lookup.BUILD_IT)

    if args.measure:
        wanted = [m for m in found if m.name == args.measure]
        if not wanted:
            near = [m.name for m in found if args.measure.lower() in m.name.lower()][:8]
            raise SystemExit(
                f"no measure called {args.measure!r}." + (f" Did you mean: {', '.join(near)}" if near else "")
            )
        cells = published(args.release)
        for measure in wanted:
            print("\n".join(explain_measure(measure, cells, args.release)))
        return

    if args.coordinates or args.unresolved:
        cells = published(args.release)
        distinct = sorted({c for m in found for c in m.coordinates}, key=lambda c: (c.template, c.row, c.column))
        resolved = [resolve(c, cells) for c in distinct]
        if args.csv:
            out = csv.writer(sys.stdout)
            out.writerow(
                ["template", "row", "column", "in_release", "matched_as", "row_label", "column_label", "datapoint"]
            )
            for item in resolved:
                if args.unresolved and item.found:
                    continue
                got = item.found or {}
                out.writerow(
                    [
                        item.coordinate.template,
                        item.coordinate.row,
                        item.coordinate.column,
                        "yes" if item.found else "no",
                        item.how,
                        got.get("row_label", ""),
                        got.get("column_label", ""),
                        got.get("datapoint", ""),
                    ]
                )
            return
        missing = [item for item in resolved if not item.found]
        # Only when something is missing, because it is a second pass over every release.
        every = published(None) if missing else None
        print("\n".join(report(resolved, wording({as_dpm(c.template) for c in distinct}), args.unresolved, every)))
        print(
            f"\n{len(resolved) - len(missing):,} of {len(resolved):,} coordinates are in "
            f"{args.release or 'some release this database carries'}; {len(missing):,} are not."
        )
        return

    print("\n".join(summarise(model, found, args.source)))


if __name__ == "__main__":
    main()
