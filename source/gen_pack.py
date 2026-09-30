"""Generate the OpenMetadata documentation pack from the normalised DPM data."""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

# Paths resolve against the repository root so the pipeline reproduces from a fresh
# clone: `uv run source/extract_dpm.py && uv run source/vocab.py && uv run source/gen_pack.py`.
REPO = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO / "source"
XLSX = SOURCE_DIR / "20260106_Annotated_Table_Layout__PAY_4.2_PSD_FRPPAY_4.2.xlsx"
DPM_JSON = SOURCE_DIR / "dpm.json"
VOCAB_JSON = SOURCE_DIR / "vocab.json"

OUT = REPO
DATA = json.loads(DPM_JSON.read_text(encoding="utf-8"))
VOCAB = json.loads(VOCAB_JSON.read_text(encoding="utf-8"))

LEADING_CODE = re.compile(r"^(?P<code>\d{4})\s+(?P<label>.+)$")
PAIR_RE = re.compile(r"^\((?P<a>[A-Za-z0-9]+):(?P<b>[A-Za-z0-9]+)\)\s*(?P<label>.+)$")
SOURCE = (
    "EBA PAY 4.2 (FRPPAY 4.2) annotated table layout, 2026-01-06; "
    "datapoint ids from the DPM 2.0 database, module PSD_FRP 1.1.0"
)
AUTHORITY = "EBA Guidelines on fraud reporting under PSD2 (EBA/GL/2018/05, as amended)"


def strip_code(label: str) -> tuple[str, str]:
    m = LEADING_CODE.match(label)
    return (m["code"], m["label"]) if m else ("", label)


def member_label(text: str) -> str:
    return text.split(") ", 1)[-1] if ") " in text else text


def by_template() -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for s in DATA["sheets"]:
        groups[s["sheet"].split("(")[0]].append(s)
    return groups


def dim_label(code: str) -> str:
    return VOCAB["dimensions"].get(code, {}).get("label", code)


# --------------------------------------------------------------------------------------
# Flat datapoint table - the lookup every other file points at
# --------------------------------------------------------------------------------------


# The annotated table layout renders module version PSD_FRP 1.0.1. Reporting is on 1.1.0,
# which has the same 1830 cells at the same coordinates and the same labels, but an
# entirely different set of VariableVIDs - not one id is shared between the two. Taking
# the ids from the layout would cite 1830 identifiers that do not exist in what is
# reported, so they are overridden from the DPM database, exported to the CSV beside this
# file. Verified: same coordinates both versions, zero shared ids.
DPM_VERSION = "PSD_FRP 1.1.0"
DPM_IDS = SOURCE_DIR / "dpm-psd_frp-1.1.0-datapoints.csv"


def load_dpm_ids() -> dict[tuple[str, str, str, str], dict[str, str]]:
    """Datapoint id and sign by (template, row, column, variant)."""
    with DPM_IDS.open(encoding="utf-8") as fh:
        return {(r["template"], r["row_code"], r["column_code"], r["variant"]): r for r in csv.DictReader(fh)}


DPM_BY_COORDINATE = load_dpm_ids()


def datapoint_rows() -> list[dict]:
    out = []
    for s in DATA["sheets"]:
        template = s["sheet"].split("(")[0]
        variant = s["sheet"][len(template) + 1 : -1] if "(" in s["sheet"] else ""
        metric = member_label(s["main_property"]) or next(
            (
                member_label(f["per_column"].get(next(iter(f["per_column"]), ""), ""))
                for f in s["footer"]
                if f["name"] == "Main Property"
            ),
            "",
        )
        geography = "; ".join(member_label(z["member"]) for z in s["z_axis"]) or "not broken down"
        col_members = {}
        for f in s["footer"]:
            if f["name"] == "Main Property":
                continue
            for col_code, val in f["per_column"].items():
                col_members.setdefault(col_code, []).append(f"{member_label(f['name'])}={member_label(val)}")
        for r in s["rows"]:
            row_code, row_label = (r["code"], r["label"]) if r["code"] else strip_code(r["label"])
            row_dims = "; ".join(f"{m.get('dimension') or dim_label(m['dim'])}={m['label']}" for m in r["members"])
            for col_code, dp in r["datapoints"].items():
                col = next((c for c in s["columns"] if c["code"] == col_code), {})
                # The warehouse column name: template without its separators, then the
                # row and column code. It carries no variant, so one name covers all
                # six metric x geography variants of a .01 template.
                column_name = f"{template.replace('.', '').replace('_', '')}_r{row_code}_c{col_code}"
                # The table is named for the template with its dot as an underscore:
                # template Y_01.01 lands in table Y_01_01, whose datapoint columns are
                # Y0101_rXXXX_cXXXX. One table per template, not per variant.
                table_name = template.replace(".", "_")
                # Swap the layout's id for the reported one. A coordinate with no match
                # means the layout and the DPM export disagree, which must not pass
                # silently - every description cites this id.
                key = (template, row_code, col_code, variant)
                reported = DPM_BY_COORDINATE.get(key)
                if reported is None:
                    raise SystemExit(f"No {DPM_VERSION} datapoint for {key}; regenerate the DPM export.")

                out.append(
                    {
                        "column_name": column_name,
                        "table_name": table_name,
                        "datapoint_id": reported["datapoint_id"],
                        "datapoint_id_1_0_1": dp["id"],
                        "template": template,
                        "template_name": s["title"].split(" - ", 1)[-1],
                        "variant": variant,
                        "variant_label": s["sheet_label"],
                        "metric": metric,
                        "geography": geography,
                        "row_code": row_code,
                        "row_label": row_label,
                        "column_code": col_code,
                        "column_label": col.get("label", ""),
                        "row_dimensions": row_dims,
                        "column_dimensions": "; ".join(col_members.get(col_code, [])),
                        "unit": dp["unit"],
                        "sign": reported["sign"] or dp["sign"],
                    }
                )
    return out


DPS = datapoint_rows()


# --------------------------------------------------------------------------------------
# Writers
# --------------------------------------------------------------------------------------

TEMPLATES = by_template()
DP_BY_TEMPLATE = defaultdict(list)
for d in DPS:
    DP_BY_TEMPLATE[d["template"]].append(d)

