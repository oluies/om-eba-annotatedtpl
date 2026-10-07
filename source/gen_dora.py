"""Generate the DORA pages from the DPM export.

DORA is shaped differently from PAY and the pages have to say so. Its register of
information mostly has **open rows** - one row per entity, contract or provider - so
there is no row/column grid to look a datapoint up in. The DPM writes those cells as
`{B_01.01, r*, c0020}`, an asterisk where PAY has `r0010`.

That means a DORA column resolves on template and column alone: 85 cells, 85 distinct
ids, 85 distinct (template, column) pairs. The row number in a warehouse column name is
a record ordinal, not a framework code.

Reads source/dpm-dora-1.1.0-datapoints.csv, which comes from the EBA DPM 2.0 database,
module DORA 1.1.0. Run after gen_pack.py.
"""

import csv
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO / "source"
DATA = SOURCE_DIR / "dpm-dora-1.1.0-datapoints.csv"
VOCAB = SOURCE_DIR / "dpm-dora-1.1.0-vocabulary.csv"
OUT = REPO / "dora"

# Where the DPM database this pack is built from is published. Cited everywhere a reader
# might otherwise take this pack as the authority.
DICTIONARY_URL = "https://www.eba.europa.eu/risk-and-data-analysis/reporting/dpm-data-dictionary"
SOURCE = f"EBA DPM 2.0 database, module DORA 1.1.0, from the EBA DPM Data Dictionary, {DICTIONARY_URL}"
# No dot in the glossary NAME: OpenMetadata quotes FQN parts that contain one.
GLOSSARY = "DORA_1_1_0"
AUTHORITY = "the DORA Implementing Technical Standards on the register of information"

# Every term here is derived from the EBA Data Point Model, so every term carries a
# reference to the dictionary it came from. The CSV format for this column is
# name;url, repeated - so a comma in either would break the row, and neither has one.
DPM_DICTIONARY = (
    "EBA DPM Data Dictionary;https://www.eba.europa.eu/risk-and-data-analysis/reporting/dpm-data-dictionary"
)

# The warehouse writes an open row as r999. The DPM writes it as r*. Same thing.
OPEN_ROW_PLACEHOLDER = "999"

# For the comparison in the overview; PAY is the framework this pack started with.
PAY_DATAPOINTS = 1830


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    def esc(cell: object) -> str:
        return str(cell).replace("|", "\\|").replace("\n", " ")

    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


rows = list(csv.DictReader(DATA.open(encoding="utf-8")))
by_template: dict[str, list[dict[str, str]]] = defaultdict(list)
for row in rows:
    by_template[row["template"]].append(row)

vocab = list(csv.DictReader(VOCAB.open(encoding="utf-8")))
PROPERTIES = {v["name"]: v for v in vocab if v["kind"] == "property" and v["name"]}
MEMBERS_BY_DOMAIN: dict[str, dict[str, str]] = defaultdict(dict)
for v in vocab:
    if v["kind"] == "member" and v["name"]:
        MEMBERS_BY_DOMAIN[v["domain"] or "Uncategorised"][v["name"]] = v["extra"]

COLUMNS_USING: dict[str, list[str]] = defaultdict(list)
for v in vocab:
    if v["name"]:
        COLUMNS_USING[v["name"]].append(f"{v['template']} c{v['column_code']}")

OPEN = [r for r in rows if r["row_kind"] == "open"]
FIXED = [r for r in rows if r["row_kind"] == "fixed"]


