"""The official translations of the reporting templates, from the Official Journal.

The DPM is English only - its `Translation` and `Language` tables are in the schema and
ship with 0 rows in every release - but the templates themselves are an annex to an EU
Implementing Regulation, and an Implementing Regulation is published in all 24 official
languages. So the Swedish and German row labels exist, they are the legally published
ones, and nothing here has to translate anything.

Where they come from, and why not from EUR-Lex: the EUR-Lex web front end answers a
scripted request with `202 Accepted` and zero bytes. The Publications Office's CELLAR
service answers properly, with the language chosen by content negotiation:

    curl -L -H "Accept: application/xhtml+xml" -H "Accept-Language: swe" \
      http://publications.europa.eu/resource/celex/32021R0451

Each language is about 22 MB of XHTML and the three are structurally identical - 13 838
table rows each, and 7 766 of the 7 768 rows that carry a row code carry the same code at
the same index in all three. This does not rely on that: each language is parsed on its
own and the languages are joined on (template, row code), which the alignment then checks.

    uv run source/fetch_its_labels.py --report      # what was found, and what it matches
    uv run source/fetch_its_labels.py --out source/its_labels.csv

What this is not: a complete answer. The regulation covers COREP, FINREP, large
exposures, leverage, liquidity and asset encumbrance; DORA, MiCA and remuneration are
separate regulations with their own CELEX ids, and the same code reads them by being
given one. And the DPM carries more than any annex does - dimension members, metrics,
module names - which have no official translation at all.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from html import unescape
from pathlib import Path
from typing import Any, NamedTuple

import duckdb
import httpx

HERE = Path(__file__).resolve().parent
CACHE = HERE / "its"
# The row wording, which the FINREP notes are matched against.
REPO_LABELS = HERE / "its_labels.csv"

# CELLAR speaks ISO 639-2/B three-letter codes, not the two-letter ones everything else
# uses. `sv` is accepted and ignored; `swe` is honoured.
LANGUAGES = {"en": "eng", "sv": "swe", "de": "deu"}

# One Implementing Regulation per framework family. 2021/451 is supervisory reporting -
# COREP, FINREP, large exposures, leverage, liquidity, asset encumbrance.
#
# The bare CELEX is the act as *adopted*, and asking for it gets the 2021 text, five years
# behind the DPM releases this is matched against. A consolidated version - 0 prefix, an
# application date suffix - is the act as amended up to that date, and is what anyone
# reading the regulation today reads. The difference is not academic: 2024-09-01 has 381
# coordinates the original does not, 57 rows are worded differently, and agreement with
# the model goes from 93.2% to 94.2%.
CELEX = "32021R0451"

# The consolidations of it, oldest first. Listed rather than discovered at run time: the
# list comes from a SPARQL query against the Publications Office (`consolidations()`
# below reproduces it), and a build that silently followed a new consolidation would
# change published labels without anyone deciding to.
CONSOLIDATIONS = {
    "32021R0451": [
        "02021R0451-20210319",
        "02021R0451-20220303",
        "02021R0451-20230711",
        "02021R0451-20240901",
    ],
}

SPARQL = "http://publications.europa.eu/webapi/rdf/sparql"

CELLAR = "http://publications.europa.eu/resource/celex/{celex}"

# A template announces itself in the annex as `C 01.00 - OWN FUNDS (CA1)`, with the code
# in every language because a code is not translated. The dash is a hyphen in the
# templates and an en dash in the instructions, and both forms appear across languages.
HEADING = re.compile(r"^([A-Z] \d{2}\.\d{2}(?:\.[a-z0-9]+)*) ?[-–—] ?(.+)$")
# COREP heads each template with its code. FINREP does not: Annex III opens with an index
# of TEMPLATE NUMBER / TEMPLATE CODE / NAME and then heads each template with the number
# alone - `1.1 Assets` for F 01.01. The index is read as the document goes past it and a
# numbered heading is resolved against it.
NUMBERED = re.compile(r"^(\d+(?:\.\d+)*)\.? +(\S.*)$")
TEMPLATE_CODE = re.compile(r"^[A-Z] \d{2}\.\d{2}(?:\.[a-z0-9]+)*$")
NUMBER = re.compile(r"^\d+(?:\.\d+)*$")
# Per annex, because the numbers are: 1 is C 01.00 in Annex I and 1.1 is F 01.01 in
# Annex III, so one map shared between them answers the wrong template.
ANNEX = re.compile(r"^ANNEX [IVX]+\b")
ROW_CODE = re.compile(r"0\d{3}")
# A cell that is punctuation, digits and nothing else is a column code or a footnote
# marker, never a label.
NOT_A_LABEL = re.compile(r"[\d\s.,*()\-–]+")


class Row(NamedTuple):
    """One table row of the annexes, as it sits in the document."""

    index: int
    template: str | None
    code: str | None
    text: str | None


def text_of(markup: str) -> str:
    """The text of a fragment, with entities resolved and whitespace flattened."""
    return unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", markup))).strip()


def rows(html: str) -> list[Row]:
    """Every table row, numbered, with the template heading in force above it.

    Paragraphs and rows are read in one pass and in order, because which template a row
    belongs to is not in the row - it is in the last heading before it. Parsing the tables
    alone gives 7 500 rows numbered 0010 upwards with no way to tell one template's 0010
    from another's.
    """
    found: list[Row] = []
    template: str | None = None
    annex = ""
    numbered: dict[str, dict[str, str]] = defaultdict(dict)
    for match in re.finditer(r"<p[^>]*>(.*?)</p>|<tr[^>]*>(.*?)</tr>", html, re.S):
        paragraph, row = match.group(1), match.group(2)
        if paragraph is not None:
            text = text_of(paragraph)
            if ANNEX.match(text):
                annex, template = text.split()[1], None
                continue
            heading = HEADING.match(text)
            if heading:
                # The model spells it F_18.00.a; the Journal spells it F 18.00.a.
                template = heading.group(1).replace(" ", "_")
                continue
            numbering = NUMBERED.match(text)
            if numbering and numbering.group(1) in numbered[annex]:
                template = numbered[annex][numbering.group(1)]
            continue
        cells = [cell for cell in (text_of(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)) if cell]
        # An index row - a template number beside a template code - is the annex's
        # contents page, not a reportable row. Recorded, and not emitted as a label.
        code = next((cell for cell in cells if TEMPLATE_CODE.match(cell)), None)
        number = next((cell for cell in cells if NUMBER.match(cell)), None)
        if code and number:
            numbered[annex].setdefault(number, code.replace(" ", "_"))
            found.append(Row(len(found), template, None, None))
            continue
        codes = [cell for cell in cells if ROW_CODE.fullmatch(cell)]
        words = [cell for cell in cells if len(cell) > 2 and not NOT_A_LABEL.fullmatch(cell)]
        found.append(Row(len(found), template, codes[0] if codes else None, words[0] if words else None))
    return found


# The instructions annex heads a template with its numbering *and* its code -
# `1.2. C 01.00 – OWN FUNDS (CA1)` - which the template annex never does, and which
# HEADING deliberately refuses so that the prose tables are not read as a template's grid.
INSTRUCTION_HEADING = re.compile(r"^[\d.]+\s+([A-Z] \d{2}\.\d{2}(?:\.[a-z0-9]+)*)\s*[-\u2013\u2014]\s*(.+)$")


def instruction_rows(html: str) -> list[Row]:
    """The prose the instructions annex gives each row, numbered over the same stream.

    The same index as `rows()` - a Row per table row of the document, whether or not it
    carries anything - so the languages align by position the way the labels do.

    What a label is to a column heading, this is to a definition: `1. Own funds Point
    (118) of Article 4(1) and Article 72 CRR The own funds of an institution shall be
    ...`, legal reference included. The shape is a two-column table of row code and text,
    which is specific enough that nothing else in the document matches it.
    """
    found: list[Row] = []
    template: str | None = None
    for match in re.finditer(r"<p[^>]*>(.*?)</p>|<tr[^>]*>(.*?)</tr>", html, re.S):
        paragraph, row = match.group(1), match.group(2)
        if paragraph is not None:
            text = text_of(paragraph)
            if ANNEX.match(text):
                template = None
                continue
            heading = INSTRUCTION_HEADING.match(text)
            if heading:
                template = heading.group(1).replace(" ", "_")
            continue
        cells = [cell for cell in (text_of(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)) if cell]
        # Two columns, a row code, and a second cell long enough to be prose. Anything
        # shorter is a heading row or a continuation, not an instruction.
        prose = template and len(cells) == 2 and ROW_CODE.fullmatch(cells[0]) and len(cells[1]) > 20
        found.append(Row(len(found), template, cells[0], cells[1]) if prose else Row(len(found), template, None, None))
    return found


def paired(english: list[Row], other: list[Row]) -> dict[int, Row]:
    """Which row of another language is which row of the English, by row code.

    difflib over the two streams of row codes rather than position-for-position. The
    original 2021 text had the same 13 838 table rows in every language and position was
    exact; the 2024 consolidation does not - German has two rows the others lack - and a
    strict pairing refuses the whole document over two rows in the middle of it.

    A sequence match absorbs that: the two odd rows become an insertion and everything
    either side stays paired. Only blocks matched one to one are kept, so a row paired
    with nothing is dropped rather than shifted onto its neighbour.
    """
    ours = [row.code or "" for row in english]
    theirs = [row.code or "" for row in other]
    pairs: dict[int, Row] = {}
    for block in SequenceMatcher(None, ours, theirs, autojunk=False).get_matching_blocks():
        for step in range(block.size):
            pairs[block.a + step] = other[block.b + step]
    return pairs


def aligned(per_language: dict[str, list[Row]]) -> tuple[list[dict[str, str]], dict[str, int]]:
    """The languages joined, with English saying which template a row is in.

    English attributes, because the heading that announces a template is typeset
    differently in each language: Swedish finds templates English does not and misses
    others, and in the 2024 consolidation German attributes 147 templates where English
    attributes 165. Joining on (template, row code) per language therefore loses coverage
    - 2027 rows against 2499 - which is why the other languages are not asked where a row
    belongs, only what it says.
    """
    english = per_language["en"]
    others = {language: paired(english, found) for language, found in per_language.items() if language != "en"}
    kept: list[dict[str, str]] = []
    counts = {"rows": len(english), "coded": 0, "unpaired": 0, "untranslated": 0}
    seen: set[tuple[str, str]] = set()
    for row in english:
        if not (row.template and row.code and row.text):
            continue
        counts["coded"] += 1
        theirs = {language: pairs.get(row.index) for language, pairs in others.items()}
        if any(other is None or other.code != row.code for other in theirs.values()):
            counts["unpaired"] += 1
            continue
        if any(not other.text for other in theirs.values() if other):
            counts["untranslated"] += 1
            continue
        if (row.template, row.code) in seen:
            continue
        seen.add((row.template, row.code))
        kept.append(
            {"template": row.template, "row": row.code, "en": row.text}
            | {language: (other.text or "") for language, other in theirs.items() if other}
        )
    return kept, counts


def consolidations(celex: str) -> list[str]:
    """Every consolidated version of an act, oldest last, asked of the Publications Office.

    Not called by the build - CONSOLIDATIONS is what it uses, so that a new consolidation
    appearing upstream cannot change published labels on its own. This is how that list is
    refreshed, deliberately, when someone looks.
    """
    query = (
        "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> "
        "SELECT ?celex WHERE { ?w cdm:resource_legal_id_celex ?celex . "
        f"FILTER(STRSTARTS(STR(?celex), '0{celex[1:]}')) }} ORDER BY ?celex"
    )
    response = httpx.get(
        SPARQL,
        params={"query": query, "format": "application/sparql-results+json"},
        follow_redirects=True,
        timeout=120.0,
    )
    response.raise_for_status()
    return [row["celex"]["value"] for row in response.json()["results"]["bindings"]]


def newest(celex: str) -> str:
    """The consolidated version to read, or the act itself when it has none."""
    found = CONSOLIDATIONS.get(celex)
    return found[-1] if found else celex


def fetch(celex: str, language: str, refresh: bool = False) -> str:
    """One language version of a regulation, cached on disk.

    22 MB a language and the Official Journal does not change under us - a regulation is
    amended by another regulation with its own CELEX id, never edited in place - so the
    cache has no expiry and `--refresh` is for when a new consolidation is wanted.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    here = CACHE / f"{celex}.{language}.html"
    if here.exists() and not refresh:
        return here.read_text(encoding="utf-8", errors="replace")
    url = CELLAR.format(celex=celex)
    print(f"fetching {celex} in {language} ...", file=sys.stderr)
    response = httpx.get(
        url,
        headers={"Accept": "application/xhtml+xml", "Accept-Language": LANGUAGES[language]},
        follow_redirects=True,
        timeout=180.0,
    )
    response.raise_for_status()
    here.write_text(response.text, encoding="utf-8")
    return response.text


