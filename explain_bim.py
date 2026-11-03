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
    uv run explain_bim.py Model.bim --measure "..." --in-words   # the formula, readable
    uv run explain_bim.py Model.bim --release 4.3        # ask an older release
    uv run explain_bim.py Model.bim --frameworks "COREP FINREP MREL RES"
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
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

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
# A model may name a coordinate in either of two conventions, and the one this was first
# written against uses both: `Dim_C[TabellKod]` on the dimension tables and
# `Fakta_S[Table_code]` on one fact table - 1 565 filters of the first and 418 of the
# second. Reading only the first undercounted the model by a fifth and never looked at the
# S framework at all.
# One filter, whichever convention it is written in and whether it names one value or a
# list. `IN { "0110", "0210" }` is not a shape to guess at: a filter list is a set, and
# three of them in one CALCULATE are the cells of their cross product - four rows by five
# columns is twenty cells, stated exactly, by whoever wrote the measure.
FILTER = re.compile(
    # The table qualifier is part of the match so that replacing a group replaces the
    # whole filter: without it `'Dim_F'` is left standing in front of what replaced it.
    # Quoting is optional in DAX - `Dim_C[TabellKod]` is as valid as `'Dim_C'[TabellKod]`
    # - and a model that writes it the other way read as nothing at all.
    r"(?:'[^']+'|[A-Za-z_]\w*)?\s*"
    r"\[(?P<kind>TabellKod|Table_code|RadKod|Row_code|KolumnKod|Column_code)\]\s*"
    r"(?:=\s*\"(?P<one>[^\"]*)\"|IN\s*\{(?P<many>[^}]*)\})"
)

AXIS = {
    "TabellKod": "template",
    "Table_code": "template",
    "RadKod": "row",
    "Row_code": "row",
    "KolumnKod": "column",
    "Column_code": "column",
}
# `IN { "C 01.00", "C 02.00" }` is a different shape and is counted rather than guessed at.
# Counted for the summary only. The lists themselves are read by `groups`, which is what
# this comment used to deny; what is counted here is how many of them a reader will meet.
IN_LIST = re.compile(r"\[(?:TabellKod|RadKod|KolumnKod|Table_code|Row_code|Column_code)\]\s*IN\s*\{")


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
    # utf-8-sig, because Visual Studio and SSDT write a .bim with a byte order mark and
    # json.loads answers one with "Unexpected UTF-8 BOM" rather than reading it.
    return BimModel.model_validate(json.loads(path.read_text(encoding="utf-8-sig")).get("model", {}))


class UnknownRelease(Exception):
    """A release asked for that this database does not carry.

    Its own type rather than SystemExit: the CLI turns it into a message and the tool
    turns it into an answer, and neither should be a traceback.
    """


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


def chosen(match: re.Match[str]) -> tuple[str, ...]:
    """What one filter selects: one value, or the values of its list."""
    if match["many"] is not None:
        return tuple(value.strip().strip('"') for value in match["many"].split(",") if value.strip())
    return (match["one"].strip(),)


# Between two filters of one group there is a comma and whitespace and nothing else. The
# rule is what stops a template in one CALCULATE pairing with a row in the next: read on
# document order alone, `CALCULATE ( x, [TabellKod] = "C 01.00" )` and the row filter of
# the CALCULATE after it look like one group, and the cell they would make is a cell
# nobody wrote.
# `&&` as well as a comma: `FILTER ( t, a = x && b = y && c = z )` is the same three
# filters standing together, written the way a FILTER() wants them.
BETWEEN = re.compile(r"^[\s,]*$|^\s*&&\s*$")


def groups(expression: str) -> tuple[list[tuple[int, int, dict[str, tuple[str, ...]]]], bool]:
    """Every run of template, row and column filters that stand together.

    Returns where each run begins and ends, what it selects, and whether anything was left
    dangling - a template with no row, two rows in a row, a group broken by other code.
    One reader for both the parsing and the rendering, because two readers of one syntax
    drift apart.
    """
    found: list[tuple[int, int, dict[str, tuple[str, ...]]]] = []
    group: dict[str, tuple[str, ...]] = {}
    begins = 0
    ends = 0
    dangling = False
    for match in FILTER.finditer(expression):
        axis = AXIS[match["kind"]]
        adjacent = bool(group) and bool(BETWEEN.match(expression[ends : match.start()]))
        # Any order within a group. Template, row, column is how the model this was written
        # for writes them, but nothing in DAX requires it, and treating a template as the
        # start of a group threw away every group that began with a row.
        if group and (not adjacent or axis in group):
            dangling = True
            group = {}
        if not group:
            begins = match.start()
        group[axis] = chosen(match)
        ends = match.end()
        if len(group) == 3:
            if "template" in group and "row" in group and "column" in group:
                found.append((begins, ends, group))
            else:
                dangling = True
            group = {}
    return found, dangling or bool(group)