# Plain paragraph rather than a blockquote: OpenMetadata's markdown viewer renders
# "> " as a literal character instead of a quote block.
NOTE = (
    "**Definitions.** The labels below are transcribed verbatim from the annotated table "
    "layout. They are the framework's own wording, not a legal definition. Where a precise "
    f"definition is needed, cite {AUTHORITY} rather than paraphrasing this file.\n"
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    def esc(cell: object) -> str:
        return str(cell).replace("|", "\\|").replace("\n", " ")

    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def variant_of(sheet: dict) -> str:
    """The sheet's variant code, empty for a template that has none."""
    name = sheet["sheet"]
    return name[name.index("(") + 1 : -1] if "(" in name else ""


# The worked example in the agent instructions, built from the data rather than typed,
# so it cannot cite an id that the shipped CSV does not contain.
EXAMPLE_COLUMN = "Y0101_r0010_c0010"
EXAMPLE_VARIANT_ROWS = "\n".join(
    f"| {d['datapoint_id']} | {d['variant']} | {d['metric']} | {d['geography']} | {d['unit']} |"
    for d in sorted((x for x in DPS if x["column_name"] == EXAMPLE_COLUMN), key=lambda x: x["variant"])
)


def write_tables() -> None:
    for template, sheets in TEMPLATES.items():
        base = sheets[0]
        name = base["title"].split(" - ", 1)[-1]
        dps = DP_BY_TEMPLATE[template]
        kind = "losses" if template.endswith(".02") else "transactions"

        variants = md_table(
            ["Sheet", "Variant", "Metric", "Geography", "Datapoints"],
            [
                [
                    s["sheet"],
                    s["sheet_label"] or "—",
                    member_label(s["main_property"]) or "see footer",
                    "; ".join(member_label(z["member"]) for z in s["z_axis"]) or "not broken down",
                    str(sum(len(r["datapoints"]) for r in s["rows"])),
                ]
                for s in sheets
            ],
        )

        col_members = defaultdict(list)
        for f in base["footer"]:
            if f["name"] == "Main Property":
                continue
            for cc, val in f["per_column"].items():
                col_members[cc].append(f"{member_label(f['name'])} = {member_label(val)}")
        columns = md_table(
            ["Code", "Label", "Fixed dimension members"],
            [[c["code"], c["label"], "; ".join(col_members.get(c["code"], [])) or "—"] for c in base["columns"]],
        )

        col_codes = [c["code"] for c in base["columns"]]
        row_rows = []
        for r in base["rows"]:
            code, label = (r["code"], r["label"]) if r["code"] else strip_code(r["label"])
            dims = "; ".join(f"{m.get('dimension', m['dim'])} = {m['label']}" for m in r["members"]) or "—"
            # The reported id, not the layout's: the two versions share no identifiers.
            ids = [
                DPM_BY_COORDINATE.get((template, code, cc, variant_of(base)), {}).get(
                    "datapoint_id", r["datapoints"].get(cc, {}).get("id", "—")
                )
                if cc in r["datapoints"]
                else "—"
                for cc in col_codes
            ]
            row_rows.append([code or "—", label, dims, *ids])
        rows_tbl = md_table(["Row", "Label", "Dimension members", *[f"DP col {c}" for c in col_codes]], row_rows)

        geo = (
            "domestic, cross-border within the EEA, and cross-border outside the EEA"
            if len(sheets) > 1
            else "no geographical breakdown"
        )
        metrics = sorted({member_label(s["main_property"]) for s in sheets if s["main_property"]})
        metric_txt = " and ".join(metrics) if metrics else "amount of losses"

        body = f"""# {template} — {name}

| | |
|---|---|
| **Framework** | PAY 4.2 (FRPPAY 4.2), payment and fraud reporting under PSD2 |
| **Template** | `{template}` |
| **Reports** | {kind} |
| **Variants** | {len(sheets)} |
| **Datapoints** | {len(dps)} |
| **Source** | {SOURCE} |

{NOTE}

## What this template reports

`{template}` reports **{name.lower()}**, measured as {metric_txt}, split across {geo}.
Each reported figure is one datapoint identified by a stable numeric id; the id is the
only identifier that is unique on its own, because row and column codes repeat across
templates and variants.

## Variants

Each variant is one sheet in the layout. Together the variant, the row code and the
column code pin down a single datapoint.

{variants}

## Columns

{columns}

## Rows

Rows without a code are section headers in the layout; they carry no datapoint. A row's
dimension members are cumulative with the column's and the variant's.

{rows_tbl}

## Suggested OpenMetadata description for the table

```text
{name}, template {template} of the EBA PAY 4.2 (FRPPAY 4.2) framework for payment and
fraud reporting under PSD2. Reports {kind} as {metric_txt}, across {len(sheets)} variant(s)
covering {geo}. Contains {len(dps)} datapoints. Row and column codes follow the annotated
table layout; the numeric datapoint id is the stable key. Source: {SOURCE}.
```

## Suggested column descriptions

""" + "\n".join(
            f"- **`{c['code']}` {c['label']}** — {c['label']} in `{template}`."
            + (
                f" Fixed dimension members: {'; '.join(col_members.get(c['code'], []))}."
                if col_members.get(c["code"])
                else ""
            )
            for c in base["columns"]
        )
        write(OUT / "04-tables" / f"{template}.md", body)


write_tables()
print(f"wrote {len(TEMPLATES)} table files")


# --------------------------------------------------------------------------------------
# Glossary
# --------------------------------------------------------------------------------------

DOMAIN_NAMES = {
    "qPY": "Payment transaction characteristics",
    "qET": "Fraud event types",
    "qRP": "Payment related parties",
    "GA": "Geographical breakdown",
}

member_usage: dict[tuple[str, str], set[str]] = defaultdict(set)
member_dimension: dict[tuple[str, str], set[str]] = defaultdict(set)
for s in DATA["sheets"]:
    template = s["sheet"].split("(")[0]
    for r in s["rows"]:
        for m in r["members"]:
            member_usage[(m["dim"], m["member"])].add(template)
            if m.get("dimension"):
                member_dimension[(m["dim"], m["member"])].add(m["dimension"])
    # z-axis members (the sheet variant) and footer members (the column axis) carry their
    # dimension in the adjacent label, not in the member cell.
    for z in s["z_axis"]:
        d = z["dim"]
        if d and d.get("member"):
            member_usage[(d["dim"], d["member"])].add(template)
            member_dimension[(d["dim"], d["member"])].add(member_label(z["name"]))
    for f in s["footer"]:
        if f["name"] == "Main Property":
            continue
        for val in f["per_column"].values():
            m = PAIR_RE.match(val)
            if m:
                member_usage[(m["a"], m["b"])].add(template)
                member_dimension[(m["a"], m["b"])].add(member_label(f["name"]))


def write_glossary() -> None:
    lines = [
        "# PAY 4.2 glossary — domains and members",
        "",
        f"Controlled vocabulary of the EBA PAY 4.2 (FRPPAY 4.2) framework, transcribed from\n{SOURCE}.",
        "",
        "A **domain** is a set of allowed values. A **dimension** is an axis that draws its",
        "values from one domain — several dimensions share a domain, which is why a member code",
        "alone does not tell you which dimension it belongs to. The member's position in the",
        "layout does.",
        "",
        NOTE,
    ]
    for dom, members in sorted(VOCAB["domains"].items()):
        dims = sorted(c for c, d in VOCAB["dimensions"].items() if d["domain"] == dom)
        lines += [
            f"\n## Domain `{dom}` — {DOMAIN_NAMES.get(dom, dom)}",
            "",
            f"{len(members)} members, used by {len(dims)} dimension(s): "
            + ", ".join(f"`{c}` {VOCAB['dimensions'][c]['label']}" for c in dims),
            "",
            md_table(
                ["Member", "Label", "Used as dimension", "Templates"],
                [
                    [
                        f"`{code}`",
                        label,
                        "; ".join(sorted(member_dimension.get((dom, code), set()))) or "—",
                        ", ".join(sorted(member_usage.get((dom, code), set()))) or "—",
                    ]
                    for code, label in sorted(members.items(), key=lambda kv: kv[1])
                ],
            ),
        ]
    write(OUT / "03-glossary" / "domains-and-members.md", "\n".join(lines))

    # Members actually observed on each dimension - NOT the domain size, which is shared
    # by every dimension drawing on that domain and would read as 31 across the board.
    used_by_dim: dict[str, set[str]] = defaultdict(set)
    for (_dom, code), dim_labels in member_dimension.items():
        for dl in dim_labels:
            used_by_dim[dl].add(code)

    dim_rows = [
        [
            f"`{c}`",
            d["label"],
            f"`{d['domain']}`",
            DOMAIN_NAMES.get(d["domain"], ""),
            str(len(used_by_dim.get(d["label"], set()))) or "0",
            str(len(VOCAB["domains"].get(d["domain"], {}))),
        ]
        for c, d in sorted(VOCAB["dimensions"].items(), key=lambda kv: (kv[1]["domain"], kv[1]["label"]))
    ]
    write(
        OUT / "03-glossary" / "dimensions.md",
        "\n".join(
            [
                "# PAY 4.2 glossary — dimensions",
                "",
                f"The {len(VOCAB['dimensions'])} axes a datapoint can be broken down by. Each draws its allowed",
                "values from one domain; see `domains-and-members.md` for the values themselves.",
                "",
                NOTE,
                "",
                md_table(["Dimension", "Label", "Domain", "Domain name", "Members used", "Domain size"], dim_rows),
                "",
                "## Note on `Card funtion in payment`",
                "",
                "The label is spelled that way in the source layout (`funtion`). It is transcribed",
                "verbatim here so a search against the framework matches. Use the corrected spelling in",
                "user-facing descriptions and keep the original as a synonym.",
            ]
        ),
    )

    metric_rows = []
    for code, label in sorted(VOCAB["properties"].items()):
        used = sorted({d["template"] for d in DPS if d["metric"] == label})
        unit = sorted({d["unit"] for d in DPS if d["metric"] == label})
        metric_rows.append([f"`{code}`", label, ", ".join(unit) or "—", ", ".join(used) or "—"])
    write(
        OUT / "03-glossary" / "metrics.md",
        "\n".join(
            [
                "# PAY 4.2 glossary — metrics",
                "",
                "What a datapoint measures. Every datapoint carries exactly one of these.",
                "",
                NOTE,
                "",
                md_table(["Code", "Metric", "Unit", "Templates"], metric_rows),
                "",
                "`€£$` marks a monetary amount reported in the reporting currency; `#` marks a count.",
                "All datapoints in this framework are constrained to non-negative values.",
            ]
        ),
    )


write_glossary()
print("glossary written")


# --------------------------------------------------------------------------------------
# Framework overview, agent instructions, README, CSVs
# --------------------------------------------------------------------------------------


def write_framework() -> None:
    rows = []
    for t, sheets in TEMPLATES.items():
        rows.append(
            [
                f"`{t}`",
                DATA["toc"].get(t, sheets[0]["title"].split(" - ", 1)[-1]),
                "losses" if t.endswith(".02") else "transactions",
                str(len(sheets)),
                str(len(DP_BY_TEMPLATE[t])),
            ]
        )
    write(
        OUT / "01-framework.md",
        "\n".join(
            [
                "# PAY 4.2 (FRPPAY 4.2) — framework overview",
                "",
                f"Transcribed from {SOURCE}.",
                "",
                "## What this framework is",
                "",
                "PAY 4.2 is the EBA reporting framework for **payment and fraud statistics under PSD2**.",
                "Payment service providers report, per reporting period, the volume and value of payment",
                "transactions and the subset of those that were fraudulent, broken down by payment",
                "instrument, authentication method, initiation channel, counterparty geography and fraud",
                "event type.",
                "",
                "## Shape of the data",
                "",
                f"- **{len(TEMPLATES)} templates**, paired: a `.01` template reports transactions and the",
                "  matching `.02` template reports the monetary losses due to fraud for the same instrument.",
                "- **Up to 6 variants per `.01` template**, one sheet each, being the cross product of",
                "  2 metrics (amount of payment, number of transactions) and 3 geographies (domestic,",
                "  cross-border within the EEA, cross-border outside the EEA).",
                f"- **{len(DPS)} datapoints** in total, each with a stable numeric id.",
                "",
                md_table(["Template", "Subject", "Reports", "Variants", "Datapoints"], rows),
                "",
                "## Axes",
                "",
                f"A datapoint is pinned down by {len(VOCAB['dimensions'])} possible dimensions drawn from",
                f"{len(VOCAB['domains'])} domains, plus one of {len(VOCAB['properties'])} metrics. See",
                "`03-glossary/`.",
                "",
                "## What is not in here",
                "",
                "The layout carries labels, codes and structure. It does **not** carry the regulatory",
                "definitions, the validation rules between datapoints, or the submission schedule.",
                f"For those, go to {AUTHORITY}.",
            ]
        ),
    )


def write_agent_instructions() -> None:
    write(
        OUT / "02-agent-instructions.md",
        f"""# How to describe PAY 4.2 assets in OpenMetadata

Instructions for an agent writing table, column and glossary descriptions for assets
derived from the EBA PAY 4.2 (FRPPAY 4.2) reporting framework.

## Anatomy of an identifier

A fully qualified datapoint has four parts. Physical table and column names usually
encode some of them:

    Y_03.01 ( 0010 )      R0080          C0020            3260891
    template  variant     row code       column code      datapoint id
    │         │           │              │                │
    │         │           │              │                └── unique on its own
    │         │           │              └── only unique within a template
    │         │           └── only unique within a template
    │         └── metric x geography; only unique within a template
    └── subject area

**The numeric datapoint id is the only part that is unique on its own.** Row code `0010`
exists in every template and means something different in each. Never describe a column
from its row or column code alone.


## Physical tables

One table per template, named for the template with its dot as an underscore, so
`Y_01.01` lands in `Y_01_01`. A row is one submission. Columns come in two kinds.

**Datapoint columns** match this, with named groups so nothing has to be inferred:

```text
^(?P<prefix>[A-Za-z]{{1,}})(?P<major>[0-9]{{2}})(?P<minor>[0-9]{{2}})_r(?P<row>[0-9]{{4}})_c(?P<col>[0-9]{{4}})$
```

Note the group widths: `major` and `minor` are **two** digits each, `row` and `col` are
four. For `Y0101_r0010_c0010` that gives `prefix=Y`, `major=01`, `minor=01`, `row=0010`,
`col=0010`.

The same identity appears in three forms. The only difference between them is
punctuation, and the column prefix is the one that has none:

| Form | Example | Shape |
|---|---|---|
| Column prefix | `Y0101` | prefix, major, minor, run together, no separator |
| Template code | `Y_01.01` | underscore after the prefix, dot between major and minor |
| Table name | `Y_01_01` | underscore after the prefix, underscore between major and minor |

So going from a column name to either of the others is substitution, not inference:

| From | To | Rule |
|---|---|---|
| `Y0101` | `Y_01.01` | join prefix, major, minor with underscore then dot |
| `Y0101` | `Y_01_01` | join prefix, major, minor with underscore then underscore |
| `A0001` | `A_00.01`, `A_00_01` | the same, nothing about it is PAY-specific |

Verified against all 320 distinct column names in this framework: no exceptions. The
prefix is a single letter in everything seen so far, but the pattern allows more so a
framework that uses two is not silently rejected.

These are the reported figures and the ones this pack describes.
They are typically stored as `varchar`, so an amount or a count is text in the database
even though the framework types it as monetary or numeric. Describe what the value is;
leave the storage type to whatever profiles the column.

**Context columns** are everything else: the delivery, period, company, currency and
form frame around the figures. A real table looks like

    Data_Delivery_SK, Period_SK, Company_SK, Receive_Date,
    Original_Currency_SK, Original_Currency, Exchange_Rate_SEK,
    No_Of_Revisions, Form_BK, Form_Name, Taxonomy_Name,
    Company_BK, Company_Name, Company_Type_Code, Company_Type_Label,
    Period_Name, Period_Start_Date, Period_End_Date, Period_Type, ReferenceDate,
    Y0101_r0010_c0010, Y0101_r0020_c0010, ...

**Do not resolve a context column against this pack.** `Period_SK` is not a datapoint
and has no framework meaning; describing it from here would be wrong. A column that does
not match the datapoint pattern is warehouse context - describe it as such or leave it.
The pattern matches all 320 datapoint column names in this framework and none of the
context columns above.

Check `Taxonomy_Name` first. A warehouse holding several EBA taxonomies uses the same
naming convention for all of them, so a `Y0101_...` column only means PAY 4.2 when the
table is PAY 4.2.

## Warehouse column names

Columns in the warehouse are named `<TEMPLATE><ROW><COLUMN>`, with the template's
separators removed:

    Y0101_r0010_c0010
    │     │     └── column code 0010
    │     └── row code 0010
    └── template Y_01.01, dots and underscores stripped

`05-datapoints.csv` carries this as its first field, `column_name`, so a column resolves
with one lookup.

**A column name does not identify a single datapoint.** It carries no variant, and a
`.01` template has six of them - two metrics crossed with three geographies. 302 of the
320 distinct column names map to six datapoints each; only the 18 from the `.02` loss
templates, which have no variants, map to one.

So `Y0101_r0010_c0010` is all six of these:

| Datapoint | Variant | Metric | Geography | Unit |
|---|---|---|---|---|
{EXAMPLE_VARIANT_ROWS}

Resolve the variant from the table, not the column: which metric and which geography the
table holds is a property of the table, whether that is in its name, a partition, or a
filter in the pipeline that loads it. If you cannot establish it, describe what the
column means across all six and say the variant is set by the table - do not pick one.

The row and column parts are shared, so everything except metric, geography, unit and
the datapoint id is the same for all six: same row label, same column label, same
dimension members. That common part is what a description can always state.

## Lookup procedure

**Where the data is.** If you are reading this through MCP you do **not** have
`05-datapoints.csv` - it lives in the repository and is what `describe_table.py` uses.
What you have is this article and one page per template, loaded into the Context Center
under `EBA` then `PAY 4.2 (FRPPAY 4.2)` then `Templates`. Each template page carries its
full row and column grid with the datapoint ids. That is your lookup table.

1. Split the column name with the pattern above and build the template code:
   `Y0101_r0010_c0010` gives template `Y_01.01`, row `0010`, column `0010`.
2. **If a `lookup_datapoint` tool is available, call it and skip to step 5.** It answers
   from `pay42.duckdb` and cannot land on the wrong row. Reading the grid by eye is the
   fallback, not the method. It covers DORA as well and picks the rule itself: PAY needs
   a row and a variant, DORA needs neither.
3. Otherwise read the page titled with that template code — `find_context` on `Y_01.01`,
   or `get_entity_details` if you already hold its FQN. Do not search for the column name
   itself; it appears nowhere in the pages.
4. In that page, find the row whose code is `row` and read the datapoint id under the
   column whose code is `col`. The row's label and dimension members are on the same
   line, and the column's fixed members are in the Columns table above it.
5. **Check what you read.** The row code printed on the line you used must equal the
   `row` group from the column name, and the column code must equal `col`. If you took
   `Y0101_r0010_c0010` and are looking at row 0030, you are one line off - a real failure
   seen in practice, where the description was correct prose about the wrong datapoint.
6. Establish the variant from the table, not the column. The page's Variants table lists
   all six with their metric and geography.

   If the table does not tell you which one it holds, say so and write only what is
   constant. These are measured facts about this data, not a judgement call:

   | Constant across all six variants | Differs per variant |
   |---|---|
   | row code, row label | **datapoint id** |
   | column code, column label | **unit** (amount or count) |
   | dimension members | **metric** |
   | template code | **geography** |

   So with no variant you have **no datapoint id and no unit**. Stating either is
   inventing one of six answers. Name the row, the column, the dimension members and the
   template, and say the variant is set by the table.

   **Do not characterise the variants from memory either.** They are metric crossed with
   geography - amount or count, domestic or within the EEA or outside it - and nothing
   else. An agent handed the six in a tool response still paraphrased them as "Payments
   in EUR", which no variant is. Quote the labels you were given.

   `lookup_datapoint` returns them spelled out, and a `determining_the_variant` hint
   with the counts for that particular table. It cannot see the warehouse, and neither
   can you: settle it from `get_entity_details`, which carries the column list and
   `totalColumns` when it truncates. One variant's worth of datapoint columns means the
   pipeline picked one and only a person knows which. MCP exposes no sample data, so
   there is no third route.
7. If you cannot resolve an identifier, say so in the description rather than guessing.
   A wrong regulatory description is worse than a missing one.

## Writing the description

State, in this order: what is measured, for which payment instrument, under which
breakdown, and the source. Keep it to two or three sentences.

```text
Number of fraudulent card-based payment transactions initiated electronically and
authenticated via strong customer authentication, reported by the issuing payment
service provider, for transactions cross-border within the EEA. Datapoint 3260891 of
template Y_03.01 (EBA PAY 4.2), row 0080, column 0020. Unit: count, non-negative.
```

Rules:

- **Do not invent regulatory definitions.** The labels here are the framework's own
  wording. Where a precise definition is needed, cite {AUTHORITY} rather than paraphrasing.
- **Do not silently correct the source.** `Card funtion in payment` is misspelled in the
  layout. Use the corrected spelling in prose, keep the original as a synonym so a search
  against the framework still matches.
- **Keep the codes in the text.** They are what a reporting analyst greps for.
- **Do not assert the physical column's semantics** beyond what the datapoint says. If a
  column is named after a datapoint but contains something else, that is a data quality
  finding, not a description.

## Writing the description back over MCP

Three tools, in this order. Tool names and argument shapes are as the OpenMetadata MCP
server defines them.

**1. Find the table.** `search_metadata` or `semantic_search`. Use the
`fullyQualifiedName` and `entityType` from the result verbatim - do not assemble an FQN
yourself.

**2. Read it.** `get_entity_details` with `entityType: "table"` and that `fqn`. Never
patch a field you have not read: the patch paths are positional and the current values
decide whether you are adding or replacing.

A PAY 4.2 table is wide - up to about a hundred columns once the context columns are
counted - so the response paginates. When it sets `columnsTruncated`, keep calling with
`columnOffset` set to the previous `columnOffset` plus `returnedColumns` until
`hasMoreColumns` is false.

**3. Patch it.** `patch_entity` with `entityType`, `fqn` and `patch`, an RFC 6902 array
as a JSON string:

```json
[
  {{"op": "replace", "path": "/description", "value": "Credit transfers transactions..."}},
  {{"op": "replace", "path": "/columns/20/description", "value": "Amount of credit..."}},
  {{"op": "replace", "path": "/columns/21/description", "value": "Amount of credit..."}}
]
```

Use `replace` when the field came back in step 2 and `add` when it did not. Put every
column of one table in a single patch rather than one call per column.

### Do not patch columns by index

`/columns/N/description` addresses the array positionally, and the array you read back
from `get_entity_details` is **not** the stored one — it is paginated and trimmed for
context, as that tool's own description says. Index 17 in what you read is not index 17
in the entity, so a correct description lands silently on the wrong column. No error is
raised. This is not something careful counting fixes.

Use the name-keyed path instead. Tables have a CSV export and import that address
columns by `column.name`:

    GET /v1/tables/name/{{fqn}}/export           text/plain CSV of the current columns
    PUT /v1/tables/name/{{fqn}}/import?dryRun=   the same CSV back

Header, from `json/data/table/tableCsvDocumentation.json` in the server source:
`column.name*, column.displayName, column.description, column.dataTypeDisplay,
column.dataType*, column.arrayDataType, column.dataLength, column.tags,
column.glossaryTerms`.

Read the export, change only `column.description` and `column.glossaryTerms` on the rows
whose name matches a datapoint, leave every other row byte-for-byte as it came back, and
write it home. `column.dataType` is required, so round-tripping the export rather than
composing a CSV is what keeps it correct.

`describe_table.py` in this pack does exactly that:

    uv run describe_table.py SQLSASTest.FIDW_BI.dbo.Y_01_01 --variant 0010 --commit

Prefer it over doing this by hand. It resolves each column against `05-datapoints.csv`,
refuses to guess a variant, and never touches a context column.

`patch_entity` is still right for the **table's own** description, which is not an array:

```json
[{{"op": "replace", "path": "/description", "value": "Credit transfers transactions..."}}]
```

### Linking the glossary

A column can carry the matching glossary term instead of repeating its definition:

```json
[{{"op": "add", "path": "/columns/20/tags/-", "value": {{
    "tagFQN": "PAY_4_2.Domains.Payment transaction characteristics.Credit transfers",
    "source": "Glossary", "labelType": "Manual", "state": "Suggested"}}}}]
```

All four of `tagFQN`, `source`, `labelType` and `state` are required. `Suggested` leaves
it for a stewards' review; use `Confirmed` only when you resolved the term from a
datapoint id rather than from a label match.

### What not to do

- **Never `create_entity` for a table or column.** They come from ingestion. If the
  target does not exist, say so - do not create it.
- **Do not patch a context column** against this pack. `Period_SK` has no framework
  meaning.
- **Confirm before writing.** Writes take effect immediately and overwrite what is
  there. A table that already has a human-written description is not yours to replace
  without being asked.
- **Do not guess the variant.** If the table does not establish the metric and geography,
  describe what holds across all six and say the variant is set by the table.

## Glossary and ontology

`06-openmetadata-glossary.csv` is a bulk import of the controlled vocabulary: one parent
term per domain, one child term per member, plus the dimensions and metrics. Link a
column to a term rather than repeating the definition in the column description.

The hierarchy to expect in the ontology explorer:

    PAY 4.2
    ├── Domains
    │   ├── Payment transaction characteristics (31 members)
    │   ├── Fraud event types (12 members)
    │   ├── Payment related parties (8 members)
    │   └── Geographical breakdown (3 members)
    ├── Dimensions ({len(VOCAB["dimensions"])}, each drawing values from one domain)
    └── Metrics ({len(VOCAB["properties"])})

Several dimensions share a domain, so a member code alone does not identify a dimension.
`Form of payment` and `Type of authentication` both draw on domain `qPY`. Resolve the
dimension from the datapoint row, never from the member code.
""",
    )


def write_lookup_tool_doc() -> None:
    """How to wire the lookup into an agent that has a local tool list."""
    write(
        OUT / "08-lookup-tool.md",
        """# Adding the lookup as an agent tool

`pay42_lookup.py` resolves a warehouse column name to its datapoint without anyone
counting rows on a page. Wiring it in takes three steps.

## 1. Build the store

```bash
uv sync
uv run source/build_duckdb.py
```

`pay42.duckdb` is derived and gitignored. Rebuild it after `gen_pack.py`; the lookup
refuses to run without it rather than answering from a stale file.

## 2. Register the tool

`LOOKUP_DATAPOINT_TOOL_DEFINITION` is the function schema, in strict mode. Add it to the
list the agent sends as `tools`:

```python
from pay42_lookup import LOOKUP_DATAPOINT_TOOL_DEFINITION

TOOLS = [
    *EXISTING_TOOLS,
    LOOKUP_DATAPOINT_TOOL_DEFINITION,
]
```

## 3. Dispatch it

Add a branch wherever local tool calls are executed - the counterpart to whatever
handles the MCP ones. The exact place depends on the app; in a Chainlit loop it is the
function the message handler calls for non-MCP tools.

**The model sends `arguments` as a JSON string, not a dict.** Parse it before use:

```python
import json

from pay42_lookup import LOOKUP_DATAPOINT_TOOL_NAME, lookup_datapoint

tool_name = raw_tool_call["function"]["name"]
arguments = json.loads(raw_tool_call["function"].get("arguments") or "{}")

match tool_name:
    case LOOKUP_DATAPOINT_TOOL_NAME:
        # strict mode always sends variant, as null when the table does not fix one.
        output = lookup_datapoint(arguments["column_name"], arguments["variant"])
    case _:
        ...
```

If the app already has a helper that parses the argument string - something like
`parse_args(raw_tool_call["function"].get("arguments", "{}"))` - use that instead of
`json.loads`, so the branch behaves like every other tool.

`lookup_datapoint` is synchronous and reads a local file, so it needs no await and no
client. It returns a dict; serialise it the same way the other tool outputs are.

## What it answers

With a variant, the resolved datapoint. Without one, the fields common to all six plus
the six candidates, and a message saying not to state a datapoint id or a unit - those
are exactly what differs. It never picks a variant on its own.

For a name that resolves to nothing it says so and repeats the pattern, so a context
column like `Period_SK` comes back as a refusal rather than a guess.

## Where the files go

DuckDB reads no environment variables of its own - every directory is a `SET` or a
connection config - so these are ours, with the usual `PAY42_` prefix and `.env` support:

| Variable | Default | What it moves |
|---|---|---|
| `PAY42_DB` | `pay42.duckdb` beside the module | the store itself |
| `PAY42_TEMP_DIR` | `<db>.tmp` | scratch files when a query spills |
| `PAY42_EXTENSION_DIR` | `~/.duckdb/extensions` | downloaded extensions |
| `PAY42_MEMORY_LIMIT` | 80% of RAM | how much it may hold before spilling |

The build script honours `PAY42_DB` and `PAY42_TEMP_DIR` too, so a build and a read
cannot disagree about the path.

`SET temp_directory` does the same job and works on a read-only connection, but it is
global to the database instance: a `SET` in one connection changes the setting for every
other one in the process, including connections opened afterwards. The lookup therefore
passes `config=` at connect time, which stays scoped to that call. The build script uses
`SET`, which is harmless in a one-shot process.

Two of these matter outside a developer checkout. Scratch files land next to the
database by default, so a read-only mount holding the store has nowhere to spill;
`PAY42_TEMP_DIR` fixes that. And in a container without a writable home, extension
downloads fail unless `PAY42_EXTENSION_DIR` points somewhere real - though this lookup
loads no extensions, so that only bites if you query the file yourself.

## Two notes on the store

Compression is automatic and per column; DuckDB chooses Dictionary for these strings and
there is no maximum to turn up. The block size is what matters at this size - the 256 KiB
default rounds a 1830-row database up past the CSV it came from, so the build uses 16 KiB
and a CHECKPOINT, which brings it to about 490 KiB with the indexes.

The same file answers ad-hoc SQL, which is often quicker than asking an agent:

```bash
duckdb pay42.duckdb -c "SELECT * FROM datapoints WHERE row_label ILIKE '%fraud%' LIMIT 5"
duckdb pay42.duckdb -c "SELECT term_fqn FROM column_terms WHERE column_name = 'Y0101_r0020_c0010'"
```
""",
    )


def write_agent_prompt() -> None:
    """The short stanza that goes into an agent's system prompt.

    Everything else in this pack is retrieved on demand. This is the part that has to be
    in effect before the agent knows there is anything to retrieve, plus the rules that
    must hold even when retrieval is skipped or fails.
    """
    write(
        OUT / "07-agent-prompt.md",
        """# Agent prompt for EBA reporting frameworks

Paste the block below into the system prompt of an agent that describes assets in
OpenMetadata. It is deliberately short: the trigger, and the rules that must hold even if
nothing is retrieved. The content lives in OpenMetadata as Context Center articles and
glossary terms, reachable with `find_context`.

It covers every framework in this pack. The frameworks resolve differently, and the
block says which rule belongs to which rather than assuming one.

```text
When describing a table or column from an EBA reporting framework, first read the
matching article (find_context) and follow it:

  table Y_*  columns Y....._r...._c....   PAY 4.2, payment and fraud reporting
                                          "How to describe PAY 4.2 assets in OpenMetadata"
  table B_*  columns B....._r..._c....    DORA, register of information
                                          "How to describe DORA assets in OpenMetadata"

A datapoint column splits the same way in both:

  ^(?P<prefix>[A-Za-z]{1,})(?P<major>[0-9]{2})(?P<minor>[0-9]{2})_r(?P<row>[0-9]{1,})_c(?P<col>[0-9]{4})$

major and minor are two digits each, col is four, and row is one or more - a PAY row
code is four digits, a DORA row is a record ordinal such as 999. The same identity has
three forms and only the punctuation differs: column prefix Y0101, template code
Y_01.01, table name Y_01_01.

If a lookup_datapoint tool is available, call it with the column name and nothing else.
It covers both frameworks and picks the rule itself. Otherwise build the template code
from the column name and read the Context Center page with that title; it holds the grid
with the datapoint ids. You do not have the CSV files; they are what the scripts use.

These hold regardless of what you find:

- Never create a table or column. Ingestion owns them. If the target does not exist,
  say so instead of creating it.
- Never patch a column by index. /columns/N addresses the array positionally, and the
  array get_entity_details returns is paginated and trimmed, so N does not mean the
  same thing there as in the entity - a correct description lands on the wrong column
  and nothing complains. Use the table CSV export/import, which is keyed by
  column.name, or run describe_table.py. patch_entity is fine for the table's own
  description.
- Confirm with the user before calling patch_entity. Do not replace a description a
  human wrote unless you were asked to.
- Check that the row and column codes on the line you read match the row and col groups
  from the column name. Reading one line off produces correct prose about the wrong
  datapoint, and nothing catches it.
- PAY only: a column name carries no variant. Row code, row label, column code, column
  label, dimension members and template code are the same for all six; the datapoint id,
  the unit, the metric and the geography are not. If the table does not establish the
  variant, do not state a datapoint id or a unit - that picks one of six answers.
- DORA only: the row carries no meaning. Every template has one row, written r* in the
  framework and as an ordinal in the warehouse. Template and column identify the
  datapoint on their own, and there are no variants.
- Columns that do not match the pattern are warehouse context - Period_SK, Company_BK,
  Taxonomy_Name and the like. They have no framework meaning, so do not describe them
  from a framework. Check Taxonomy_Name to confirm which framework a table belongs to:
  the naming convention is shared, so a Y0101_ column only means PAY 4.2 if the table is.
```

## Where to put it instead

If the agent runs as an OpenMetadata persona, the same text can live in the persona
context document and be fetched with `get_persona_context`. That keeps one copy for the
organisation rather than one per agent. The trigger still belongs in the prompt, because
the agent has to know to make that call.

## Adding a framework

The block names each framework's table prefix and article. A third one is two lines in
the table at the top and, if it resolves differently again, one rule in the list. Keep
the rules that apply everywhere general and mark the framework-specific ones, as the PAY
and DORA lines are.

## Two things to check first

Retrieval only works if the server supports it. `company_context` needs vector embeddings
configured for its `query` mode - without them only `fqn` lookups work. And knowledge
pills are extracted asynchronously, so confirm the articles reached
`pageProcessingStatus: Processed` before relying on them being searchable.
""",
    )


def write_csvs() -> None:
    fields = list(DPS[0].keys())
    with (OUT / "05-datapoints.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(DPS)

    # Header copied from openmetadata-service json/data/glossary/glossaryCsvDocumentation.json.
    # The import takes glossary TERMS only - the glossary itself must already exist, and an
    # empty `parent` puts a term directly under it. glossaryStatus takes Draft, Approved or
    # Deprecated.
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
    WIDTH = len(header)
    # The glossary NAME carries no dot. OpenMetadata's FullyQualifiedName.quoteName wraps
    # any part containing a dot in double quotes, so a glossary called "PAY 4.2" is stored
    # as "PAY 4.2".Domains while a parent column written as PAY 4.2.Domains does not match
    # it - the import then fails with "Entity PAY 4.2.Domains ... not found". The readable
    # form lives in displayName instead.
    GLOSSARY = "PAY_4_2"

    def fqn(*parts: str) -> str:
        """Join FQN parts the way OpenMetadata does, quoting the ones that need it."""
        quoted = [f'"{p.replace(chr(34), chr(34) * 2)}"' if ("." in p or '"' in p) else p for p in parts]
        return ".".join(quoted)

    def row(parent, name, display, desc, synonyms="", related="", status="Draft"):
        out = [parent, name, display, desc, synonyms, related, "", "", "", "", status]
        return out + [""] * (WIDTH - len(out))

    rows = [
        row("", g, g, f"{g} of the PAY 4.2 framework.", status="Approved") for g in ("Domains", "Dimensions", "Metrics")
    ]

    for dom, members in sorted(VOCAB["domains"].items()):
        dom_name = DOMAIN_NAMES.get(dom, dom)
        rows.append(
            row(
                fqn(GLOSSARY, "Domains"),
                dom_name,
                dom_name,
                f"Domain `{dom}` of PAY 4.2: the {len(members)} allowed values for the dimensions that draw on it.",
                synonyms=dom,
                status="Approved",
            )
        )
        for code, label in sorted(members.items(), key=lambda kv: kv[1]):
            dims = sorted(member_dimension.get((dom, code), set()))
            tpls = sorted(member_usage.get((dom, code), set()))
            desc = (
                f"Member `{code}` of domain `{dom}` ({dom_name}) in PAY 4.2. "
                + (f"Used as a value of: {', '.join(dims)}. " if dims else "")
                + (f"Appears in template(s): {', '.join(tpls)}. " if tpls else "")
                + f"Label transcribed verbatim from the layout; for a definition see {AUTHORITY}."
            )
            rows.append(row(fqn(GLOSSARY, "Domains", dom_name), label, label, desc, synonyms=code))

    for code, d in sorted(VOCAB["dimensions"].items(), key=lambda kv: kv[1]["label"]):
        dom_name = DOMAIN_NAMES.get(d["domain"], d["domain"])
        rows.append(
            row(
                fqn(GLOSSARY, "Dimensions"),
                d["label"],
                d["label"],
                f"Dimension `{code}` of PAY 4.2. Draws its values from domain `{d['domain']}` ({dom_name}).",
                synonyms=code,
                related=fqn(GLOSSARY, "Domains", dom_name),
            )
        )

    for code, label in sorted(VOCAB["properties"].items()):
        units = sorted({d["unit"] for d in DPS if d["metric"] == label})
        rows.append(
            row(
                fqn(GLOSSARY, "Metrics"),
                label,
                label,
                f"Metric `{code}` of PAY 4.2. Unit: {', '.join(units) or 'n/a'}. Non-negative.",
                synonyms=code,
            )
        )

    with (OUT / "06-openmetadata-glossary.csv").open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows([header, *rows])
    return len(rows)


write_framework()
write_agent_instructions()
write_agent_prompt()
write_lookup_tool_doc()
GLOSSARY_TERMS = write_csvs()
n = GLOSSARY_TERMS
print(f"framework + agent instructions written; glossary CSV rows: {n}")


write(
    OUT / "README.md",
    f"""# om-eba-annotatedtpl

The EBA **PAY 4.2 (FRPPAY 4.2)** annotated table layout — payment and fraud reporting
under PSD2 — normalised from a 55-sheet spreadsheet into documentation an agent can use
when describing tables, columns and glossary terms in OpenMetadata.

**{len(DPS)} datapoints · {len(TEMPLATES)} templates · {len(VOCAB["dimensions"])} dimensions over
{len(VOCAB["domains"])} domains · {sum(len(m) for m in VOCAB["domains"].values())} controlled values.**

![The pack loaded as Knowledge Pages in OpenMetadata](docs/knowledge-pages.png)

## What is in here

| File | What it is | Read it when |
|---|---|---|
| `01-framework.md` | What PAY 4.2 is, the {len(TEMPLATES)} templates, the shape of the data | You need orientation |
| `02-agent-instructions.md` | How to decode an identifier and write a description | **Start here** |
| `07-agent-prompt.md` | The stanza to paste into an agent's system prompt, covering every framework | You are configuring an agent |
| `describe_table.py` | Writes descriptions and glossary terms onto a table's columns, by name | You are describing a real table |
| `pay42_lookup.py` | Deterministic datapoint lookup over DuckDB, and its tool definition | You are giving an agent a lookup tool |
| `08-lookup-tool.md` | How to register and dispatch that tool | You are wiring it into an agent |
| `03-glossary/domains-and-members.md` | The {sum(len(m) for m in VOCAB["domains"].values())} controlled values across {len(VOCAB["domains"])} domains | You need the vocabulary |
| `03-glossary/dimensions.md` | The {len(VOCAB["dimensions"])} breakdown axes | You need to know which axis a value belongs to |
| `03-glossary/metrics.md` | The {len(VOCAB["properties"])} metrics and their units | You need the unit |
| `04-tables/<TEMPLATE>.md` | One per template: variants, columns, rows, datapoint ids | You are describing a table |
| `05-datapoints.csv` | All {len(DPS)} datapoints, keyed by `table_name` and `column_name` | You have a column to describe |
| `06-openmetadata-glossary.csv` | Bulk glossary import, {GLOSSARY_TERMS} terms | You are loading the glossary |

## Warehouse column names

One table per template — `Y_01.01` lands in `Y_01_01` — with datapoint columns named
`Y0101_r0010_c0010`: template with its separators stripped, then row and column code.
`05-datapoints.csv` is keyed by both, as its first two fields.

Everything that does not match `^[A-Za-z][0-9]{{4}}_r[0-9]{{4}}_c[0-9]{{4}}$` is warehouse
context (`Period_SK`, `Company_BK`, `Taxonomy_Name`, ...) and has no framework meaning.

A column name carries no variant, so 302 of the 320 distinct names map to six datapoints
each — two metrics across three geographies — and the 18 from the `.02` loss templates
map to one. The variant is a property of the table, not the column.
`02-agent-instructions.md` has the worked example.

## Reproducing

```bash
uv sync
uv run source/extract_dpm.py    # xlsx  → source/dpm.json      (structure)
uv run source/vocab.py          # dpm   → source/vocab.json    (vocabulary)
uv run source/gen_pack.py       # both  → the markdown and CSV in this repo
```

The spreadsheet is built on merged-cell blocks: the row axis sits to the right of the
data columns, the column axis in a footer block, and the sheet axis in the header. The
merge *spans* are what identify where each block starts and ends, which is why the
extraction uses openpyxl — a plain cell reader gives you the values but not the geometry.

## Importing into OpenMetadata

```bash
export OM_HOST=https://your-host/api      # the /api suffix is required
export OM_JWT_TOKEN=...
uv run import_to_openmetadata.py --dry-run
uv run import_to_openmetadata.py --pages-only
uv run import_to_openmetadata.py --glossary-only --commit
```

| Flag | Effect |
|---|---|
| `--dry-run` | Print the page tree and stop. Contacts nothing. |
| `--pages-only` | Knowledge Pages only, skip the glossary |
| `--glossary-only` | Glossary only, skip the pages |
| `--commit` | Actually write the glossary terms. Without it, only the first pass is dry run. |
| `--reset-glossary` | **Destructive.** Hard-delete the glossary and its terms first. |
| `--verify` | Compare the database listing with the search-index listing, then stop |
| `--no-reindex` | Do not reindex after writing pages |

Markdown goes to Knowledge Pages (`PUT /v1/contextCenter/pages`) under an `EBA` root, so
a later framework can be loaded beside this one:

    EBA
    └── PAY 4.2 (FRPPAY 4.2)
        ├── Framework
        ├── Agent instructions
        ├── Agent prompt
        ├── Glossary      (dimensions, domains and members, metrics)
        └── Templates     (one page per template)

There is no bulk file upload and no document library — `docStore/document.json` is a
generic JSON payload store the UI uses for persona layouts.

![An article page](docs/agent-instructions-page.png)

### The glossary import runs in passes

The CSV holds glossary **terms**; it does not create the glossary, so the importer does
that first. Then it sends the terms one level at a time.

A term's parent is resolved against the database, and a dry run persists nothing, so a
term whose parent sits in the same file can never validate — on a freshly created, empty
glossary the import answers `Entity not found: glossaryTerm <uuid>`, naming a reference
that only ever existed in memory. The passes are therefore:

| Pass | Terms | |
|---|---|---|
| 1 | 3 | `Domains`, `Dimensions`, `Metrics` |
| 2 | 21 | the domains, dimensions and metrics themselves |
| 3 | 54 | the members |
| 4 | 14 | the rows carrying `relatedTerms`, which point from a dimension to a domain on the same level |

Each pass is dry run and then committed before the next begins, so **without `--commit`
only the first pass can be checked** — the later ones have nothing to resolve against yet.

Terms are created as `Draft` except the three grouping terms. Promote them once a domain
expert has checked the definitions: the descriptions here are structural, they say where
a term is used, not what it legally means.

### Doing it by hand

```bash
AUTH="Authorization: Bearer $OM_JWT_TOKEN"

curl -X POST "$OM_HOST/v1/glossaries" -H "$AUTH" -H 'Content-Type: application/json' -d '{{"name": "PAY_4_2", "displayName": "PAY 4.2 (FRPPAY 4.2)", "description": "..."}}'

curl -X PUT "$OM_HOST/v1/glossaries/name/PAY_4_2/import?dryRun=true" -H "$AUTH" -H 'Content-Type: text/plain' --data-binary @06-openmetadata-glossary.csv
```

The second call imports the whole file at once and **will fail** for the reason above;
split it by level first, or use the script. The header comes from
`json/data/glossary/glossaryCsvDocumentation.json` in the OpenMetadata source:
`parent, name*, displayName, description, synonyms, relatedTerms, references, tags,
reviewers, owner, glossaryStatus, color, iconURL, domains, extension`. Check it against
your own instance — `GET /v1/glossaries/documentation/csv` returns what your server
expects. An empty `parent` puts a term directly under the glossary.

The glossary is named `PAY_4_2`, not `PAY 4.2`, and carries the readable form in its
displayName. OpenMetadata quotes any FQN part containing a dot, so a glossary called
`PAY 4.2` is addressed as `"PAY 4.2".Domains`; a parent column written `PAY 4.2.Domains`
then matches nothing and every child row fails with `Entity ... not found`.

`Payment related parties` appears twice, once as a domain and once as a dimension. That
is deliberate — dimension `qKKL` carries the same label as its domain `qRP` — and the two
have different parents, so the FQNs do not collide.

## Troubleshooting

### A re-run does not change a page

`EntityRepository.updateDescription` reverts a PUT that would replace a non-empty
description when the caller is a **bot**, and answers 200 as if it had worked. A second
import from a bot token therefore leaves the old text in place while every line prints a
tick. The importer detects this and falls back to PATCH, which the server's own comment
names as the way round it; if that is refused too, the run ends by naming the pages that
kept their old body. Use a user token, or delete the pages so they are created fresh.

### Pages written but missing from the list

The UI lists pages through `/search/hierarchy`, which reads the search index, while the
write goes to the database. Indexing is asynchronous, so a fresh import can be invisible
in every list view. The importer reindexes the ids it wrote; `--verify` shows the two
counts side by side.

### The diagrams or quotes look wrong

Descriptions are sanitised on write by an OWASP HTML policy, which HTML-escapes as it
goes: a plus sign comes back as a numeric character reference, and a greater-than sign as
`&gt;`. ASCII tree connectors and markdown blockquotes do not survive. The generator
draws with box characters, uses fenced blocks instead of quotes, and fails the build if a
plus sign reaches any page.

## Licence

The code is MIT (see `LICENSE`). The PAY 4.2 content — codes, labels, datapoint ids,
structure and the source workbook — is EBA material, reproduced under the EBA legal
notice, which authorises reproduction provided the source is acknowledged. That is a
permission with an attribution condition, not a named open licence, and the MIT licence
does not extend to it. See `NOTICE`. Not affiliated with or endorsed by the EBA.

## The one thing to get right

Row code `0010` and column code `0010` exist in every template and mean something
different in each. Only the numeric **datapoint id** is unique on its own. Resolve to a
datapoint id before writing any description.
""",
)
print("README written")


# --------------------------------------------------------------------------------------
# Guard
# --------------------------------------------------------------------------------------

# OpenMetadata's markdown viewer turns '+' into &#43; and then escapes the ampersand
# again, so it shows up as a literal &amp;#43; on the page. Nothing generated here needs
# one, and it has crept back in twice, so fail the build rather than ship it.
_OFFENDERS = {"+": "renders as &amp;#43; in OpenMetadata"}
_problems = [
    f"{path.relative_to(OUT)}:{n}: {reason}\n    {line.strip()[:100]}"
    for path in sorted(OUT.rglob("*.md"))
    if "source" not in path.parts
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
    for char, reason in _OFFENDERS.items()
    if char in line
]
if _problems:
    raise SystemExit("Characters that do not survive the OpenMetadata viewer:\n  " + "\n  ".join(_problems))
print(f"guard: no offending characters in {len(list(OUT.rglob('*.md')))} markdown files")