def write_overview() -> None:
    table = md_table(
        ["Template", "Table", "Subject", "Rows", "Datapoints"],
        [
            [f"`{code}`", f"`{rs[0]['table_name']}`", rs[0]["template_name"], rs[0]["row_kind"], str(len(rs))]
            for code, rs in sorted(by_template.items())
        ],
    )
    write(
        OUT / "01-framework.md",
        f"""# DORA — register of information

The register of information under the Digital Operational Resilience Act: which entities
report, which contractual arrangements they hold with ICT third-party service providers,
which functions those services support, and how the arrangements are assessed.

**{len(rows)} datapoints across {len(by_template)} templates.** Transcribed from {SOURCE}.

**Definitions.** The labels here are the framework's own wording, not a legal definition.
Where a precise definition is needed, cite {AUTHORITY} rather than paraphrasing this file.

## How this differs from PAY 4.2

PAY reports fixed grids: a known row, a known column, {PAY_DATAPOINTS:,} datapoints. DORA mostly
does not. {len(OPEN)} of its {len(rows)} datapoints sit on **open rows** - the register holds one row
per entity, contract or provider, and the count is whatever the reporter has.

The DPM writes an open row as `r*`. A warehouse writes it as a record ordinal, commonly
`r{OPEN_ROW_PLACEHOLDER}`. Neither is a framework row code, and neither narrows the datapoint.

`B_99.01` carries a fixed row code, `0040`, instead of `r*`. It makes no difference to a
lookup: every DORA template has exactly one row, and its datapoints differ by column.

So for DORA the column carries the meaning and the row carries the record. That changes
the lookup, and `02-agent-instructions.md` says how.

## Templates

{table}
""",
    )


def write_agent_instructions() -> None:
    example = next(r for r in rows if r["template"] == "B_01.01" and r["column_code"] == "0020")
    write(
        OUT / "02-agent-instructions.md",
        f"""# How to describe DORA assets in OpenMetadata

Instructions for an agent writing table and column descriptions for assets derived from
the DORA register of information. Read this instead of the PAY 4.2 instructions when the
table is a `B_*` one - the lookup rule is different.

## The column name

```text
{example["column_name_pattern"].replace("*", OPEN_ROW_PLACEHOLDER)}
```

splits the same way as a PAY column, with the same pattern:

```text
^(?P<prefix>[A-Za-z]{{1,}})(?P<major>[0-9]{{2}})(?P<minor>[0-9]{{2}})_r(?P<row>[0-9]{{1,}})_c(?P<col>[0-9]{{4}})$
```

Note `row` is `[0-9]{{1,}}` here, not four digits: an open row is written as a record
ordinal such as `{OPEN_ROW_PLACEHOLDER}`, which is three.

| Form | Example | Shape |
|---|---|---|
| Column prefix | `{example["column_name_pattern"].split("_")[0]}` | prefix, major, minor, no separator |
| Template code | `{example["template"]}` | underscore, then dot |
| Table name | `{example["table_name"]}` | underscore, then underscore |

## The row does not narrow anything

**Ignore the row number when resolving a DORA column.** {len(OPEN)} of the {len(rows)} datapoints sit
on open rows: the register holds one row per entity, contract or provider, and the DPM
writes that as `r*`. A warehouse writes an ordinal instead - `r{OPEN_ROW_PLACEHOLDER}` or a running number - and
it identifies the record, not the framework cell.

Template and column identify the datapoint on their own. Verified against the DPM: {len(rows)}
cells, {len(rows)} distinct ids, {len(rows)} distinct template-and-column pairs.

`B_99.01` looks like an exception - the DPM gives it a fixed row code `0040` rather than
`r*` - but it is not one in practice: all {len(FIXED)} of its datapoints sit on that single
row and differ by column. So the rule holds for every DORA template without exception.

## Describing a column

State what the column holds, name the template it belongs to, and cite the datapoint id.
There are no variants in DORA, so unlike PAY there is nothing being withheld:

```text
{example["column_label"]}, column {example["column_code"]} of template {example["template"]}
({example["template_name"]}) in the DORA register of information. Datapoint
{example["datapoint_id"]} (EBA DPM, module DORA 1.1.0). One row per record; the row
number in the column name is an ordinal, not a framework code.
```

## Use the tool if it is there

`lookup_datapoint` covers DORA and decides which rule applies on its own - pass the
column name and nothing else. `variant` is a PAY argument and has no meaning here.

```text
lookup_datapoint("B0101_r999_c0020")
  template B_01.01, column 0020, "Name of the entity", datapoint 3287126
```

## Validation rules

The answer carries `validation_rules`: the EBA rules that reach the cell, with severity
and the DPM-XL expression. DORA has 71 of them across 11 templates, and they are the
reason a column such as `B0202_r*_c0080` is not free text - several say it must be
present whenever certain other columns are.

Name the codes in the description and leave the expressions out:

> ... Datapoint 3296069 (EBA DPM, module DORA 1.1.0). Validation rules (EBA DPM,
> warning): e23680_e, v8869_m, v8870_m.

Do not paraphrase an expression into English. It is a new claim about what the framework
requires, and the code is what the EBA's published rule lists are indexed by.

`B_99.01` has no validation rules at all, so its columns name none. That is the model's
answer, not a gap in this pack.

## Display names

Set one for the table and for every column, and use the one `lookup_datapoint` returns:
`display_name` for the column, `table_display_name` for the table.

DORA is the easy case. The rows are records, so a row label would say nothing, and the
column label is the whole of the name:

```text
B_01_01            ->  B 01.01 Entity maintaining the register of information
B0101_r999_c0020   ->  Name of the entity
```

No row code, no ordinal, no datapoint id. The codes are in the column name right next to
it, and the ordinal is not a framework code at all.

## The rest is the same as PAY

Everything in the PAY 4.2 instructions about *how* to write applies here too, and is not
repeated: do not create tables or columns, do not patch columns by index, write a column
by name through its own entity, confirm before replacing what a person wrote, and leave
warehouse context columns alone.
""",
    )