# --------------------------------------------------------------------------------------
# What the model makes of them
# --------------------------------------------------------------------------------------

DPM_ROWS = """
SELECT   tv.Code                  AS template,
         hv.Code                  AS row_code,
         trim(hv.Label)           AS label
FROM     TableVersion tv
JOIN     TableVersionHeader th ON th.TableVID = tv.TableVID
JOIN     HeaderVersion hv ON hv.HeaderVID = th.HeaderVID
JOIN     Header h ON h.HeaderID = th.HeaderID
WHERE    h.Direction = 'Y'  -- Y is the vertical axis: rows. X is columns, Z sheets.
     AND tv.EndReleaseID IS NULL
     AND hv.Code IS NOT NULL
"""


def normal(text: str) -> str:
    """For comparing a label the Journal typeset against one the DPM stores.

    Not for display and not for matching in anger: it exists to answer "is this the same
    row", where the two differ by a numbering prefix, a dash that is an en dash in one and
    a hyphen in the other, and case.
    """
    without_number = re.sub(r"^[\d.\s]*", "", text)
    flattened = re.sub(r"[‐-―]", "-", without_number)
    return re.sub(r"[^a-z0-9]+", " ", flattened.lower()).strip()


def model_rows(con: duckdb.DuckDBPyConnection) -> dict[tuple[str, str], str]:
    """The row labels the model has, for the version of each template in force."""
    cursor = con.execute(DPM_ROWS)
    return {(template, row): label for template, row, label in cursor.fetchall()}


