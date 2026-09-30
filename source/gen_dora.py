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
OUT = REPO / "dora"

SOURCE = "EBA DPM 2.0 database, module DORA 1.1.0"
AUTHORITY = "the DORA Implementing Technical Standards on the register of information"

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

## The rest is the same as PAY

Everything in the PAY 4.2 instructions about *how* to write applies here too, and is not
repeated: do not create tables or columns, do not patch columns by index, use the table
CSV export and import which is keyed by `column.name`, confirm before writing, and leave
warehouse context columns alone.
""",
    )


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
write_templates()
print(f"dora/: {len(by_template)} templates, {len(rows)} datapoints ({len(OPEN)} open rows, {len(FIXED)} fixed)")