def coordinates_in(expression: str) -> tuple[tuple[Coordinate, ...], bool]:
    """Every coordinate the expression names, and whether anything was left dangling.

    A filter may name one value or a list, and three in one group are the cells of their
    cross product - four rows by five columns is twenty cells. That is what the measure
    says, not an inference about it, which is why the lists are read rather than counted.
    """
    runs, dangling = groups(expression)
    found = [
        Coordinate(template, row, column)
        for _, _, group in runs
        for template in group["template"]
        for row in group["row"]
        for column in group["column"]
    ]
    return tuple(found), dangling


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
        # A release the database does not carry matches no rows, and every coordinate then
        # reads as withdrawn - a whole model apparently obsolete because of a typo. The
        # lookups refuse an unknown release by name; so does this.
        if release:
            carried = [row[0] for row in con.execute(dpm_lookup.RELEASES_IN_FILE_SQL).fetchall()]
            if release not in carried:
                raise UnknownRelease(
                    f"No DPM release {release!r} in this copy of the database. It has: {', '.join(carried)}."
                )
        con.execute(
            "SELECT framework, table_code, row_code, column_code, row_label, column_label, datapoint "
            f"FROM ({cells.sql})",
            gen_wasm_data.release_parameters(cells, release),
        )
        names = [column[0] for column in con.description or []]
        rows = con.fetchall()
    # Every framework a cell is filed under, not whichever row came last. Thirteen
    # templates are in two - C_18.00 is COREP and IF - and keeping one meant that asking
    # for IF refused a cell that exists in IF, on the grounds that it is COREP. That is
    # the guarantee --frameworks was added to give, undone by a dict comprehension.
    cells_by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows:
        cell = dict(zip(names, row, strict=True))
        key = (cell["table_code"], cell["row_code"], cell["column_code"])
        held = cells_by_key.setdefault(key, {**cell, "frameworks": set()})
        held["frameworks"].add(cell.pop("framework"))
    return cells_by_key


def whose(found: dict[str, Any], frameworks: set[str] | None) -> str:
    """Which framework to name for a cell: the one asked for, where that narrows it.

    A template in two frameworks named as both is noise when the caller has already said
    which it means, and the only honest answer when they have not.
    """
    held = set(found.get("frameworks") or ())
    return "/".join(sorted(held & frameworks if frameworks and held & frameworks else held))


@dataclass(frozen=True)
class Resolved:
    """What the DPM says about a coordinate, or that it says nothing."""

    coordinate: Coordinate
    found: dict[str, Any] | None
    matched_as: tuple[str, str, str] | None
    # The framework of a template that matched but was not among those asked for. A code
    # is not unique across frameworks, and "it is PAY and you said COREP and FINREP" is a
    # different answer from "nothing has it".
    refused: str | None = None

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


def resolve(
    coordinate: Coordinate,
    cells: dict[tuple[str, str, str], dict[str, Any]],
    frameworks: set[str] | None = None,
) -> Resolved:
    """The coordinate as the DPM has it, trying the forms a human might have written.

    Literal forms first, and only then the open-table form, so that a template with both a
    real row and an open one is never reported as open when the row exists.

    `frameworks` is which ones the model is written against. A template code is not unique
    across them - this model's `S 01.01` is its own standard report and the DPM's is PAY -
    so a match outside the set is refused and reported as a refusal rather than passed off
    as the answer.
    """
    refused = None
    for template in template_variants(coordinate.template):
        for row in [*variants(coordinate.row), OPEN]:
            for column in [*variants(coordinate.column), OPEN]:
                key = (template, row, column)
                found = cells.get(key)
                if not found:
                    continue
                if frameworks and found["frameworks"].isdisjoint(frameworks):
                    refused = refused or "/".join(sorted(found["frameworks"]))
                    continue
                return Resolved(coordinate, found, key)
    return Resolved(coordinate, None, None, refused)


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