# A template and its variants: C_75.01.a and C_75.01.w are C_75.01 reported under another
# scope, with the same grid. The Journal prints the grid once, under the stem.
#
# A letter, not [a-z0-9]: F 04.02.1 and F 04.02.2 are separate templates with their own
# codes in the Journal's own index, not variants of an F 04.02. Treating a numeric suffix
# as a variant would hand them a grid they do not have - and would do it silently, since
# there is usually no F 04.02 published to take it from.
STEM = re.compile(r"^([A-Z]_\d{2}\.\d{2})\.[a-z]+$")


def stem_of(template: str) -> str | None:
    """The template a variant is a variant of, or None if it is not one."""
    found = STEM.match(template)
    return found.group(1) if found else None


def worded_differently(celex: str, languages: list[str]) -> list[dict[str, str]]:
    """Rows the consolidations of an act word differently, one entry per wording.

    Not a version selector, which is what this started as. The four consolidations of
    2021/451 are two distinct texts, and they differ in 58 of 4273 coordinates across 16
    of 165 templates - so a control offering a choice would show the same thing on 149
    pages out of 165, which teaches a reader that the choice does not matter anywhere.
    The 16 templates where it does are told, on the rows where it does.
    """
    per_version = {}
    for version in CONSOLIDATIONS.get(celex, [celex]):
        here = {language: rows(fetch(version, language)) for language in languages}
        labels, _ = aligned(here)
        per_version[version] = {(row["template"], row["row"]): row for row in labels}

    everywhere = set().union(*(set(found) for found in per_version.values()))
    changed = []
    for key in sorted(everywhere):
        wordings = []
        for version, found in per_version.items():
            row = found.get(key)
            if row and (not wordings or wordings[-1][1]["en"] != row["en"]):
                wordings.append((version, row))
        if len(wordings) > 1:
            changed.extend(
                {"template": key[0], "row": key[1], "celex": version} | {k: v for k, v in row.items() if k in languages}
                for version, row in wordings
            )
    return changed