def write_glossary() -> None:
    """The vocabulary behind DORA's columns.

    Two kinds. A **property** is what a column holds and what type it is - the column's
    own concept, of which there are 50 across the 85 columns. A **member** is a value on
    a dimension, which only the 37 columns that carry a dimensional context have.

    PAY's glossary is the other way round: few properties, many members. DORA describes
    entities and contracts rather than measuring them, so most of its meaning sits in
    what the column *is* rather than in how it is broken down.
    """
    prop_rows = [
        [name, v["extra"] or "—", str(len(COLUMNS_USING[name])), ", ".join(sorted(set(COLUMNS_USING[name]))[:3])]
        for name, v in sorted(PROPERTIES.items())
    ]
    domain_sections = []
    for domain, members in sorted(MEMBERS_BY_DOMAIN.items()):
        table = md_table(
            ["Member", "Description", "Columns"],
            [
                [name, (desc or "—")[:110], ", ".join(sorted(set(COLUMNS_USING[name]))[:3])]
                for name, desc in sorted(members.items())
            ],
        )
        domain_sections.append(f"### {domain}\n\n{len(members)} members.\n\n{table}")

    write(
        OUT / "04-glossary.md",
        f"""# DORA glossary

The vocabulary behind the {len(rows)} columns, from {SOURCE}.

**Definitions.** These are the framework's own wording, not legal definitions. Where a
precise one is needed, cite {AUTHORITY}.

## Properties

What a column holds, and its type. {len(PROPERTIES)} distinct properties across {len(rows)} columns -
so most columns have their own, which is what makes DORA a register rather than a
measurement.

{md_table(["Property", "Type", "Columns", "Used by"], prop_rows)}

## Domain members

Only the columns that carry a dimensional context have these: {len(vocab) - len(rows)} of {len(rows)}.
{sum(len(m) for m in MEMBERS_BY_DOMAIN.values())} members across {len(MEMBERS_BY_DOMAIN)} domains.

"""
        + "\n\n".join(domain_sections),
    )


