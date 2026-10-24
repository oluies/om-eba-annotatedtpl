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
from html import unescape
from pathlib import Path
from typing import Any, NamedTuple

import duckdb
import httpx

HERE = Path(__file__).resolve().parent
CACHE = HERE / "its"

# CELLAR speaks ISO 639-2/B three-letter codes, not the two-letter ones everything else
# uses. `sv` is accepted and ignored; `swe` is honoured.
LANGUAGES = {"en": "eng", "sv": "swe", "de": "deu"}

# One Implementing Regulation per framework family. 2021/451 is supervisory reporting -
# COREP, FINREP, large exposures, leverage, liquidity, asset encumbrance.
CELEX = "32021R0451"

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


def aligned(per_language: dict[str, list[Row]]) -> tuple[list[dict[str, str]], dict[str, int]]:
    """The languages joined by position, with English saying which template a row is in.

    By position rather than by (template, row code), which is what this started as. The
    heading that announces a template is typeset slightly differently in each language -
    Swedish finds eleven templates English does not and misses four it has - so attributing
    per language disagrees about which rows belong where, and the join then drops two
    thirds of everything. The documents themselves are parallel: the same number of table
    rows, and the same row code at the same index in 7 766 of 7 768 cases. So English says
    where a row is and the index says what it says in Swedish, and a row whose code is not
    identical across the languages is dropped rather than guessed at.
    """
    english = per_language["en"]
    others = {language: found for language, found in per_language.items() if language != "en"}
    if any(len(found) != len(english) for found in others.values()):
        raise SystemExit(
            "The language versions have different numbers of table rows, so position cannot "
            "align them. Re-fetch with --refresh: this means one cache is of another "
            "consolidation than the rest."
        )
    kept: list[dict[str, str]] = []
    counts = {"rows": len(english), "coded": 0, "misaligned": 0, "untranslated": 0}
    seen: set[tuple[str, str]] = set()
    for row in english:
        if not (row.template and row.code and row.text):
            continue
        counts["coded"] += 1
        theirs = {language: found[row.index] for language, found in others.items()}
        if any(other.code != row.code for other in theirs.values()):
            counts["misaligned"] += 1
            continue
        if any(not other.text for other in theirs.values()):
            counts["untranslated"] += 1
            continue
        if (row.template, row.code) in seen:
            continue
        seen.add((row.template, row.code))
        kept.append(
            {"template": row.template, "row": row.code, "en": row.text}
            | {language: other.text or "" for language, other in theirs.items()}
        )
    return kept, counts


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
    parser.add_argument("--celex", default=CELEX, help=f"the regulation to read. Default {CELEX}.")
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
    parser.add_argument("--report", action="store_true", help="say what was found and what the model makes of it")
    parser.add_argument("--disagreements", type=int, default=10, help="how many to print with --report")
    args = parser.parse_args()

    wanted = [language.strip() for language in args.languages.split(",") if language.strip()]
    unknown = [language for language in wanted if language not in LANGUAGES]
    if unknown:
        raise SystemExit(f"Unknown language(s) {unknown}. Known: {', '.join(LANGUAGES)}.")
    if "en" not in wanted:
        raise SystemExit("English is the join key back into the model; ask for it.")

    per_language = {language: rows(fetch(args.celex, language, args.refresh)) for language in wanted}
    for language, found in per_language.items():
        print(f"{language}: {len(found)} table rows, {sum(1 for row in found if row.code)} carrying a row code")

    labels, counts = aligned(per_language)
    print(
        f"English rows with a template, a code and a label: {counts['coded']}\n"
        f"  dropped, the code differs across languages at that position: {counts['misaligned']}\n"
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
        columns = ["template", "row", *wanted] + (["from"] if args.variants else [])
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