# FINREP's instructions annex is not COREP's. COREP gives a two-column table of row code
# and prose; Annex V gives numbered paragraphs of narrative guidance, and names the item
# it is about by quoting its label rather than by its code:
#
#   1. 'Cash on hand' shall include holdings of national and foreign banknotes…
#
# So the key is the label, matched inside one template. The yield is small and that is a
# property of the annex, not of this: 708 numbered paragraphs in Part 2, 246 quoting an
# item at all, and 65 whose quoted term is a row of the template they sit under. The
# other 643 are guidance about accounting treatment, which belongs to no row.
FINREP_HEADING = re.compile(r"^(\d+(?:\.\d+)*)\.\s+(.+?)\s*\((\d+(?:\.\d+)*)\)$")
NUMBERED_PARAGRAPH = re.compile(r"^(\d+)\.\s")
QUOTED_ITEM = re.compile(r"[\u2018']([^\u2019']{4,90})[\u2019']")


def paragraphs(html: str) -> list[tuple[str, str, str]]:
    """Part 2's numbered paragraphs, each with the template number it sits under.

    In document order, each with its own number and the template heading above it.

    The numbers are not unique: they restart, so `1.` occurs many times and keying on it
    pairs an English paragraph about cash on hand with a Swedish one about exposure
    classes - which is the one thing this must not do, because the result reads as a
    translation. They are aligned as a sequence instead, the way the row codes are.

    Anchored on the heading shape and not on "PART 2: TEMPLATE RELATED INSTRUCTIONS",
    which is English and found nothing in the other two. `1.1. Assets (1.1)` is
    `1.1. Tillgångar (1.1)` in Swedish, and the number in the brackets is the same in
    every language because a template number is not translated.
    """
    found: list[tuple[str, str, str]] = []
    template = ""
    for match in re.finditer(r"<p[^>]*>(.*?)</p>", html, re.S):
        text = text_of(match.group(1))
        heading = FINREP_HEADING.match(text)
        if heading:
            template = heading.group(3)
            continue
        own = NUMBERED_PARAGRAPH.match(text)
        if template and own and len(text) > 40:
            found.append((own.group(1), template, text))
    return found