def agrees(journal: str, dpm: str) -> bool:
    """Whether the Official Journal's row and the DPM's row are the same row.

    They are keyed the same way - template and row code - and they do not always agree:
    the Journal's grid for F 05.01 starts at a heading, so its row 0010 is "By product"
    where the DPM's 0010 is "On demand [call] and short notice [current account]". Pairing
    them by code alone put the Swedish for one row against another, which is worse than
    showing no Swedish at all.

    So the Swedish is used only where the Journal's own English matches the DPM's label.
    Case and punctuation are not what is being judged; the wording is.
    """
    plainly = lambda text: re.sub(r"[^\w]+", " ", (text or "").casefold(), flags=re.UNICODE).strip()  # noqa: E731
    return bool(journal) and plainly(journal) == plainly(dpm)


def summarise(model: BimModel, found: list[Measure], show_source: bool) -> list[str]:
    """What the model is, before anything is said about what it means."""
    tables = model.tables
    calculated = [table.name for table in tables if "calculated" in table.kinds()]
    calculation_groups = [table.name for table in tables if "calculationGroup" in table.kinds()]
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
    if calculation_groups:
        lines.append(f"calculation groups: {', '.join(calculation_groups)}")
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
        "  as the model writes them: "
        + ", ".join(f"{letter} {count:,}" for letter, count in sorted(frameworks.items())),
    ]
    unpaired = [measure for measure in found if measure.unpaired]
    if unpaired:
        lines.append(
            f"  {len(unpaired)} measure(s) have filters that do not form a whole "
            "template/row/column group; see --unpaired"
        )
    # Only the lists inside groups that were read: counting the ones in a dangling group
    # as "read as the cells of their cross product" would be a claim about cells nobody got.
    lists = sum(
        len(IN_LIST.findall(measure.expression[begins:ends]))
        for measure in found
        for begins, ends, _ in groups(measure.expression)[0]
    )
    if lists:
        lines.append(f"  {lists} filter(s) name a list, read as the cells of their cross product")
    return lines


def elsewhere(
    coordinate: Coordinate,
    every: dict[tuple[str, str, str], dict[str, Any]],
    frameworks: set[str] | None = None,
) -> str:
    """Whether a coordinate the chosen release lacks exists in any release at all.

    The distinction is what makes the missing list worth reading. A coordinate that exists
    in an older release is a template that moved or was withdrawn, and the measure needs
    rewriting against whatever replaced it. One that exists in no release is a typo, or a
    coordinate someone invented, and it has never returned anything.
    """
    found = resolve(coordinate, every, frameworks)
    if not found.found:
        # Said without the framework it would be a contradiction of the line above it:
        # "not in this release (a PAY template has that code)" followed by what that PAY
        # template says is two answers to one question.
        return "in no release this database carries"
    return f"in an older release: {found.found['row_label']} / {found.found['column_label']}"[:96]


def report(
    resolved: list[Resolved],
    swedish: dict[tuple[str, str], dict[str, str]],
    only_missing: bool,
    every: dict[tuple[str, str, str], dict[str, Any]] | None = None,
    frameworks: set[str] | None = None,
) -> list[str]:
    """One line per coordinate, with what the DPM calls it."""
    lines = []
    for item in sorted(resolved, key=lambda r: (r.coordinate.template, r.coordinate.row, r.coordinate.column)):
        if only_missing and item.found:
            continue
        if not item.found:
            why = f"NOT IN THIS RELEASE{f' (a {item.refused} template has that code)' if item.refused else ''}"
            lines.append(f"{str(item.coordinate):34} {why}")
            if every is not None:
                lines.append(f"{'':34} {elsewhere(item.coordinate, every, frameworks)}")
            continue
        label = f"[{whose(item.found, frameworks)}] {item.found['row_label']} / {item.found['column_label']}"
        note = f"  (written {item.coordinate.template}, matched {item.how})" if item.how else ""
        lines.append(f"{str(item.coordinate):34} {label[:76]}{note}")
        says = swedish.get((item.found["table_code"], item.found["row_code"]))
        if says and says.get("sv") and agrees(says.get("en", ""), item.found["row_label"]):
            lines.append(f"{'':34} sv: {says['sv'][:76]}")
    return lines