def write_glossary_csv() -> None:
    """The DORA vocabulary as OpenMetadata glossary terms.

    A separate glossary from PAY's: different framework, different vocabulary, and a
    shorter FQN than nesting them under one root would give. Name carries no dot, for the
    same reason as PAY_4_2 - OpenMetadata quotes an FQN part that contains one.

    Header and level structure match the PAY export, so the same four-pass importer
    loads it: a parent is resolved against the database and a dry run persists nothing,
    so a term whose parent sits in the same file can never validate.
    """
    header = [
        "parent",
        "name*",
        "displayName",
        "description",
        "synonyms",
        "relatedTerms",
        "references",
        "tags",
        "reviewers",
        "owner",
        "glossaryStatus",
        "color",
        "iconURL",
        "domains",
        "extension",
    ]

    def row(parent: str, name: str, desc: str, synonyms: str = "", status: str = "Draft") -> list[str]:
        out = [parent, name, name, desc, synonyms, "", DPM_DICTIONARY, "", "", "", status]
        return out + [""] * (len(header) - len(out))

    rows_out = [
        row("", "Properties", "What a DORA column holds, and its data type.", status="Approved"),
        row(
            "", "Domains", "Value domains used by the DORA columns that carry a dimensional context.", status="Approved"
        ),
        row("", "Templates", "The templates of the DORA register of information.", status="Approved"),
    ]

    # One term per template, so a table can carry a link a reader can follow rather than a
    # sentence. Underscores in the name: a dot in an FQN part has to be quoted, and that
    # has broken this import before.
    for code, rs in sorted(by_template.items()):
        table = code.replace(".", "_")
        name = rs[0]["template_name"]
        rows_out.append(
            row(
                f"{GLOSSARY}.Templates",
                table,
                f"Template {code} of the DORA register of information, EBA DPM module 1.1.0: {name}. "
                f"Warehouse table {table}, {len(rs)} datapoint column(s). The Context Center article "
                f"named {table} holds the columns and datapoint ids.",
                status="Approved",
            )
        )

    for name, v in sorted(PROPERTIES.items()):
        used = sorted(set(COLUMNS_USING[name]))
        rows_out.append(
            row(
                f"{GLOSSARY}.Properties",
                name,
                f"Property of the DORA register of information. Data type: {v['extra'] or 'unspecified'}. "
                f"Used by {len(used)} column(s): {', '.join(used[:6])}. "
                f"Label transcribed verbatim; for a definition see {AUTHORITY}.",
            )
        )

    for domain, members in sorted(MEMBERS_BY_DOMAIN.items()):
        rows_out.append(
            row(
                f"{GLOSSARY}.Domains",
                domain,
                f"Value domain of the DORA register: {len(members)} members.",
                status="Approved",
            )
        )
        for member, desc in sorted(members.items()):
            used = sorted(set(COLUMNS_USING[member]))
            rows_out.append(
                row(
                    f"{GLOSSARY}.Domains.{domain}",
                    member,
                    (desc or f"Member of the {domain} domain in the DORA register.")[:400]
                    + (f" Used by: {', '.join(used[:6])}." if used else ""),
                )
            )

    with (OUT / "05-openmetadata-glossary.csv").open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows([header, *rows_out])
    print(f"  glossary CSV: {len(rows_out)} terms")


def write_templates() -> None:
    for code, rs in sorted(by_template.items()):
        first = rs[0]
        kind = first["row_kind"]
        grid = md_table(
            ["Column", "Label", "Row", "Datapoint"],
            [
                [
                    r["column_code"],
                    r["column_label"] or "—",
                    OPEN_ROW_PLACEHOLDER if r["row_code"] == "*" else r["row_code"],
                    r["datapoint_id"],
                ]
                for r in sorted(rs, key=lambda x: (x["column_code"], x["row_code"]))
            ],
        )
        note = (
            f"Rows are **open**: one per record. The row number in a column name is an ordinal "
            f"(`r{OPEN_ROW_PLACEHOLDER}` in the warehouse, `r*` in the DPM) and does not narrow the datapoint - "
            "the column alone identifies it."
            if kind == "open"
            else (
                f"The row code is fixed at `{first['row_code']}` rather than `r*`, but this template still "
                f"has a single row: its {len(rs)} datapoints differ by column. The column identifies the "
                "datapoint, as everywhere else in DORA."
            )
        )
        write(
            OUT / "03-templates" / f"{code}.md",
            f"""# {code} — {first["template_name"]}

| | |
|---|---|
| **Framework** | DORA, register of information |
| **Template** | `{code}` |
| **Warehouse table** | `{first["table_name"]}` |
| **Rows** | {kind} |
| **Datapoints** | {len(rs)} |
| **Source** | {SOURCE} |

{first["template_desc"] or ""}

{note}

## Columns

{grid}

## Suggested OpenMetadata description for the table

```text
{first["template_name"]}, template {code} of the DORA register of information.
Contains {len(rs)} datapoints. {"Rows are open: one per record." if kind == "open" else f"{len(rs)} fixed rows."}
Source: {SOURCE}.
```
""",
        )


write_overview()
write_agent_instructions()
write_glossary()
write_glossary_csv()
write_templates()
print(f"dora/: {len(by_template)} templates, {len(rows)} datapoints ({len(OPEN)} open rows, {len(FIXED)} fixed)")