def finrep_notes(
    per_language: dict[str, str],
    labels: dict[tuple[str, str], str],
    numbers: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    """Paragraphs of Annex V attached to the row they quote, in every language.

    `labels` is the row wording already collected, keyed on (template, row) and normalised
    - the match is an exact one inside a single template, because a near match here would
    hang an official definition on the wrong row, which is worse than having none.
    """
    english = paragraphs(per_language["en"])
    others = {}
    for language, html in per_language.items():
        if language == "en":
            continue
        theirs = paragraphs(html)
        pairs: dict[int, str] = {}
        matcher = SequenceMatcher(None, [n for n, _, _ in english], [n for n, _, _ in theirs], autojunk=False)
        for block in matcher.get_matching_blocks():
            for step in range(block.size):
                pairs[block.a + step] = theirs[block.b + step][2]
        others[language] = pairs
    # Injectable so the matching can be tested without an annex index to parse.
    numbers = numbers if numbers is not None else template_numbers(per_language["en"])
    by_label: dict[str, dict[str, str]] = {}
    for (template, row), text in labels.items():
        by_label.setdefault(template, {}).setdefault(normal(text), row)

    notes = []
    seen: set[tuple[str, str]] = set()
    for index, (_, number, text) in enumerate(english):
        template = numbers.get(number)
        if not template or template not in by_label:
            continue
        # A paragraph that pairs with nothing is dropped rather than carried with the
        # English in its place, which would read as a translation and is not.
        theirs = {language: pairs.get(index, "") for language, pairs in others.items()}
        if any(not other for other in theirs.values()):
            continue
        for term in QUOTED_ITEM.findall(text):
            row = by_label[template].get(normal(term))
            if not row or (template, row) in seen:
                continue
            seen.add((template, row))
            notes.append(
                {"template": template, "row": row, "en": text}
                | {language: other or "" for language, other in theirs.items()}
            )
            break
    return notes


def template_numbers(html: str) -> dict[str, str]:
    """The annex index, as number to code: 1.1 is F 01.01."""
    numbers: dict[str, str] = {}
    annex = ""
    for match in re.finditer(r"<p[^>]*>(.*?)</p>|<tr[^>]*>(.*?)</tr>", html, re.S):
        paragraph, row = match.group(1), match.group(2)
        if paragraph is not None:
            text = text_of(paragraph)
            if ANNEX.match(text):
                annex = text.split()[1]
            continue
        if annex not in ("III", "IV"):
            continue
        cells = [cell for cell in (text_of(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)) if cell]
        code = next((cell for cell in cells if TEMPLATE_CODE.match(cell)), None)
        number = next((cell for cell in cells if NUMBER.match(cell)), None)
        if code and number:
            numbers.setdefault(number, code.replace(" ", "_"))
    return numbers


def database_path() -> Path:
    """The DPM database, from the environment or where fetch_dpm2.py puts it."""
    database = Path(os.environ.get("DPM2_DB") or HERE / "dpm2" / "dpm2.duckdb")
    if not database.exists():
        raise SystemExit(f"{database} is not there; source/fetch_dpm2.py builds it.")
    return database


def model_keys(database: Path) -> set[tuple[str, str]]:
    """Every (template, row) the model has, which is what variants are expanded against."""
    with duckdb.connect(str(database), read_only=True) as con:
        return set(model_rows(con))


def report(labels: list[dict[str, str]], model: dict[tuple[str, str], str]) -> dict[str, Any]:
    """How much of the model these labels reach, and how well they agree.

    Two numbers, and the second matters more. `covered` is how many of the model's rows
    have a published translation at the same coordinate - the ceiling on what this can
    deliver. `agreeing` is how many of those have an English text that matches the model's
    own: where they disagree, the coordinate is the same but the row may not be, and a
    translation hung on it would be wrong rather than missing.
    """
    published = {(row["template"], row["row"]): row for row in labels}
    hits = {key: value for key, value in published.items() if key in model}
    agreeing = {key: value for key, value in hits.items() if normal(value["en"]) == normal(model[key])}
    by_template: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for key in model:
        by_template[key[0]][0] += 1
    for key in hits:
        by_template[key[0]][1] += 1
    for key in agreeing:
        by_template[key[0]][2] += 1
    # The templates these labels actually reach, as against every template in force. The
    # difference between the two is the parser's reach, not the Journal's: within a
    # template it has found, almost every row is there.
    reached = {key[0] for key in published}
    in_reach = {key for key in model if key[0] in reached}
    # What a stem fallback would add, measured rather than assumed: a variant row that
    # has no published label of its own, whose stem has one at the same row code. The
    # agreement rate on those is the test - if the variant is not the same grid after
    # all, its English text will not match the stem's.
    variants = {
        key: published[(stem_of(key[0]) or "", key[1])]
        for key in model
        if key not in published and (stem_of(key[0]) or "", key[1]) in published
    }
    variants_agreeing = {key for key, value in variants.items() if normal(value["en"]) == normal(model[key])}
    return {
        "published_rows": len(published),
        "model_rows": len(model),
        "covered": len(hits),
        "agreeing": len(agreeing),
        "reached_templates": len(reached),
        "rows_in_reach": len(in_reach),
        "covered_in_reach": len(in_reach & set(hits)),
        "by_variant": len(variants),
        "by_variant_agreeing": len(variants_agreeing),
        "templates": {
            template: {"model": counts[0], "covered": counts[1], "agreeing": counts[2]}
            for template, counts in sorted(by_template.items())
            if counts[1]
        },
        "disagreements": [
            {"template": key[0], "row": key[1], "journal": value["en"][:70], "model": model[key][:70]}
            for key, value in sorted(hits.items())
            if key not in agreeing
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--celex",
        default="",
        help="the version of the regulation to read - a consolidated id such as "
        f"02021R0451-20230711, or {CELEX} for the act as adopted. Default: the newest "
        f"consolidation of {CELEX}, which is {newest(CELEX)}.",
    )
    parser.add_argument(
        "--versions",
        action="store_true",
        help="list the consolidated versions known for the regulation and stop.",
    )
    parser.add_argument(
        "--changed",
        action="store_true",
        help="collect the rows the consolidations word differently, one entry per wording, "
        "instead of the labels. Small: 58 coordinates over 16 templates.",
    )
    parser.add_argument(
        "--languages",
        default="en,sv,de",
        help="comma separated, English required. Default en,sv,de.",
    )
    parser.add_argument("--refresh", action="store_true", help="fetch again rather than use the cache")
    parser.add_argument("--out", type=Path, help="write the aligned labels here as CSV")
    parser.add_argument(
        "--variants",
        action="store_true",
        help="also give a variant template the grid of the template it varies - C_75.01.a "
        "from C_75.01 - which the Journal prints once. Needs the DPM, to know which "
        "variants exist. Every row says which it is in the `from` column.",
    )
    parser.add_argument(
        "--instructions",
        action="store_true",
        help="collect the instructions annex's prose per row instead of the labels - what a "
        "row means and which article requires it, rather than what it is called.",
    )
    parser.add_argument("--report", action="store_true", help="say what was found and what the model makes of it")
    parser.add_argument("--disagreements", type=int, default=10, help="how many to print with --report")
    args = parser.parse_args()

    if args.versions:
        for version in CONSOLIDATIONS.get(args.celex or CELEX, []):
            print(version)
        return
    args.celex = args.celex or newest(CELEX)

    wanted = [language.strip() for language in args.languages.split(",") if language.strip()]
    unknown = [language for language in wanted if language not in LANGUAGES]
    if unknown:
        raise SystemExit(f"Unknown language(s) {unknown}. Known: {', '.join(LANGUAGES)}.")
    if "en" not in wanted:
        raise SystemExit("English is the join key back into the model; ask for it.")

    if args.changed:
        changed = worded_differently(CELEX, wanted)
        print(f"{len(changed)} wordings over {len({row['template'] for row in changed})} templates")
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with args.out.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["template", "row", "celex", *wanted])
                writer.writeheader()
                writer.writerows(changed)
            print(f"wrote {args.out}")
        return

    if args.instructions:
        # COREP's tables, then FINREP's narrative, into one file with a `shape` saying
        # which it is - because they are not the same kind of thing and a reader of the
        # file should not have to guess.
        pages = {language: fetch(args.celex, language, args.refresh) for language in wanted}
        per_language = {language: instruction_rows(html) for language, html in pages.items()}
        from_tables, counts = aligned(per_language)
        wording = {}
        for row in csv.DictReader((REPO_LABELS.read_text(encoding="utf-8")).splitlines()):
            wording[(row["template"], row["row"])] = row["en"]
        notes = finrep_notes(pages, wording)
        labels = [row | {"shape": "table"} for row in from_tables] + [row | {"shape": "note"} for row in notes]
        print(
            f"from COREP's instruction tables: {len(from_tables)}\nfrom FINREP's Annex V, quoting a row: {len(notes)}"
        )
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with args.out.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["template", "row", *wanted, "celex", "shape"])
                writer.writeheader()
                writer.writerows(
                    sorted(
                        ({**row, "celex": args.celex} for row in labels),
                        key=lambda row: (row["template"], row["row"]),
                    )
                )
            print(f"wrote {args.out}")
        return

    read = rows
    per_language = {language: read(fetch(args.celex, language, args.refresh)) for language in wanted}
    for language, found in per_language.items():
        print(f"{language}: {len(found)} table rows, {sum(1 for row in found if row.code)} carrying a row code")

    labels, counts = aligned(per_language)
    print(
        f"English rows with a template, a code and a label: {counts['coded']}\n"
        f"  dropped, no row with that code lines up in every language: {counts['unpaired']}\n"
        f"  dropped, one language has no text there: {counts['untranslated']}\n"
        f"aligned across {', '.join(wanted)}: {len(labels)} distinct coordinates"
    )

    if args.variants:
        published = {(row["template"], row["row"]): row for row in labels}
        added = [
            published[(stem_of(key[0]) or "", key[1])] | {"template": key[0], "from": "stem"}
            for key in model_keys(database_path())
            if key not in published and (stem_of(key[0]) or "", key[1]) in published
        ]
        labels = [row | {"from": "journal"} for row in labels] + added
        print(f"with variants: {len(labels)} rows, {len(added)} of them from a stem")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        labels = [row | {"celex": args.celex} for row in labels]
        columns = ["template", "row", *wanted, "celex"] + (["from"] if args.variants else [])
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(sorted(labels, key=lambda row: (row["template"], row["row"])))
        print(f"wrote {args.out}")

    if args.report:
        with duckdb.connect(str(database_path()), read_only=True) as con:
            model = model_rows(con)
        found = report(labels, model)
        print(
            f"\nthe model has {found['model_rows']} row labels in the templates in force.\n"
            f"  {found['covered']} of them have a published translation at the same coordinate "
            f"({100 * found['covered'] / max(found['model_rows'], 1):.1f}%)\n"
            f"  {found['agreeing']} of those also agree on the English text "
            f"({100 * found['agreeing'] / max(found['covered'], 1):.1f}% of what is covered)\n"
            f"\nwithin the {found['reached_templates']} templates these labels reach, the model has "
            f"{found['rows_in_reach']} rows and {found['covered_in_reach']} are covered "
            f"({100 * found['covered_in_reach'] / max(found['rows_in_reach'], 1):.1f}%).\n"
            "The gap between that and the figure above is reach, not the Journal: a template the "
            "parser finds is a template it reads almost completely."
        )
        print(
            f"\na stem fallback - a variant taking its grid from the template it varies, "
            f"C_75.01.a from C_75.01 - would add {found['by_variant']} rows, of which "
            f"{found['by_variant_agreeing']} agree with the model's English "
            f"({100 * found['by_variant_agreeing'] / max(found['by_variant'], 1):.1f}%). "
            "That rate is the test of whether a variant really is the same grid."
        )
        print("\nby template, best first:")
        ranked = sorted(found["templates"].items(), key=lambda item: -item[1]["agreeing"])
        for template, counts in ranked[:12]:
            print(
                f"  {template:<12} {counts['agreeing']:>4} agreeing of {counts['covered']:>4} covered, "
                f"model has {counts['model']}"
            )
        if found["disagreements"]:
            print(f"\n{len(found['disagreements'])} coordinates where the texts differ. First {args.disagreements}:")
            for row in found["disagreements"][: args.disagreements]:
                print(f"  {row['template']} r{row['row']}\n    journal: {row['journal']}\n    model:   {row['model']}")


if __name__ == "__main__":
    main()