def some(values: list[str], most: int = 4) -> str:
    """A list a reader can take in: the first few, and how many were left."""
    shown = " | ".join(values[:most])
    return shown if len(values) <= most else f"{shown} | +{len(values) - most} more"


def in_words(
    expression: str,
    cells: dict[tuple[str, str, str], dict[str, Any]],
    swedish: dict[tuple[str, str], dict[str, str]] | None = None,
    frameworks: set[str] | None = None,
) -> str:
    """The DAX with each group of filters written as the cells it selects.

    The formula is otherwise untouched. Rewriting it into prose would be a second language
    to learn, and it would hide which part of the measure a reader is looking at - what is
    unreadable here is not DAX, it is `r0350 c0010`, so only that is replaced.

    The groups are found the same way `coordinates_in` finds them, because two readers of
    one syntax drift apart: a group that does not come as template, row, column is left
    exactly as written rather than reassembled into something nobody wrote.
    """

    def row_said(coordinate: Coordinate) -> str:
        found = resolve(coordinate, cells, frameworks)
        if not found.found:
            refusal = f" (a {found.refused} template has that code)" if found.refused else ""
            return f"{coordinate.row}?{refusal}"
        says = (swedish or {}).get((found.found["table_code"], found.found["row_code"]), {})
        english = found.found["row_label"]
        if says.get("sv") and agrees(says.get("en", ""), english):
            return says["sv"]
        return english or "the filed row"

    def column_said(coordinate: Coordinate) -> str:
        """The column's own wording, or its code where the DPM does not have the cell."""
        found = resolve(coordinate, cells, frameworks)
        return (found.found or {}).get("column_label") or coordinate.column

    def anchor(group: dict[str, tuple[str, ...]]) -> tuple[Coordinate, Resolved]:
        """The first cell of the product the DPM has, which the labels are read from.

        Reading them from the first cell *written* collapsed a whole group whenever that
        one was missing: `TabellKod IN { "C 02.00", "C 02.00.A" }` is a measure written to
        survive a template being split, and it rendered as "not in this release" because
        the half it was written to outlive is indeed gone.
        """
        for template in group["template"]:
            for row in group["row"]:
                for column in group["column"]:
                    here = Coordinate(template, row, column)
                    found = resolve(here, cells, frameworks)
                    if found.found:
                        return here, found
        written = Coordinate(group["template"][0], group["row"][0], group["column"][0])
        return written, resolve(written, cells, frameworks)

    def group_said(group: dict[str, tuple[str, ...]]) -> str:
        first, found = anchor(group)
        if not found.found:
            refusal = f" (a {found.refused} template has that code)" if found.refused else ""
            return f"«{first} - not in this release{refusal}»"
        whose_framework = whose(found.found, frameworks)
        rows = some([row_said(Coordinate(first.template, row, first.column)) for row in group["row"]])
        columns = some([column_said(Coordinate(first.template, first.row, column)) for column in group["column"]])
        # Each template marked as the rows are, so a group spanning a split says which
        # half is gone rather than hiding it behind the half that is not.
        templates = some(
            [
                template
                if any(
                    resolve(Coordinate(template, row, column), cells, frameworks).found
                    for row in group["row"]
                    for column in group["column"]
                )
                else f"{template}?"
                for template in group["template"]
            ]
        )
        return f"«{templates} ({whose_framework}) · {rows} · {columns}»"

    written: list[str] = []
    last = 0
    for begins, ends, group in groups(expression)[0]:
        written += [expression[last:begins], group_said(group)]
        last = ends
    written.append(expression[last:])
    return "".join(written)


def explain_measure(
    measure: Measure,
    cells: dict[tuple[str, str, str], dict[str, Any]],
    release: str | None,
    plainly: bool = False,
    swedish: dict[tuple[str, str], dict[str, str]] | None = None,
    frameworks: set[str] | None = None,
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
    written = in_words(measure.expression, cells, swedish, frameworks) if plainly else measure.expression
    lines += ["", "  " + written.replace("\n", "\n  "), ""]
    for coordinate in measure.coordinates:
        item = resolve(coordinate, cells, frameworks)
        if not item.found:
            refusal = f" (a {item.refused} template has that code)" if item.refused else ""
            lines.append(f"  {coordinate} - not in {release or 'any release this database carries'}{refusal}")
            continue
        label = f"{item.found['row_label'] or '(the filed row)'} / {item.found['column_label']}"
        lines.append(f"  {coordinate} - [{whose(item.found, frameworks)}] {label}")
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
        # The release goes with it: the rules a cell is under are scoped to a module version,
        # so asking without it answers for the newest module rather than the one being read.
        cell = dpm_lookup.lookup_dpm_cell(
            item.found["table_code"], item.found["row_code"], item.found["column_code"], None, release
        )
        if not cell.get("found"):
            lines.append(f"      no rules read: {cell.get('message', 'the lookup found nothing')}")
            continue
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
    parser.add_argument(
        "--in-words",
        action="store_true",
        help="with --measure: the formula with each coordinate written as the cell it is",
    )
    parser.add_argument("--release", default=None, help="which DPM release to resolve against, e.g. 4.3")
    parser.add_argument(
        "--frameworks",
        default=None,
        help=(
            "which frameworks the model's codes belong to, space separated, e.g. "
            "'COREP FINREP MREL RES'. A template code is not unique across frameworks - "
            "this model's `S 01.01` is its own standard report and the DPM's is PAY - so "
            "without this a code can match a template nobody meant."
        ),
    )
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

    def cells_for(release: str | None) -> dict[tuple[str, str, str], dict[str, Any]]:
        """`published`, with an unknown release as a message rather than a traceback."""
        try:
            return published(release)
        except UnknownRelease as refused:
            raise SystemExit(str(refused)) from refused

    if args.measure:
        wanted = [m for m in found if m.name == args.measure]
        if not wanted:
            near = [m.name for m in found if args.measure.lower() in m.name.lower()][:8]
            raise SystemExit(
                f"no measure called {args.measure!r}." + (f" Did you mean: {', '.join(near)}" if near else "")
            )
        cells = cells_for(args.release)
        for measure in wanted:
            said = wording({as_dpm(c.template) for c in measure.coordinates}) if args.in_words else {}
            print(
                "\n".join(
                    explain_measure(
                        measure,
                        cells,
                        args.release,
                        args.in_words,
                        said,
                        set(args.frameworks.split()) if args.frameworks else None,
                    )
                )
            )
        return

    if args.coordinates or args.unresolved:
        cells = cells_for(args.release)
        distinct = sorted({c for m in found for c in m.coordinates}, key=lambda c: (c.template, c.row, c.column))
        allowed = set(args.frameworks.split()) if args.frameworks else None
        resolved = [resolve(c, cells, allowed) for c in distinct]
        if args.csv:
            out = csv.writer(sys.stdout)
            out.writerow(
                [
                    "template",
                    "row",
                    "column",
                    "in_release",
                    "framework",
                    "matched_as",
                    "row_label",
                    "column_label",
                    "datapoint",
                ]
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
                        whose(got, allowed),
                        item.how,
                        got.get("row_label", ""),
                        got.get("column_label", ""),
                        got.get("datapoint", ""),
                    ]
                )
            return
        missing = [item for item in resolved if not item.found]
        # Only when something is missing, because it is a second pass over every release.
        every = cells_for(None) if missing else None
        print(
            "\n".join(
                report(resolved, wording({as_dpm(c.template) for c in distinct}), args.unresolved, every, allowed)
            )
        )
        print(
            f"\n{len(resolved) - len(missing):,} of {len(resolved):,} coordinates are in "
            f"{args.release or 'some release this database carries'}; {len(missing):,} are not."
        )
        return

    print("\n".join(summarise(model, found, args.source)))


if __name__ == "__main__":
    main()


# --------------------------------------------------------------------------------------
# As a tool an agent can call
# --------------------------------------------------------------------------------------

# Only this one view is offered. "What does this measure mean?" is a question with a
# bounded answer; `--coordinates` over 1 228 of them is a release-time job for a person or
# a pipeline, and its answer is hundreds of lines nobody should spend a context window on.
EXPLAIN_BIM_MEASURE_TOOL_NAME = "explain_bim_measure"

# Where .bim files may be read from. Every other tool in this pack reads a database or an
# API; this one takes a path, and a tool that takes a path is a file reader unless it is
# told where to stop. Set BIM_ROOT to move it.
DEFAULT_BIM_ROOT = "/mnt/y/Dockuments"

EXPLAIN_BIM_MEASURE_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": EXPLAIN_BIM_MEASURE_TOOL_NAME,
        "description": (
            "Explain one measure of an SSAS tabular model (.bim) whose DAX names DPM "
            "coordinates, resolving each to the reporting cell it is: the row and column "
            "labels, the datapoint id, whether the template is open, and whether the "
            "coordinate still exists in the release asked for. Use it when a measure "
            "returns a figure whose provenance is unclear, or when a model needs checking "
            "against a newer DPM release. Reads only; the model's connection string is "
            "never returned."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "bim": {
                    "type": "string",
                    "description": "The .bim file, named relative to the configured model directory.",
                },
                "measure": {"type": "string", "description": "The measure's name, exactly as the model spells it."},
                "frameworks": {
                    "type": ["array", "null"],
                    "items": {"type": "string"},
                    "description": (
                        "Which frameworks the model's codes belong to, e.g. "
                        "['COREP','FINREP']. A template code is not unique across "
                        "frameworks - a model's own S 01.01 matches the EBA's PAY template "
                        "of that code - so without this a coordinate can be answered from "
                        "a template nobody meant."
                    ),
                },
                "release": {
                    "type": ["string", "null"],
                    "description": (
                        "Which DPM release to resolve against, e.g. '4.4'. Null means any release the database carries."
                    ),
                },
            },
            "required": ["bim", "measure"],
            "additionalProperties": False,
        },
    },
}


def model_root() -> Path:
    """Read at call time, not at import, so a host can set it after importing this."""
    return Path(os.environ.get("BIM_ROOT", DEFAULT_BIM_ROOT))


def within_root(name: str) -> Path:
    """The file, if it is a .bim inside the configured directory, and an error if not.

    Resolved before the check, which is the whole point: `../../etc/passwd` and a symlink
    out of the directory both look like a name inside it until the path is resolved.
    """
    root = model_root().resolve()
    wanted = Path(name)
    wanted = (wanted if wanted.is_absolute() else root / wanted).resolve()
    if wanted.suffix.lower() != ".bim":
        raise ValueError(f"{name} is not a .bim file")
    if not wanted.is_relative_to(root):
        raise ValueError(f"{name} is outside {root}")
    return wanted


def explain_bim_measure(
    bim: str,
    measure: str,
    release: str | None = None,
    frameworks: list[str] | None = None,
) -> dict[str, Any]:
    """One measure, with every DPM coordinate in it resolved. The tool behind the name."""
    try:
        path = within_root(bim)
    except ValueError as refused:
        return {"found": False, "message": str(refused)}
    if not path.exists():
        return {"found": False, "message": f"{bim} is not there"}
    if not dpm_lookup.available():
        return {"found": False, "message": dpm_lookup.BUILD_IT}

    try:
        model = read(path)
    except (ValueError, ValidationError) as unreadable:
        return {"found": False, "message": f"{bim} is not a .bim this can read: {unreadable}"}

    wanted = [m for m in measures_of(model) if m.name == measure]
    if not wanted:
        return {"found": False, "measure": measure, "message": f"no measure called {measure!r} in {bim}"}

    try:
        cells = published(release)
    except UnknownRelease as refused:
        return {"found": False, "message": str(refused)}
    asked = set(frameworks) if frameworks else None
    found = wanted[0]
    return {
        "found": True,
        "measure": found.name,
        "table": found.table,
        "folder": found.folder,
        "expression": found.expression,
        "release": release,
        "frameworks": sorted(asked) if asked else None,
        "coordinates": [
            {
                "written": str(item.coordinate),
                "in_release": bool(item.found),
                "matched_as": item.how or None,
                "open_table": is_open(item),
                "frameworks": sorted((item.found or {}).get("frameworks") or ()),
                "refused": item.refused,
                "row_label": (item.found or {}).get("row_label"),
                "column_label": (item.found or {}).get("column_label"),
                "datapoint": (item.found or {}).get("datapoint"),
            }
            for item in (resolve(c, cells, asked) for c in found.coordinates)
        ],
    }
