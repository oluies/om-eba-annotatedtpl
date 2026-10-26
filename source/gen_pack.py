"""Generate the OpenMetadata documentation pack from the normalised DPM data."""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

# Where both the annotated layout and the DPM database this pack is built from are
# published. Cited everywhere a reader might otherwise take this pack as the authority.
DICTIONARY_URL = "https://www.eba.europa.eu/risk-and-data-analysis/reporting/dpm-data-dictionary"

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

# Extracted from the DPM database by source/extract_rules.py, which needs the 139 MB
# download. The file is committed, so a checkout without the download still documents the
# real counts; zero only if it has never been generated.
RULES_CSV = REPO / "09-validation-rules.csv"
RULE_ROWS = list(csv.DictReader(RULES_CSV.open(encoding="utf-8"))) if RULES_CSV.exists() else []
PAY_RULES = len({r["rule_code"] for r in RULE_ROWS if r["module"].startswith("PSD_FRP")})
DORA_RULES = len({r["rule_code"] for r in RULE_ROWS if r["module"].startswith("DORA")})

LEADING_CODE = re.compile(r"^(?P<code>\d{4})\s+(?P<label>.+)$")
PAIR_RE = re.compile(r"^\((?P<a>[A-Za-z0-9]+):(?P<b>[A-Za-z0-9]+)\)\s*(?P<label>.+)$")
SOURCE = (
    "EBA PAY 4.2 (FRPPAY 4.2) annotated table layout, 2026-01-06; "
    "datapoint ids from the DPM 2.0 database, module PSD_FRP 1.1.0; both from the EBA DPM "
    f"Data Dictionary, {DICTIONARY_URL}"
)
AUTHORITY = "EBA Guidelines on fraud reporting under PSD2 (EBA/GL/2018/05, as amended)"

# Every term here is derived from the EBA Data Point Model, so every term carries a
# reference to the dictionary it came from. The CSV format for this column is
# name;url, repeated - so a comma in either would break the row, and neither has one.
DPM_DICTIONARY = (
    "EBA DPM Data Dictionary;https://www.eba.europa.eu/risk-and-data-analysis/reporting/dpm-data-dictionary"
)


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

                # The join key to a warehouse's own form metadata. FI's BA_Form_Cell
                # carries DPM_Cell_Code in this shape - template with a space rather than
                # an underscore - so a description can be assembled from both sides.
                # Verified to be unique across all 1830 cells.
                parts = [template.replace("_", " "), f"r{row_code}", f"c{col_code}"]
                if variant:
                    parts.append(f"s{variant}")
                dpm_cell_code = "{" + ", ".join(parts) + "}"

                out.append(
                    {
                        "column_name": column_name,
                        "table_name": table_name,
                        "dpm_cell_code": dpm_cell_code,
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

They are describable, just not from the framework. The suffix is the convention, and it
says what the column is for:

| Suffix | What it is | Always there |
|---|---|---|
| `_sk` | surrogate key (surrogatnyckel), the warehouse's own identifier | yes |
| `_bk` | business key (affärsnyckel), the identifier the source system uses | no |
| `_bid` | business id | no |

A surrogate key is warehouse plumbing and means nothing outside it; a business key is
what someone would recognise from the source system, which is the one worth describing in
business terms.

`Period_Type` is a coded column with three values: `Y` year, `Q` quarter, `M` month. State
the codes and what they mean rather than paraphrasing, since the codes are what a query
filters on.

Check `Taxonomy_Name` first. A warehouse holding several EBA taxonomies uses the same
naming convention for all of them, so a `Y0101_...` column only means PAY 4.2 when the
table is PAY 4.2. FI's `BA_Form_Cell` spans 33 taxonomy names, from `DPM_2.6` to
`DPM_4.2`, and the same cell code can mean something else in each.

Where `lookup_datapoint` can reach that table it checks for you and answers with a
`pack_overlay` line. When it says the cell is current under a release this pack does not
describe, **use the warehouse fields and leave this pack's datapoint id, unit and
dimension members out.** An id borrowed across releases is wrong in a way nothing in the
catalogue would show. The row and column labels, the form and the data type in the same
answer are still correct, and a description built from those alone is a good one - a
narrower description is not a worse description.

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
6. Establish the variant from the table **or the row**, never the column. The page's
   Variants table lists all six with their metric and geography.

   **Look for an open axis first.** The sheet axis can land in the warehouse two ways:
   one table per variant, or one table holding all of them with a context column saying
   which row is which. That column is named `Open_Axis_1` or similar and its values are
   the variant labels, one per row. Seen in the wild, so a table carrying one variant's
   worth of datapoint columns may still hold all six.

   With an open axis, a column description must not name a datapoint id or a unit: both
   depend on the row. Describe what is common and name the axis column as where the rest
   comes from. `describe_table.py` detects this and refuses `--variant` when it applies.

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

   `lookup_datapoint` returns them spelled out. Wired to the warehouse's own form
   metadata it also returns `open_axis_values`, the variant labels that column actually
   carries, read from `BA_Form_Axis` - which settles it outright, and is the only route
   that does. Unwired it returns a `determining_the_variant` hint with the counts for
   that particular table, and you settle it from `get_entity_details`, which carries the
   column list and `totalColumns` when it truncates. One variant's worth of datapoint
   columns means the pipeline picked one and only a person knows which. MCP exposes no
   sample data, so there is no third route.
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

The display name alongside it carries the labels - "Of which authenticated via strong
customer authentication - Fraudulent payment transactions" - so the description does not
repeat them.

Rules:

- **Do not invent regulatory definitions.** The labels here are the framework's own
  wording. Where a precise definition is needed, cite {AUTHORITY} rather than paraphrasing.
- **Do not silently correct the source.** `Card funtion in payment` is misspelled in the
  layout. Use the corrected spelling in prose, keep the original as a synonym so a search
  against the framework still matches.
- **Keep the codes in the text.** They are what a reporting analyst greps for.
- **Do not repeat the display name.** The row and column labels are the display name, and
  the two fields sit next to each other in the UI, so opening a description with them says
  the same thing twice. Start with what is measured. The exception is a catalogue where
  display names could not be set at all, where the labels have to go somewhere.
- **Do not assert the physical column's semantics** beyond what the datapoint says. If a
  column is named after a datapoint but contains something else, that is a data quality
  finding, not a description.
- **Name the validation rules, do not restate them.** `lookup_datapoint` returns them under
  `validation_rules` with the DPM-XL expression. Write the codes; paraphrasing an expression
  into English is how a description ends up asserting a constraint the framework does not
  impose. See below.

## Validation rules

A datapoint is usually constrained by EBA validation rules, and the lookup returns them:

```json
"validation_rules": [
  {{"rule_code": "v09123_m", "severity": "warning",
   "expression": "with {{tY_01.01, c*, s*, default: 0, interval: true}}: {{r0030}} ... {{r0010}}"}},
  {{"rule_code": "v89551_h", "severity": "warning", "expression": "...", "variants": ["0030"]}}
]
```

Put the codes in the description and stop there:

> ... Unit: count, non-negative. Validation rules (EBA DPM, warning): v09123_m, v09124_m.

Three reasons not to go further. The expression contains characters OpenMetadata's viewer
mangles. An English restatement of a formal rule is a new claim, and a wrong one in a
regulatory catalogue is worse than no claim. And the code is what the EBA's own published
rule lists are indexed by, so it is what a reporting analyst searches for.

A `variants` key means the rule reaches only those sheet variants of the column, not all
six. If the table holds one variant, the lookup has already dropped the rules belonging to
the others - do not re-add them.

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

Use the name-keyed path instead. **A column is its own entity**, addressable by FQN:

```text
GET /v1/columns/name/{{fqn}}?entityType=table    read one column
PUT /v1/columns/name/{{fqn}}?entityType=table    set description and tags together
```

The body is an `UpdateColumn`: omit `tags` and the existing ones are left alone, and the
server validates every term against the glossary, so a bad term is a 404 rather than a
silent miss.

```json
{{"description": "...", "tags": [{{"tagFQN": "PAY_4_2.Domains....", "source": "Glossary"}}]}}
```

**PATCH against a column answers 405** - verified against a live server, and the resource
carries no `@PATCH` in the source. Documentation showing a JSON patch against a column
entity does not apply to this version. The entity type is `tableColumn`, not `column`.

The table CSV export and import also work, keyed by `column.name`:

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

`describe_table.py` in this pack writes whole tables that way, through the column entity
rather than the CSV round trip:

    uv run describe_table.py SQLSASTest.FIDW_BI.dbo.Y_01_01 --variant 0010 --commit

The table part may be a pattern, which the catalogue expands rather than this pack - a
template described here may not be loaded, and a table that is loaded may be a framework
this pack does not cover:

    uv run describe_table.py 'SQLSASTest.FIDW_BI.dbo.Y*' --commit
    uv run describe_table.py 'SQLSASTest.EBATAX.bet.B*' --commit

Quote it. An unquoted `Y*` is a shell glob, and a shell with no matching file either passes
it through or fails outright depending on which shell. Only the table name may be a
pattern: the schema has to be named, because that is what the listing is scoped to.

Each table is reported on its own and one failure does not stop the rest; the run ends with
a count and the FQNs that had problems. `--variant` is refused against a pattern, since it
names what a single table holds.

Both frameworks are handled. A `B_*` table resolves against the DORA export: an open
template matches on the column code alone, because the ordinal in the column name carries
no meaning, and a fixed template like `B_99.01` matches the column name exactly. DORA
columns get terms from the `DORA_1_1_0` glossary rather than PAY's, and all 85 of them
carry at least one.

The table itself gets a description as well as a display name, saying which template it
is, how many datapoint columns it has, and - for PAY - which variant it holds. That last
part is the one thing about a PAY table a reader cannot work out from the columns, and the
reason the column descriptions have to stay silent about it when nobody knows.

### Linking the table to its article

Two links, and they do different jobs.

A **glossary term per template** now exists in both glossaries - `PAY_4_2.Templates.Y_01_01`,
`DORA_1_1_0.Templates.B_99_01` - and the table carries the one for its own template. That is
a modelled edge, so it is navigable in the UI and shows in the ontology explorer, where a
sentence is not. Existing tags on the table are kept: a tier or a PII tag has nothing to do
with this pack, and tags are a whole-array patch.

The term name uses underscores. A dot in an FQN part has to be quoted, and that has broken
this import before.

A template's **article and its term are linked to each other too**, and not by a URL: a
Context Center page carries `tags`, so `import_to_openmetadata.py` tags each template
article with its own template term. The term then lists the article and the article shows
the term, which is one object seen twice rather than two that happen to mention each other.
It needs no route, which is the point - the Context Center route is not the same across
versions.

That step runs last, after the glossary import, because the server validates every tag and
answers 404 for a term it does not know. If the glossaries are not loaded yet it says so
once and tells you to load them, rather than failing 29 times. Running it again is a no-op.

The other direction is `describe_table.py`'s job, because only it knows which warehouse
tables a template actually landed in: writing a table adds it to that article's
`relatedEntities`, so the article lists its tables and each table is one hop from its
reference text. Existing relations are kept, a second run is a no-op, and a template with no
article imported yet is reported rather than treated as an error - a description is worth
writing either way.

The **article** is named in the table description, and linked when `OM_PAGE_URL` is set:

```bash
OM_PAGE_URL='https://your-host/contextCenter/articles/{{name}}' uv run describe_table.py ... --commit
```

The route is configured rather than guessed because it changed when Knowledge Center became
Context Center and is not the same across versions - copy it out of the browser once. Unset,
the description names the article instead of linking it, which is not a loss for an agent:
`find_context` resolves an article by name.

Prefer it over doing this by hand. It resolves each column against `05-datapoints.csv`,
refuses to guess a variant, and never touches a context column.

### Three tools for writing your own text

The batch writer generates its text from the pack. When the description is yours, the
same module exposes the pieces as tools, so none of the endpoint's traps are yours to
remember:

| Tool | What it does |
|---|---|
| `read_table_metadata(table_fqn)` | the table's display name and description, then every column with its display name, description, data type and terms - one call, paging handled |
| `write_column_metadata(table_fqn, column_name, description, display_name, expect_current, terms)` | sets one column and proves it landed |
| `write_table_metadata(table_fqn, description, display_name, expect_current)` | the same for the table itself |

Pass null for anything you do not mean to change. A field the body does not carry is
left alone; a field sent empty is cleared, which is not the same thing.

Read first, always. The write refuses to replace a description it has no sign you read:
it answers `already described, and nothing says you read it` and hands you the current
text, so one retry with `expect_current` set to that text is enough. If it comes back
`it says something else now`, someone changed it between your read and your write, and
the answer carries what it says instead. A display name is not guarded that way - it is
a label, not prose, and one you pass replaces what is there.

Then it reads back what it wrote and compares. That is not belt and braces: this endpoint
answers `200` for a write a bot token was not permitted to make, keeping the old text, so
a write that did nothing is indistinguishable from one that worked until you look. When
that happens the answer says `the server answered 200 and kept the old description` -
which is about the token, not about the text, so do not rewrite the text in response.

The comparison allows for sanitisation. The server HTML-escapes the ampersand, the angle
brackets and the plus sign on write, so nothing ever comes back byte-identical, and
comparing exactly reported a write that had in fact landed as though the token had refused
it - a false alarm that reads exactly like the real thing. Descriptions generated by this
pack avoid those characters anyway: all 3788 of them are clean.

`terms` left null leaves the existing glossary terms alone; an empty list clears them.
Every term is validated against the glossary, so a term that does not exist fails the
whole write with a 404 - set the description alone if the glossary is not loaded yet.

### Two more tools, for frameworks this pack does not cover

A warehouse holds more than PAY and DORA. For a table named after any other template,
`lookup_datapoint` correctly answers that it knows nothing, and two further tools read the
EBA DPM 2.0 database directly:

| Tool | Answers |
|---|---|
| `lookup_dpm_table` | A template in any framework: its name, the module versions it belongs to, which axes are open, and every row, column and sheet with its code, label and parent |
| `lookup_dpm_cell` | One cell: its dimension members, data type, period type, whether it is reportable, and the validation rules with their expressions |

`parent_code` on a row is what an "Of which" row is a breakdown of — the nesting the
annotated layout shows only by indentation.

Both are registered **only when the DPM database has been downloaded**, because it is
139 MB and not in the repository. If they are not in your tool list, that is why, and
`uv run source/fetch_dpm2.py` is the fix. Prefer `lookup_datapoint` for PAY and DORA: it
knows the warehouse column naming and these two do not.

Two things to be careful of in their answers. Two entries with the same `rule_code` are
not a duplicate — the rule differs between the module versions listed on each, in
expression or in severity, and `v09247_s` really is a warning in PSD_FRP 1.1.0 and an
error in 1.2.0. And a template that comes back with no rows and no columns is one the
model records nothing for, 143 of 1052 in this release; it does not mean the report has no
columns.

### Registering all of this in an agent

`agent_tools.py` assembles the four definitions and dispatches them, so a host
application imports two names and cannot end up with a tool registered but not wired:

```python
from agent_tools import TOOLS, dispatch

response = client.chat.completions.create(model=..., messages=..., tools=list(TOOLS))
result = dispatch(call.function.name, call.function.arguments)
```

Two things it absorbs. `arguments` arrives as a **JSON string**, not a dict - it takes
either. And every tool here blocks on a socket or a file, so from an async loop:

```python
result = await asyncio.to_thread(dispatch, call.function.name, call.function.arguments)
```

Nothing in `dispatch` raises. A tool that fails returns `{{"error": ...}}`, which the
model can read and act on, where an exception would end the turn. `uv run agent_tools.py`
prints the definitions, so what the model will be shown can be read before it is shown.

### Display names: use the one you are given

**Do not compose a display name yourself.** `lookup_datapoint` returns it, under
`display_name` in `common`, with `table_display_name` for the table. Pass those through.

The reason is that the obvious rule is wrong. Row label then column label reads well and
is not unique: the EBA layout nests its rows, so "Of which: authenticated via strong
customer authentication" appears under several parents and the label alone is identical in
each. Measured on this framework, **63 of 214 label pairs collide that way**, and two
columns sharing a display name show up in the catalogue as two columns that look like the
same column.

What distinguishes those rows is in their dimensions, which is where the parent context
ends up once the layout is flattened. So a colliding label is extended with the dimension
members that differ within its own group, and only those:

| Column | Display name |
|---|---|
| `Y0101_r0010_c0010` | Credit transfers - Payment transactions |
| `Y0101_r0060_c0010` | Of which authenticated via strong customer authentication - Payment transactions (Initiated via remote payment channel) |
| `Y0101_r0240_c0010` | Of which authenticated via strong customer authentication - Payment transactions (Initiated via non-remote payment channel) |

Deciding that needs every row of the table side by side, which is why it is computed from
the data rather than left to you. All 320 columns of all 14 templates come out unique.

What is deliberately absent, so you can recognise a name that was invented rather than
looked up:

- **the variant**, because it belongs to the table or, with an open axis, to the row - a display name naming one would make six columns claim to be the same one
- **the codes**, because `r0010` and `c0010` are in the column name right next to it
- **the datapoint id and the unit**, for the same reason a description leaves them out when the variant is unknown

For DORA the rows are records, so a row contributes nothing and the column label is the
whole of the name.

`describe_table.py --commit` writes both from the same rule, and its dry run prints them,
so what will be written can be read before it is.

### A bot token cannot set a display name

OpenMetadata ships `ApplicationBotPolicy` with a rule that denies `EditDisplayName`, so an
application bot may write a description but not a label:

```text
403 Principal: CatalogPrincipal{{name='mcpapplicationbot'}} operation EditDisplayName
denied by role ApplicationBotImpersonationRole, policy ApplicationBotPolicy
```

Both travel in one request, so without care a denied label takes the description with it.
The write retries once without the label and reports `display_name_refused` alongside the
description it did write. **Do not retry that call** - the answer is about the token, not
about the label, and a second attempt is denied the same way.

To set display names, use a personal access token rather than the bot, or amend the policy.
With a label-only write there is nothing left to retry, so that one comes back as a plain
failure.

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

`pay42.duckdb` is derived and gitignored. **Rebuild it after every pull**: a pull brings
new code and new CSVs but leaves the old database in place, and a field added since it
was built is missing from it. The lookup checks for that and says to run the line above
rather than failing somewhere unhelpful. Rebuild it after `gen_pack.py`; the lookup
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

Or skip all of it: `agent_tools.py` in this pack is this dispatch for every tool here -
the lookup, the catalogue writers and the two DPM lookups - with `TOOLS` to register and
`dispatch(name, arguments)` to call. It takes `arguments` as either the string or a parsed dict, and it never raises.

`lookup_datapoint` is synchronous and reads a local file, so it needs no await and no
client. It returns a dict; serialise it the same way the other tool outputs are.

## What it answers

With a variant, the resolved datapoint. Without one, the fields common to all six plus
the six candidates, and a message saying not to state a datapoint id or a unit - those
are exactly what differs. It never picks a variant on its own.

For a name that resolves to nothing it says so and repeats the pattern, so a context
column like `Period_SK` comes back as a refusal rather than a guess.

Either way the answer carries `validation_rules`: the EBA validation rules that reach the
cell, each with its code, its severity and its DPM-XL expression verbatim. With a variant
given, the rules belonging to the other variants are dropped rather than listed. Without
one, a rule that reaches only some variants carries a `variants` key saying which.

Put the codes in a description, not the expressions - `02-agent-instructions.md` says why.

## Two more tools, for the rest of the DPM

`lookup_dpm_table` and `lookup_dpm_cell` read the EBA DPM 2.0 database itself, so they
answer for COREP, FINREP, resolution, ESG and every other framework in it - everything
`lookup_datapoint` correctly refuses. `agent_tools.TOOLS` includes them only when the
database has been downloaded, because a tool whose every answer is "not downloaded" costs
a turn and teaches the model to stop calling it:

```bash
uv run source/fetch_dpm2.py     # 167 MB download, then 539 MB of Access, then DuckDB
uv run dpm_lookup.py C_01.00    # the same answers, from the command line
```

`dispatch` knows both names whether or not they are registered, so a host that registered
them before the file moved gets an explanation rather than an exception.

## The warehouse's own form metadata, where there is one

`05-datapoints.csv` carries two keys a warehouse's form metadata also keys on:
`dpm_cell_code` in the shape `{{Y 01.01, r0010, c0010, s0010}}`, and `column_name` in the
shape `Y0101_r0010_c0010`. At FI the metadata is `FIDW_BI.dbo.BA_Form_Cell`, joined to
`dbo.BA_Form_Axis` on `Cell_sk`. Where it is reachable it is the primary source and this
pack is an overlay on it:

| From the warehouse | From this pack |
|---|---|
| form, taxonomy version, row and column labels | the dimension members |
| data type and the warehouse's own datapoint key | EBA's VariableVID |
| the open-axis values a column actually carries | the glossary terms |
| every form it holds | PAY 4.2 and DORA |

The split follows from what each side can know. The warehouse knows which release a cell
is current under and which variants a physical column holds; it cannot say what a
dimension member means. This pack is the other way round. So the warehouse states the
facts and the pack supplies the meaning, joined on `dpm_cell_code`.

`ba_form_cell.py` does that join when `BA_SERVER` is set, using Kerberos - no credentials
in the connection string, the ticket from `kinit` carries the identity:

```bash
kinit
export BA_SERVER=your-sql-server
uv run pay42_lookup.py Y0101_r0010_c0010
```

It scopes to `Current_flg = 1`, the definition in force. A cell code present under
several current forms is reported rather than resolved, because the column means
different things in each and only the table's own `Form_BK` says which applies.

### Which variant, answered from the database

A `.01` template has six variants and a column name that names none of them. Connected,
the tool stops guessing: `BA_Form_Axis` enumerates the `Open_Axis_value_1` values defined
for that physical column and returns them as `open_axis_values`. The warehouse stores
`Row_Column_Code` with a suffix the column name does not carry, so that lookup is a
prefix `LIKE` - with the underscores escaped, since in `LIKE` an underscore matches any
single character and these column names are full of them. Every one of them is in
that column, as rows, so a column description covers all of them and still must not name
a datapoint id or a unit - those belong to the row.

Unconnected, the tool returns the `determining_the_variant` hint instead and the agent
settles it through OpenMetadata, which is the best an agent with no database can do.

### Only where the taxonomy matches

`BA_Form_Cell` spans 33 taxonomy names, from `DPM_2.6` to `DPM_4.2`. The same cell code
can mean something else in each, so every answer carries a `pack_overlay` line saying
whether this pack's ids may be attached at all. Where the warehouse has the cell under a
release this pack does not describe, the overlay is left off rather than asserted: the
warehouse fields on their own are still a correct description, and a datapoint id
borrowed across releases is simply wrong.

### Did it actually reach SQL Server

Every answer says, in a `warehouse` field, which of the three happened:

| `warehouse` | Meaning |
|---|---|
| `not consulted - BA_SERVER is not set` | the pack answered alone |
| `no row in BA_Form_Cell for this key with Current_flg = 1` | it queried and found nothing |
| `BA_Form_Cell joined to BA_Form_Axis on <server>` | it queried and matched |
| `warehouse_lookup_failed: ...` | it tried and the query or the connection failed |

Silence would read the same as a miss, so there is none.

To test the connection on its own, before trusting any lookup, or to ask it about one
column or one cell code directly:

```bash
kinit
BA_SERVER=your-sql-server uv run ba_form_cell.py
BA_SERVER=your-sql-server uv run ba_form_cell.py Y0101_r0010_c0010
```

### Seeing the statement that ran

`BA_DEBUG=1` logs every statement the module sends, with its parameters filled in, so the
exact query can be pasted into SSMS when an answer looks wrong. It logs the row count and
the cells it folded them into as well - zero cells and six cells are both plausible
answers to the same query, and that is where the difference shows:

```bash
BA_DEBUG=1 BA_SERVER=your-sql-server uv run ba_form_cell.py Y0101_r0010_c0010
```

The log goes to stderr and the answer to stdout, so the JSON can still be piped. What
executes is the parameterised statement; the rendering is for reading. In a host
application, enable logging for the `ba_form_cell` logger instead of setting the variable.

It reports the server, the table, `SUSER_SNAME()` - who Kerberos authenticated you as -
and how many current cells the table holds. A failure comes back with the reason rather
than a traceback.

Without `BA_SERVER` the pack answers on its own, which is what an agent with no database
access gets. The enrichment never fails a lookup: a database that is down produces a note
in the answer, not an error.

**The SQL has not been run against the real table.** Treat the first run as a test and
check the column names.

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

The last bullet is for an agent that also has the DPM lookups. Drop it if yours does not:
a tool list in a prompt that the agent cannot call is an invitation to invent the answer.

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
  and nothing complains. A column is its own entity: write it by name, with
  write_column_metadata if that tool is there, or PUT /v1/columns/name/{{fqn}}.
  patch_entity is fine for the table's own description.
- Set a display name as well as a description, on the table and on every column, and
  use the one you are given: display_name and table_display_name from
  lookup_datapoint. Do not compose one. Row label plus column label is not unique,
  because the layout nests its rows, so the tool extends a repeated label with the
  dimension members that tell it apart from its siblings - which needs the whole table
  in view. Keep the variant, the codes, the datapoint id and the unit out of it.
- Confirm with the user before replacing a description a human wrote. The write tools
  refuse it unless you pass back the text you read, which is the same rule.
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
- Validation rules: lookup_datapoint returns them under validation_rules, with the
  rule code, the severity and the DPM-XL expression. Put the codes in the description -
  "Validation rules (EBA DPM, warning): v09123_m, v09124_m." - and not the expressions.
  Do not restate a rule in English: that is a new claim, and a wrong one about what the
  framework requires is worse than saying nothing.
- A framework this pack does not cover - COREP, FINREP, AML and the rest - is answered
  by the DPM lookups if they are in your tool list. They read the EBA DPM database
  directly, and between them they answer a template, a cell, an aggregate, a rule and a
  reported file:

    lookup_dpm_table       a template: its axes, their nesting, the modules it is in
    lookup_dpm_cell        one cell: dimension members, data type, validation rules
    lookup_dpm_dimensions  what a template breaks down by, and under which exact wording
    lookup_dpm_cells       the cells one dimension member covers, with datapoint ids
    lookup_dpm_sums        which rows add up to which, from the validation rules
    lookup_dpm_rule        a validation code, v0174_m, to the check it stands for
    lookup_dpm_rules       the other way: every rule that reaches one template
    lookup_dpm_datapoint   a reported dp<N> id back to the cell it is
    lookup_dpm_property    a report's column header, qCDF, to the property it names
    lookup_dpm_history     what became of a datapoint, or what has been at a coordinate,
                           across every release the database carries
    explain_report         what a reported xBRL-CSV file is, before checking it
    check_report           that module version's rules, run against the file

  Five rules hold for all of them:

  - lookup_dpm_dimensions before lookup_dpm_cells. It is what tells you the wording a
    dimension and its members actually have, and a near miss matches nothing. The same
    goes for a report's column header: qCDF is "Name of entity" and qGDF is "Name of
    Holding entity", both real, so resolving one proves nothing about which template it
    belongs to.
  - Never write a datapoint id, a cell code or a warehouse column name that did not come
    out of a tool answer. F04041_r0070_c0015 looks exactly as plausible as a real one.
  - Two versions, and they are not the same thing. taxonomy_version is the module's own
    version number, 3.3.0; dpm_release is the DPM version it belongs to, 4.2, which is
    what a reporting institution usually means by "the version". Every answer carries
    both - write both, and never one as if it were the other.
  - Ask by whichever number you have: version is the taxonomy one, dpm_release the DPM
    one. Never both in one call.
  - do_not_use marks a module version whose FromReferenceDate equals its
    ToReferenceDate: published and superseded without ever covering a reporting period,
    43 of 165 in DPM 4.4. Nothing is filed under it, so do not describe anything against
    it. "The newest" skips them.
  - active is false for a rule the EBA has deactivated. It is published and not run -
    2928 of 30791 rule scopes in DPM 4.4 - so do not tell a reader to satisfy it, and do
    not quietly leave it out either.
  - A rule code is not a stable statement. 2005 of 7514 consecutive versions of a rule
    change the expression, and others change only the severity - v0174_m is an error to
    DPM 4.1 and a warning from 4.2 with the same expression. lookup_dpm_rule returns
    `changes` saying what differed and when (rewritten, reformatted, severity,
    deactivated, reactivated, withdrawn), and a `url` per version linking to the rule as
    that release had it. Never write a code without the release it was checked under.
  - A coordinate is an address, not an identity. Within one release {T, rNNNN, cNNNN}
    names exactly one datapoint; across releases 4517 of 135043 coordinates in DPM 4.4
    have carried more than one. Before writing that a column has always meant the same
    thing - the claim a time series rests on - ask lookup_dpm_history. It answers by
    datapoint, which survives a relayout, or by coordinate, which does not, and it tells
    a rewording apart from a change of meaning: between 3.5 and 4.0 the EBA renamed
    dimensions wholesale while the members stayed, and that is not a change to report.

  Reading a code out of a validation outcome, where it rarely arrives clean:

    v0174_m        a rule. Also _h, _s, _a, _q, _e, by framework.
    v10270_a-2     a variant of a rule, numbered with a DASH. A real, separate code.
    v3775_s_62     a rule with the engine's OCCURRENCE number after an UNDERSCORE.
                   v3775_s covers 432 cells of C_20.00 and expands once per reported
                   record, so 62 says which application failed. The model has the rule,
                   never the occurrence: which record it was is in the report, not here.
                   lookup_dpm_rule strips it and reports it back as occurrence.
    p_1            a precondition. No severity and no module version of its own: it
                   gates the rules that name it, and they are checked only where it
                   holds. An outcome naming one is about a rule in its used_by.

  Pass the code as it came. Do not trim it yourself - p_10 is not p_1, and v10270_a-2 is
  not v10270_a. The lookup knows which suffixes mean what.
  - A rule code is one rule per module version: v0174_m is an error in COREP_OF 3.1.0
    (DPM 3.4) and a warning in 4.1.0 (DPM 4.2). Name the version you answered under, in
    the description and in any query you generate. Two entries with the same rule code
    are not a duplicate.
  - For a reported file, explain_report before check_report. not_evaluated is the
    checker's limit and not a pass, and a large unmapped count means the file belongs to
    another release rather than that the report is wrong.
- Columns that do not match the pattern are warehouse context - Period_SK, Company_BK,
  Taxonomy_Name and the like. They have no framework meaning, so do not describe them
  from a framework. Check Taxonomy_Name to confirm which framework a table belongs to:
  the naming convention is shared, so a Y0101_ column only means PAY 4.2 if the table is.
  Their suffix says what they are: _sk surrogate key, always present; _bk business key,
  the source system's own identifier; _bid business id. Period_Type is coded Y year,
  Q quarter, M month.
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


def write_csvs() -> int:
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

    def row(parent, name, display, desc, synonyms="", related="", status="Draft", references=DPM_DICTIONARY):
        out = [parent, name, display, desc, synonyms, related, references, "", "", "", status]
        return out + [""] * (WIDTH - len(out))

    rows = [
        row("", g, g, f"{g} of the PAY 4.2 framework.", status="Approved")
        for g in ("Domains", "Dimensions", "Metrics", "Templates")
    ]

    # One term per template, so a table can carry a real link rather than a mention in
    # prose: a glossary term is navigable in the UI and shows up in the ontology explorer,
    # where a sentence does not. The term name uses underscores - the warehouse table name -
    # because a dot in an FQN part has to be quoted and that has broken this import before.
    template_names = {dp["template"]: dp["template_name"] for dp in DPS}
    for code, name in sorted(template_names.items()):
        table = code.replace(".", "_")
        rows.append(
            row(
                fqn(GLOSSARY, "Templates"),
                table,
                f"{code} {name}",
                f"Template {code} of EBA PAY 4.2, module {DPM_VERSION}: {name}. Warehouse table "
                f"{table}. The Context Center article named {table} holds the variants, columns, "
                "rows and datapoint ids.",
                status="Approved",
            )
        )

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

Two published pages, neither of which needs anything installed:

- **[A page per template](https://oluies.github.io/om-eba-annotatedtpl/templates/)** — 327
  of them, COREP, FINREP and DORA: every cell searchable, the official Swedish and German
  beside the English, what the instructions annex says a row is, what has changed since
  the first release, and which rules check it. The DPM release is a control on the page.
- **[Ask a question](https://oluies.github.io/om-eba-annotatedtpl/)** — eleven questions
  over the same model, answered in your browser with DuckDB-WASM, each with the SQL and the
  file it read beside the answer.

![The pack loaded as Knowledge Pages in OpenMetadata](docs/knowledge-pages.png)

## What is in here

| File | What it is | Read it when |
|---|---|---|
| `01-framework.md` | What PAY 4.2 is, the {len(TEMPLATES)} templates, the shape of the data | You need orientation |
| `02-agent-instructions.md` | How to decode an identifier and write a description | **Start here** |
| `07-agent-prompt.md` | The stanza to paste into an agent's system prompt, covering every framework | You are configuring an agent |
| `describe_table.py` | Writes descriptions and glossary terms onto a table's columns, by name | You are describing a real table |
| `pay42_lookup.py` | Deterministic datapoint lookup over DuckDB, and its tool definition | You are giving an agent a lookup tool |
| `agent_tools.py` | All sixteen tool definitions, one dispatcher, and a shell front end for trying one | You are wiring the tools into an agent |
| `env.sh` | `source env.sh` reads `.env`, sets the two DuckDB stores and prints every variable the pack reads, with secrets counted rather than shown | A tool reads the wrong store, or a datapoint id will not resolve |
| `dpm_lookup.py` | Ten lookups over the whole DPM 2.0 database: a template, a cell, a reported datapoint id, a report's column header, a validation code, every rule reaching a template, what a template breaks down by, the cells one dimension member covers, which rows add up to which, and what has happened to a datapoint or a coordinate across releases | A warehouse table is COREP, FINREP or anything but PAY and DORA, you need the codes behind a business aggregate, or you are reading a report or a validation outcome |
| `check_instance.py` | Runs a module's validation rules against a reported xBRL-CSV file, as a CLI and as the `check_report` tool | You want to know whether a report adds up before you send it, or want an agent to check its own arithmetic |
| `web/` | A query page in Scala.js over that tree: pick a question, fill it in, see the answer and the SQL, with a small model that turns a question into one of eleven — published at [oluies.github.io/om-eba-annotatedtpl](https://oluies.github.io/om-eba-annotatedtpl/) | You want the model without installing anything |
| `obs/` | A page per template in Observable Framework: every cell searchable, the official Swedish and German beside the English, and the release a control rather than a build — published at [/templates/](https://oluies.github.io/om-eba-annotatedtpl/templates/) | You are reading about one template |
| `source/gen_wasm_data.py` | Writes the model as partitioned parquet a browser can query with DuckDB-WASM | You are building a web page over the DPM |
| `source/score_translation.py` | Scores a local translation model against the Official Journal's own wording, since we hold it | Someone proposes machine-translating the labels |
| `source/fetch_its_labels.py` | The official Swedish and German row labels, from the Official Journal: the DPM is English only, but the templates are an annex to an Implementing Regulation and that is published in all 24 languages | You want a label in a language the model does not carry |
| `source/apply_vr_updates.py` | Applies the EBA's between-release validation rule updates (deactivations, reactivations, severity changes) to a local DPM database | A rule's severity or activity changed since the release you downloaded |
| `source/load_to_mssql.py` | Loads the DPM database into SQL Server over TDS, authenticating with your Kerberos ticket | You want the dictionary in the same database as the reported figures |
| `display_names.py` | The rule for what a table and its columns are called | You are setting display names |
| `08-lookup-tool.md` | How to register and dispatch that tool | You are wiring it into an agent |
| `03-glossary/domains-and-members.md` | The {sum(len(m) for m in VOCAB["domains"].values())} controlled values across {len(VOCAB["domains"])} domains | You need the vocabulary |
| `03-glossary/dimensions.md` | The {len(VOCAB["dimensions"])} breakdown axes | You need to know which axis a value belongs to |
| `03-glossary/metrics.md` | The {len(VOCAB["properties"])} metrics and their units | You need the unit |
| `04-tables/<TEMPLATE>.md` | One per template: variants, columns, rows, datapoint ids | You are describing a table |
| `05-datapoints.csv` | All {len(DPS)} datapoints, keyed by `table_name` and `column_name` | You have a column to describe |
| `06-openmetadata-glossary.csv` | Bulk glossary import, {GLOSSARY_TERMS} terms | You are loading the glossary |
| `09-validation-rules.csv` | The {PAY_RULES + DORA_RULES} EBA validation rules of both modules, and every cell each one reaches | You want to know what constrains a column |
| `README_DPM2.md` | The DPM 2.0 database's data model, as diagrams, with worked queries | You are querying the model directly |

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
uv run pytest                   # the test suite
```

CI runs the same thing on every push: `ruff check`, `ruff format --check`, `ty check`,
`pytest` on Python 3.12 and 3.14, and one job that regenerates the pack from the workbook
and fails if anything in git moved. That last one is what stops a hand edit to a generated
file from shipping — the product here *is* generated files, so without it an edit to
`README.md` or `05-datapoints.csv` would survive until the next regeneration quietly
undid it.

Dependencies are kept current by Renovate (`renovate.json`), which refreshes `uv.lock`
on a schedule rather than only when a version constraint moves, and keeps the exact
action versions in the workflow current. It needs the Renovate GitHub App installed on
the repository; GitHub's own Dependabot security alerts are separate and need no
configuration at all.

`pytest` needs nothing but the checkout. The tests that do need one of the two derived
databases - `pay42.duckdb` and the DPM 2.0 download - skip with the command that builds
it rather than failing, so a fresh clone reports what it could check.

The spreadsheet is built on merged-cell blocks: the row axis sits to the right of the
data columns, the column axis in a footer block, and the sheet axis in the header. The
merge *spans* are what identify where each block starts and ends, which is why the
extraction uses openpyxl — a plain cell reader gives you the values but not the geometry.

## The DPM 2.0 database

The annotated table layout is a spreadsheet rendering of the model. The model itself is
published as an Access database, and four scripts use it:

```bash
uv run source/fetch_dpm2.py          # download, unpack, load into DuckDB (needs mdbtools)
uv run source/check_against_dpm2.py  # does this pack match the model, cell for cell?
uv run source/extract_rules.py       # → 09-validation-rules.csv
uv run source/gen_dpm2_doc.py        # → README_DPM2.md
```

**[`README_DPM2.md`](README_DPM2.md) is the map**: the 73 tables, the relationships that
actually hold between them as four diagrams, and a worked query for each thing you are
likely to want. Read it before writing SQL against this database.

It is release 4.2.1 of the DPM 2.0 database, the same release the layout comes from, at
[the DPM data dictionary]({DICTIONARY_URL}). 167 MB of zip, 539 MB of Access, 139 MB of
DuckDB, all under `source/dpm2/` and all gitignored. Reading the Access file needs
`mdbtools` 1.0 or newer — the file is ACE12, and older releases read only Jet `.mdb`.

`check_against_dpm2.py` is the one check this pack cannot do on itself. It matches every
pack datapoint against the module's reportable cells, both directions, and exits non-zero
on a difference:

```
DPM 2.0 release 4.2.1 (2026-02-15)
PSD_FRP 1.1.0: all {len(DPS)} pack rows match the model, none missing
DORA 1.1.0: all 85 pack rows match the model, none missing
```

Two details it has to absorb. The DPM writes a table code `Y_01.01` where the layout and
the warehouse write `Y 01.01`. And a cell with `IsExcluded` set is a greyed-out box in
the template — in the model, not reportable — which the pack leaves out, so the
comparison does too. `Y_01.01` has 396 cells, 72 of them excluded, and the pack has 324.

### Trying a lookup before wiring it into anything

`agent_tools.py` runs any one tool from a shell, through the same dispatcher an agent
calls, and prints the answer with a plain `json.dumps` — the host's own serialisation, so
an answer it could not hand back fails here rather than mid-turn.

```bash
uv run agent_tools.py                    # the definitions the model will be shown
uv run agent_tools.py lookup_dpm_sums table='F 12.01.a' module=FINREP9 version=null
uv run agent_tools.py lookup_dpm_dimensions table=F_04.04.1 module=FINREP9 version=null
uv run agent_tools.py lookup_dpm_cells table=F_04.04.1 dimension='Counterparty sector' \\
    member='Credit institutions' module=FINREP9 version=null
uv run agent_tools.py check_report table=Y_01.01 module=PSD_FRP version=1.1.0 instance=report.csv
uv run agent_tools.py explain_report instance=report.csv text=null limit=null
uv run agent_tools.py lookup_dpm_datapoint datapoint=dp152217
uv run agent_tools.py lookup_dpm_rule rule_code=v0174_m
uv run agent_tools.py lookup_dpm_rules table=C_01.00 module=COREP_OF version=null
```

Arguments are `key=value`, and `null` is spelled out, because that is what the schemas
offer for an unpinned module version. Take the dimension and member wording from
`lookup_dpm_dimensions`: a near miss matches nothing, and that is as true from the shell
as from the model.

### Questions that reach the tools

A question only reaches these tools if it carries a **template code** — `F 12.01.a`,
`F_04.04.1`, `Y_01_01`, `C_01.00`. Without one the model has nothing to pass and answers
from memory. The sequence below replaces a hand-maintained spreadsheet of row codes by
column codes, which is the job this is for. Every answer quoted is from FINREP9 3.3.0.

**The structure, instead of a YAML file of levels.**

> Which rows and columns does F_04.04.1 have, with the nesting?

`lookup_dpm_table` returns `parent_code` and `is_abstract` per entry — the hierarchy
itself. `0014 Gross carrying amount` is abstract: a heading with no cell of its own, whose
children are `0015, 0030, 0040, 0041`. An "of which" row is simply a child, so excluding
them is a filter on `parent_code` rather than a convention to maintain by hand.

**A dimension breakdown.**

> What does F_04.04.1 break down by? And which cells have Counterparty sector =
> Credit institutions?

`lookup_dpm_dimensions` first, always: it is what says that `Counterparty sector` is a
dimension of that template at all, and under which exact wording. Then
`lookup_dpm_cells`, which for that member returns 24 cells across rows `0040` (debt
securities) and `0100` (loans and advances) — both instrument blocks, which a hand-written
mapping of one block would have missed.

**The aggregate, as code.**

> Write a SQL query summing gross carrying amount for financial corporations in
> F_04.04.1 — counterparty is credit institutions or other financial corporations, the
> column sits under *Gross carrying amount*, no "of which" columns. **Every column name
> must come from `lookup_dpm_cells`; do not write one yourself.** Leave the table name a
> parameter and name the rule code you built the selection on.

Sixteen columns, `F04041_r0040_c0015` through `F04041_r0110_c0041`. The sentence in bold
is the one that matters: without it a model produces `F04041_r0070_c0015`, which looks
exactly as plausible and is not a cell.

**The grouping is yours, not the model's.**

> Build the same aggregation table as my notebook, but take the hierarchy from the DPM
> rather than from a YAML file. The grouping of counterparty sectors is my own business
> definition and must be an explicit dict in the code — not something you derive.

Rolling `Credit institutions` and `Financial corporations other than credit
institutions` up into one `Financial corporations` figure is not in the DPM. The model
holds the leaves; a roll-up across them is a decision, and it should read as one in the
code rather than arrive as though the EBA had said it. (The EBA does publish member
hierarchies, in `ATTT2Hierarchies` — no tool exposes them yet.)

**Reading a report file.**

> What is `report.csv`? Then check it.

`explain_report` answers what a report is before anything asks whether it holds: it
resolves a sample of its datapoint ids to cells and every column header to a property. It
takes a path or the report's text, so a few rows pasted into the conversation are enough.
The two fixed columns are `datapoint` and `factValue`; the rest are the open dimensions,
headed by a property code. For the EBA's own sample file:

| Column | Property |
|---|---|
| `qCDF` | Name of entity — a typed dimension, hence a free-text value |
| `qBBE` | Location of activity |
| `ei1452` | Country where a service/activity is provided |

Both halves fail in ways worth telling apart. A datapoint id above the highest this
release has means the report was built against a newer one, which the answer says rather
than leaving an empty result to interpret. That is not hypothetical: those three ids
resolve to nothing in release 4.2.1, to nothing in 4.3, and in 4.4 to columns
`0040`, `0050` and `0060` of V_04.01, *Freedom to provide services*, in the
`AML_ELIGIBILITY` module - customers, incoming transactions, outgoing transactions.

An open table's key dimensions are the headers the model marks `IsKey`, and a report of
it carries exactly their property codes. V_04.01 is keyed on `qCDF`, `qBBE` and `ei1452`
— the three columns above — which `lookup_dpm_table` reports per header and
`explain_report` compares the report's columns against.

That comparison is the only check on a column that works. The first column of that sample
was read off a screenshot as `qGDF`, which resolves: *Name of Holding entity*, a real
property of the model, and the wrong one — the template's key is `qCDF`, *Name of
entity*. A header resolving to something proves nothing about whether it belongs to this
template, and only the comparison against the keys says so.

A header that resolves to nothing points at the release instead: a property code is
scoped to one, and the same property is `x21` through release 4.2 and `qx2013` after it.
And where the report has more rows than distinct datapoints, it has one row per record of
an open table, told apart by those dimension columns. Run `explain_report` before
`check_report` on any report whose provenance is not certain: one from another release
checks as "nothing mapped", which reads like a bad report rather than a newer file.

**The check, rather than an instruction not to guess.**

> Which rows add up to which in F_04.04.1 in FINREP9? Then check `report.csv` with
> `check_report` and tell me which rules failed and which could not be evaluated.

`lookup_dpm_sums` answers that row `0140` is rows `0010` and `0070` added together, over
12 columns, under rule `v23856_h` — the EBA's own rule, not arithmetic the model wrote.
`check_report` then runs every rule of that module version against the file:

```json
{{ "found": true, "table": "Y_01.01", "module": "PSD_FRP 1.1.0",
  "facts": 324, "mapped": 324, "unmapped": 0,
  "hold": ["v09124_m", "v09198_s", "v09247_s"],
  "fail": [{{"rule_code": "v09123_m", "severity": "warning", "fails": 12, "of": 12}}],
  "not_evaluated": [] }}
```

Read `not_evaluated` before `hold`: it is the checker's limit, not a pass — four of the
model's thirty-eight operators, each skipped rule named with the operator it needs. An
empty list, as here, is the claim that this module is covered completely. `unmapped` is
the next one to read: a large count almost always means the file is for another module
version rather than that the report is wrong.

Two phrases worth reusing in any of these: **"do not write any column name yourself"**,
and **"say which module version the answer is for"** — a rule changes both its expression
and its severity between versions, so a generated query should carry the version in a
comment.

### More than one release

`source/fetch_dpm2.py --release 4.3` fetches another release beside the first. Each lands
in its own files and its own database, because releases are separate downloads of
overlapping content and merging them would make "which release says this" unanswerable.
Point `DPM2_DB` at the one a lookup should read.

The default stays the release the pack is built from, so `check_against_dpm2.py` keeps
comparing like with like. What the others are for is a report that will not resolve:

| | 4.2.1 | 4.3 | 4.4 |
|---|---|---|---|
| Templates | 1052 | 1120 | — |
| Modules | 61 | 65 | — |
| Highest datapoint id | 1010000004 | 1010001382 | resolves the file above |

**An older module version is not restated.** Of the 145 module versions present in both
4.2.1 and 4.3, every one has exactly the same cell count, and of the 142 carrying rules,
every one has the same rule count. 4.3 adds releases and modules - `AML_RA`, `TCB_CORE`,
`TCB_HU`, `TCB_LIQUIDITY` - rather than revising what was there. So a description written
against a module version stays true as releases go by, and a figure that will not resolve
is a newer framework rather than a changed one.

### What the model has that the layout does not

Validation rules, nesting and every other framework. The first two are extracted into the
pack; the third is reachable through `dpm_lookup.py`, which reads the database directly
and so needs the download.

There are no member definitions to harvest. Of the {sum(len(m) for m in VOCAB["domains"].values())} controlled values this pack
documents, the DPM publishes a definition for **none** — the 1453 items that do carry one
belong to COREP, PILLAR3, MiCA and the rest. The definitions in this pack are the only
ones there are, which is also why they must not be invented.

## Validation rules

`09-validation-rules.csv` holds the {PAY_RULES} rules of PSD_FRP 1.1.0 and the
{DORA_RULES} of DORA 1.1.0, one row per rule and each cell it reaches:

| Field | |
|---|---|
| `module` | `PSD_FRP 1.1.0` or `DORA 1.1.0` |
| `rule_code`, `severity` | e.g. `v09123_m`, `warning` |
| `table_name`, `row_code`, `column_code`, `sheet_code` | the cell, in warehouse spelling; `*` is an open axis, empty is an axis the table does not have |
| `expression` | the rule in DPM-XL, verbatim |

Which cells a rule reaches is **not** parsed out of the expression. The model resolves
its own operands, in `OperandReferenceLocation`, and that is what the extraction reads —
so a rule is attached to a column because the EBA says it is, not because a regular
expression agreed. All 4635 rule-cell rows resolve to a datapoint this pack has.

A column description names the rules that reach it and stops there:

> ... Non-negative. Validation rules (EBA DPM, warning): v09123_m, v09124_m, v09247_s,
> v89551_h. v89551_h reaches only variant(s) 0030.

The expression is deliberately not in it. 93 of the {PAY_RULES} PAY expressions contain a plus
sign, which the OpenMetadata viewer renders as a literal `&amp;#43;` — the same reason the
build guard refuses one anywhere in this pack. The code is the handle: the EBA's own rule
lists are indexed by it, the CSV has the expression, and `lookup_datapoint` hands an agent
the whole thing under `validation_rules`.

A rule can reach only some of a column's six variants — 186 of the 845 PAY rule-column
pairs do — so the description says which, and a table that holds one variant does not
list a rule belonging to another.

### Reading a validation outcome

A validation report names a rule code and a failing cell and nothing else. `lookup_dpm_rule`
is the way back:

```bash
uv run agent_tools.py lookup_dpm_rule rule_code=v0174_m
```

```
COREP_OF   3.1.0   error    from 2023-06-30   cells 4
COREP_OF   4.0.0   error    from 2025-03-31   cells 4
COREP_OF   4.1.0   warning  from 2026-03-31   cells 4

{{r0070, c0010}} = the sum of {{r0080, c0010}}, {{r0090, c0010}} and {{r0091, c0010}}
on C_01.00
```

One row per module version, each with its own severity, the first submission date it
applies to, and the cells that version names — resolved by the model rather than parsed
out of the DPM-XL in `expression`. Which is the point of the next section.

`lookup_dpm_rules` goes the other way, from a template you are about to describe to every
rule that reaches it:

```bash
uv run agent_tools.py lookup_dpm_rules table=C_01.00 module=COREP_OF version=null
```

C_01.00 has 50 rules in COREP_OF 4.1.0 — 12 errors and 38 warnings — of which 23 reach
outside the template, and 4 more in **COREP_LE, a module C_01.00 is not part of at all**:
`v0655_m` multiplies row 0015 of C_01.00 by a column of C_28.00. Those cross-return
checks are the ones a reader is least likely to know about, which is why the template is
resolved without the module and why each rule lists every template it names.

### Taxonomy version and DPM version are different things

This is the conflation that costs the most, and the model's own column names invite it.
`ModuleVersion.VersionNumber` is the module's **taxonomy version** — FINREP9 3.3.0 — and
the **DPM version**, which is what a reporting institution usually means by "the
version", is the release the module version was introduced in:

| Module | Taxonomy version | DPM version | From | To |
|---|---|---|---|---|
| FINREP9 | 3.1.0 | 3.4 | 2022-12-31 | 2026-03-30 |
| FINREP9 | 3.2.0 | 4.0 | 2024-12-31 | 2024-12-31 |
| FINREP9 | 3.3.0 | 4.2 | 2026-03-31 | 2027-09-29 |
| FINREP9DP | 1.0.0 | 4.2 | 2026-03-31 | 2026-03-31 |
| FINREP9DP | 1.1.0 | 4.2.1 | 2026-03-31 | — |

Every lookup reports both, as `taxonomy_version` and `dpm_release`, and takes either:
`version` is the taxonomy one, `dpm_release` is the DPM one, and passing both is two
questions rather than one, so it is refused. Asking by release does the translation the
caller cannot: DPM 4.0 and 4.1 both resolve to FINREP9 3.2.0, DPM 4.2 onwards to 3.3.0.

**`FromReferenceDate` equal to `ToReferenceDate` means the module version is not to be
used.** It was published and superseded without ever covering a reporting period, so
nothing is filed under it — FINREP9 3.2.0 and FINREP9DP 1.0.0 above, and 43 of the 165
module versions in DPM 4.4. The answers mark it `do_not_use`, and resolving "the newest"
skips those, because a confident answer about a version no one files is worse than a
refusal.

### The rules change between releases, and the EBA publishes the patches

A DPM release is a snapshot. Between releases the EBA deactivates rules, reactivates them
and changes severities, and publishes each batch as a SQL script on its [validation rules
packages page](https://www.eba.europa.eu/risk-and-data-analysis/reporting/reporting-frameworks/validation-rules-packages).
The next DPM release absorbs them, so an older database is behind by every batch published
since:

```bash
uv run source/apply_vr_updates.py 'https://www.eba.europa.eu/.../DPM VR updates scripts.zip'
```

The batch of 2026-09-13 deactivates 81 rule scopes and reactivates 2. Against DPM 4.4 it
is a no-op — all 83 are already there. Against 4.2.1, 79 of them would change. Which is
the measure of what a release snapshot costs: a description written from 4.2.1 can name a
rule the EBA stopped running a year earlier.

The script is read and parsed, never executed. It arrives as SQL over the internet, and
handing that to a database is how a dictionary acquires a statement nobody read — only
`UPDATE OperationScope SET IsActive, Severity, FromSubmissionDate WHERE OperationScopeID
IN (...)` is recognised, and a file with anything else in it is refused rather than
partly applied. Without `--commit` it reports and changes nothing.

### The model as parquet, for a browser

```bash
uv run source/gen_wasm_data.py --dpm-release 4.4   # into web/public/data
```

Seven tables, pre-joined, answer every question the lookups answer — **3.05 MB for
everything DPM 4.4 ships**, in 67 files. Publishing the model's own tables instead would
be 71.6 MB, of which `ContextComposition` alone is 38.

Two things decide that, and neither is the codec. Sorting each table on the column its
questions filter by, with 50k row groups, took the dimension table from 7.58 MB to 3.26
MB — and the bytes a browser pulls for six questions from 32.9 MB to 8.3 MB, because
unsorted parquet statistics prune nothing. Splitting the three big tables by framework
takes it further: one question reads one partition. Seven questions against the published
tree pull **1.8 MB** in total, each answering in 4–17 ms.

Against those, the codec is noise — zstd 3.26 MB, zstd 22 3.14 MB, brotli 3.01 MB, gzip
3.25 MB, snappy 3.84 MB — so this writes zstd at level 22 and leaves brotli's extra 4%
alone rather than find out whether the WASM build reads it.

**What is stored decides more than how it is compressed.** Three changes took a release
from 3.06 MB to 1.62:

| | before | after |
|---|---:|---:|
| `cell_members`, COREP | 455 kB | 122 kB |
| `rule_cells`, COREP | 499 kB | 172 kB |
| `cells`, COREP | 184 kB | 138 kB |

The dimension table stored the datapoint id, which is unique per cell and therefore a
random int64 inside a (template, dimension, member) group: 336 kB of that 455, compressing
to nothing. It stores the row and column codes instead — short, sorted, and what the
answer shows anyway — and the id comes back from the join to `cells`. The rule-cell table
was sorted by template alone, leaving each rule's rows interleaved with every other
rule's; sorting within the rule clusters them. And the cell code is the three columns
beside it with punctuation, so it is composed where it is shown rather than stored.

### Publishing it

The EBA's legal notice says: *"Reproduction of all EBA material on this site is
authorised, provided the source is acknowledged, save where otherwise stated."* The DPM
database is on that site, neither its download pages nor the database itself states
otherwise, and the published tree is a reformatting of codes, labels and rules rather
than a copy of the database. So the condition is the acknowledgement, and it is carried
in three places rather than one: `NOTICE`, the `source_notice` field in every
`manifest.json`, and the footer of the page, because a published copy is read where this
repository is not.

Two things that are not about copyright. Release 4.4 is a **draft** technical package, so
anything built from it is a draft too — the generator takes `--draft`, the manifest
carries it, and the page says so when that release is picked, because a reader should not
have to open a NOTICE to learn that the EBA is still changing it. And this is a
reformatting, not the EBA's distribution: a reporting institution gets the database from
the EBA, and the page says that as well.

`.github/workflows/wasm-data.yml` publishes it, to
**<https://oluies.github.io/om-eba-annotatedtpl/>**. It stays manual rather than running
on push: each release is a 200 MB download and several minutes, and publishing is a
decision each time rather than a consequence of a commit. Untick *deploy* to build the
artefact and stop.

### Labels in another language

The DPM is English. Its `Translation` and `Language` tables are in the schema and ship
with 0 rows in every release, so there is nothing to read - but there is nothing to
translate either, because the templates are an annex to an Implementing Regulation and an
Implementing Regulation is published in all 24 official languages. The Swedish row labels
are already the legally published ones.

```bash
uv run source/fetch_its_labels.py --report                    # what is there, and what the model makes of it
uv run source/fetch_its_labels.py --variants --out source/its_labels.csv
```

EUR-Lex's web front end answers a scripted request with `202` and zero bytes; the
Publications Office's CELLAR service answers properly, with the language chosen by
content negotiation. Each language is about 20 MB of XHTML. English says which template a row belongs to —
the heading that announces one is typeset differently per language, and joining on
(template, row) per language loses a fifth of the coverage — and the other languages are
asked only what a row reads. They are matched to it by a sequence alignment over the row
codes rather than position for position: the 2021 text had the same 13 838 table rows in
every language, the 2024 consolidation does not, and two extra German rows refused the
whole document until the match absorbed them as an insertion. A row that pairs with
nothing is dropped rather than shifted onto its neighbour.

**Choosing a release.** The template pages are built with
[Observable Framework](https://observablehq.com/framework) and query the parquet in the
reader's browser, so the release is a control on the page: pick 4.3 and the cells, the
dimensions, the rules and their severities are 4.3's answer, asked again. They were Quarto
documents, which render once at build and so could only be a directory per release with a
link between them. The same mechanism gives the other thing a document could not — every
cell of a template, searchable, rendered as you scroll, where the document showed twelve
rows and pointed at a CSV.

Quarto still renders the same content as markdown, which is what goes into OpenMetadata.
A catalogue article is static text; a public page should not be.

**Which templates get a page.** The catalogue is built from the release named in
`templates_from`, but it is scoped to the releases actually being published: a template
withdrawn before the oldest of them answers "no reportable cells" under every release a
reader can choose. That was 37 of 349 pages - C_02.00, C_16.00.a, C_24.01, C_91 through
C_96 - each honest and each useless. 312 remain. The framework comes from the catalogue
too rather than being a control: no template of the 312 is filed under two frameworks, so
a free choice was one whose every setting but one produced an empty page.

**The page fetches each file; it does not let DuckDB read it.** httpfs reads a parquet over
HTTP ranges, and GitHub Pages serves these gzipped - the `content-length` is then the
compressed length while a byte range comes from the uncompressed file, so DuckDB reads the
footer where it was told the end is and answers `No magic bytes found at end of file`.
Which of the two variants the CDN holds decides whether it happens: the COREP pages passed
while every FINREP page lost its dimensions, and the query page showed a reader
`NetworkError: Failed to execute 'send' on 'XMLHttpRequest'`. Both pages now fetch each
file once, which decompresses it, and hand DuckDB the bytes. Anything else built over this
tree should do the same.

**DORA is in, with two of seven sections empty and saying so.** Its 15 register templates
are in the same model and the publish already wrote their partitions, so they cost nothing
but the catalogue entry. What they do not have is the Official Journal: the Swedish and
German labels and the instructions come from the supervisory reporting ITS, 2021/451, and
DORA's templates are an annex to 2024/2956 - a different regulation, not fetched. The
page says that rather than showing an empty table.

**An open table is not its cell count.** 14 of DORA's 15 templates and 66 of COREP's 159
are open: the reporter adds the rows, the columns or the sheets, so "4 reportable cells"
is the shape of one row and says nothing about how much is filed. B_02.01 is one row per
contractual arrangement, C_06.02 one per group entity, C_09.01.b one sheet per country.
The pages say so under the counts, from `Table.HasOpenRows` and its two siblings.

**A table is the content, not an illustration.** Observable's theme caps `p, table, figure`
at the prose measure, 640px, and ends what does not fit with an ellipsis - which showed
about fifteen characters of a row label and of each of the three languages, 157 of 550
cells clipped on one page. The prose keeps its measure and the tables get the column. Only
the narrow columns are given a width: under `table-layout: fixed` the rest share what is
left, so a table is exactly as wide as the page, where sizing every column made it wider
and pushed the last two off the edge.

The regulation's own versions are the opposite case and get no control. The four
consolidations of 2021/451 are two distinct texts, and they differ in 58 of 4 273
coordinates across 16 of 165 templates — a selector would show the same thing on 149 pages
out of 165, which teaches a reader that the choice never matters. Those 16 templates say
so inline instead, on the rows where the wording changed:

> **0510**
> `02021R0451-20210319` — (-) Amount exceeding the 17.65 **%** threshold
> `02021R0451-20230711` — (-) Amount exceeding the 17.65**%** threshold

```bash
uv run source/fetch_its_labels.py --changed --out source/its_label_changes.csv
```

**Which version of the regulation matters, and the default is not the obvious one.** The
bare CELEX `32021R0451` is the act *as adopted* — the 2021 text, five years behind the
releases it is matched against. A consolidated version is the act as amended up to a
date, and `--versions` lists them: `02021R0451-20210319`, `-20220303`, `-20230711`,
`-20240901`. The newest is the default, and the difference is not academic — 381
coordinates the original does not have, 57 rows worded differently, and agreement with
the model up a point. Every row carries the `celex` it came from, and the pages say so.

Measured against DPM 4.4, for the templates in force: **2 539 of 13 371 row labels have a
published translation at the same coordinate, and 2 387 of those agree on the English
text** as well. Within the 165 templates the parser reaches, **96 %** of the model's rows
are covered — the gap to the first figure is reach, not the Journal.

Two things the annexes do differently. COREP heads each template with its code
(`C 01.00 - OWN FUNDS (CA1)`). FINREP does not: Annex III opens with an index of template
number, code and name, and then heads each template with the number alone — `1.1 Assets`
for F 01.01. The index is read as the document goes past it, per annex, because the
numbers collide: `1` is C 01.00 in Annex I and `1.1` is F 01.01 in Annex III.

And a variant takes the grid of the template it varies. The Journal prints `C 75.01`
once; the model has `C_75.01.a` and `C_75.01.w`, the same grid reported under another
scope. `--variants` fills those in and marks them `stem` in the `from` column, which adds
**3 479 rows** with the model's English — the same rate as the direct
matches, which is what makes the fallback defensible rather than convenient. A numeric
suffix is not a variant: `F 04.02.1` and `F 04.02.2` have their own codes in the Journal's
own index.

#### What a row means, not only what it is called

`--instructions` reads the other half of the same document. The instructions annex gives
each row its meaning and the article that requires it, and it is published in every
language too:

> **C 01.00, row 0010** — *1. Own funds Point (118) of Article 4(1) and Article 72 CRR
> The own funds of an institution shall consist of the sum of its Tier 1 capital and
> Tier 2 capital.*
>
> *1. Kapitalbas Artikel 4.1.118 och artikel 72 i CRR Ett instituts kapitalbas ska
> utgöras av summan av primärkapital och supplementärkapital.*

```bash
uv run source/fetch_its_labels.py --instructions --out source/its_instructions.csv
```

1 040 rows across 51 templates, three languages — **and that is COREP**. Its instructions
annex is a two-column table of row code and prose, under a heading that carries the
template's code.

**FINREP's Annex V is a different kind of document**, and the yield says so: 37 rows
against COREP's 1 040. It is narrative guidance in numbered paragraphs, naming the item
it is about by quoting its label rather than by a code —

> 1. ‘Cash on hand’ shall include holdings of national and foreign banknotes in circulation.

— so a note is attached by matching that quoted term, exactly, inside one template. Of
708 numbered paragraphs, 246 quote an item at all and 37 survive both that match and the
alignment across languages. The other 671 are guidance about accounting treatment, which
belongs to no row. Each row says which it is in a `shape` column: `table` or `note`.

The alignment is a sequence match and not a key, because the paragraph numbers restart
under every heading. Keying on them paired an English paragraph about cash on hand with a
Swedish one about exposure classes — a wrong translation presented as a translation,
which is the one thing this must not produce. A test now pins that a note's three
languages carry the same paragraph number.

What this cannot give: dimension members, metrics and module names, which the DPM carries
and no annex does. And a code is never translated - `F_18.00.a`, `r0010`, `dp152217`,
`v0174_m` are identities, in every language.

#### Why not just run a translation model

Because holding the published translations makes that testable rather than arguable.
`source/score_translation.py` runs a local model over a sample and scores it against the
Journal's own wording. Against a 9 GB general model on one laptop, 25 labels:

| | exact |
|---|---|
| plain | 1 / 25 |
| with a 40-term glossary drawn from the official labels | 6 / 25 |

Six times better, and still wrong nineteen times. The failures are terminology, not
fluency: `Debt securities` came back as `Skuldsäkerheter`, which is fluent Swedish and is
not the term — the Journal says `Räntebärande värdepapper`. A better model writes better
Swedish; it does not know which Swedish the regulation uses. One run rendered `Level 1
collateral which is extremely high quality covered bonds` as `Säkerhet på nivå 1 **utom**
säkerställda obligation` — *utom* means "except", so the label was negated while reading
perfectly.

So a model is for this pack's own prose, and for a first draft of the vocabulary the
Journal does not carry, which a person then approves. It is not for the labels. The
labels are published.

### The page over it

```bash
uv run source/gen_wasm_data.py --dpm-release 4.4   # into web/public/data/4.4
cd web && ./build.sh --js-mode release             # public/main.js, 118 kB gzipped
python3 server.py public 8097                      # any static server that speaks byte ranges
```

Each release lands in its own directory and the page offers them, because releases are
separate answers to the same question rather than versions of one. Between what 4.2.1
published and what 4.4 does, **408 rules changed severity or activity**, 1738 rules are
new and 829 are gone: `v0491_m` is active under 4.2.1 and deactivated under 4.4, which
the page shows by switching the release and asking again. The release is in the URL, so
a shared answer stays the answer it was.

DuckDB 2.0 on this side of the wire; DuckDB-WASM in the browser stays at 1.29.0, because
there is no 2.0 of it — the newest published is 1.33.1-dev, and it is *bigger*: 7.1 MB
brotli against 6.2 MB for the pinned one, measured from the CDN. The databases in
`source/dpm2/` were written by 1.x and 2.0 reads them, which is what matters here: nothing
rebuilds them.

Scala.js and Laminar, no npm and no bundler: Scala.js emits ES modules and the browser
resolves the DuckDB-WASM import from the CDN itself. `web/src/dpm/DuckDb.scala` is the
facade — six calls, because no Scala.js facade for DuckDB-WASM exists.

The row cap is a control rather than a constant: a question that carries a `LIMIT` offers
*Rows*, starting at 200 and going to 5000, and the number travels in the URL with the
question, so a link worth sending because it has 900 rows arrives with 900. Visits are
counted by [GoatCounter](https://www.goatcounter.com/help/privacy) — no cookies, no
cross-site identifier, and the path is cut down by hand so what leaves the tab is which of
the eleven questions was opened, never a slot.

A question is a template and the slots a reader fills, never free SQL, and the answer
shows the statement that produced it. That is the same argument as everywhere else in
this pack: `F04041_r0070_c0015` looks exactly as plausible as a real cell code, so a page
that invites anyone — or any model — to write their own SQL over this schema invites the
mistake back in.

Eleven questions, which are data rather than code:

| | |
|---|---|
| Which cells does a template have? | the grid, with labels and datapoint ids |
| What does a template break down by? | dimensions and the exact wording of their members |
| Which cells make up an aggregate? | one dimension, one member — the hand-maintained spreadsheet, answered |
| Which rows add up to which? | from the rules, not from reading a grid |
| Which rules reach a template? | with the rows each names here, and how many templates it spans |
| What does a validation code mean? | per module version, with severity and whether it is still run |
| Which rules has the EBA switched off? | `active` is false: published and not run |
| What is this reported datapoint id? | `dp152217` back to its cell |
| What does a report's column header mean? | `qCDF` is *Name of entity*, and where it is a key |
| What are a template's key dimensions? | the columns a report of an open table carries |
| Which module versions…? | taxonomy version, DPM version, and `do_not_use` |

The slots offer what is there. Framework, template, module, dimension and member each
come with a list read out of the published data, and each one narrows the next: 21
frameworks, 153 templates in FINREP, nine dimensions on F_04.04.1, six members of
*Counterparty sector*. That is the near miss turned into a list — the member is
"Financial corporations other than credit institutions", and nobody was going to type
that from memory. The fields stay typeable, because a code pasted out of a report should
go straight in whether or not it is on the list, and the lists are filled when a field is
first reached for rather than on load, since filling them needs the engine.

The question and its slots live in the URL, so an answer can be sent to someone. A table
that stops at its limit says so, because one that does not reads as the whole answer.

Behind a fold, because it costs a download: a small model (SmolLM2 360M, ~376 MB, or
Qwen2.5 in 0.5B and 1.5B) loaded with WebLLM only when someone asks for it. **It never
writes SQL.** Its whole job is to pick one of the eleven questions and fill in its slots,
and the page then runs that question's own statement:

```json
{{"question": "sums", "slots": {{"table": "F_12.01.a", "module": "FINREP9"}}}}
```

That is the same argument as the rest of the pack, applied to the model: a 360M model can
choose among eleven questions, and it cannot write correct SQL over a schema where a
plausible-looking cell code is wrong and a near miss in a dimension's wording matches
nothing. What it chose is shown before the answer, so a wrong reading is visible rather
than silent, and a question id or slot name it invents is refused rather than rounded to
the nearest one.

It asks in two steps — which question, then that question's slots — because one grammar
cannot say "these slots, for that question": the schema is fixed before the model
answers, so a single call let 0.5B pick the rule question and fill in `framework` and
`table`, which the catalogue then had to refuse.

Run against Safari, which has the WebGPU that a headless Chromium does not:

| asked in these words | SmolLM2 360M | Qwen2.5 0.5B |
|---|---|---|
| what does v0174_m mean? | the rule, 1 row | the rule, 1 row |
| which rows add up to which in F 12.01.a under FINREP9? | the sums, 6 rows | the sums, 6 rows |
| what does a report column called qCDF mean? | the property, 6 rows | — |
| which cells of F_04.04.1 are credit institutions…? | the whole grid, wrong | the whole grid, wrong |
| which rules are deactivated in COREP_OF? | every rule on a template, wrong | the module versions, wrong |

So: a convenience with a visible failure mode, not a replacement for the list above it.
Both models needed the same two things to get the first three right — the two steps, and
`hints` on each question, which are the words someone might actually use. Without the
hints both read "which rows add up to which" as the rules question, because both are
about rules and a template and the id `sums` says nothing on its own.

### What is cached, and what is not

Measured rather than assumed. With `Cache-Control: max-age=600` — what GitHub Pages sends
— a second visit refetched every range, and within one session each question re-read the
files it named. So the five small tables (modules, rules, sums, headers, properties, 450
kB together) are read into the engine once per release, and the questions that use them
pull **nothing** over the wire afterwards. Once, and shared: the first version remembered
the finished connection rather than the work in flight, so every keystroke in a slot —
each one asks for the connection to fill its list — started another read of all five.
That was 3.7 MB of the 5.2 a session cost, with `headers.parquet` read nine times. The partitioned tables stay on HTTP: they are
per framework, only the needed one is ever touched, and copying them into OPFS by hand
would buy less than it costs to keep correct across a release switch.

### Asking in your own words

Without WebGPU the page says so and the questions keep working — which is most of why
they exist. Checking `navigator.gpu` is not enough: Chromium exposes the object and then
returns null from `requestAdapter()` when there is no GPU to drive, so the page asks for
the adapter before sending anyone to fetch 376 MB that cannot run.
Measured in a browser: eleven questions, 15–46 ms each, 4.0 MB pulled in total including
the page itself.

### A rule code is not one rule

The same code is re-issued per module version, and both the expression and the severity
change between them. `v09247_s` is a `warning` in PSD_FRP 1.1.0 and an `error` in 1.2.0.
`09-validation-rules.csv` is scoped to the two module versions this pack describes;
`lookup_dpm_cell` is not, and returns one entry per version with the versions listed, so
two entries with the same code there are a change, not a duplicate.

## Environment

Exactly one variable is required: `OM_JWT_TOKEN`. Everything else has a default that is
right for a local checkout, so nothing has to be configured to run the generators, the
tests or a lookup.

### `OM_*` — OpenMetadata

Read by `describe_table.py` and `import_to_openmetadata.py`.

| Variable | What it is | Default |
|---|---|---|
| `OM_JWT_TOKEN` | Bearer token. **The one required variable.** | — |
| `OM_HOST` | API root. The `/api` suffix is part of it | `http://localhost:8585/api` |
| `OM_CA_BUNDLE` | Path to a CA bundle for TLS verification | the system store |
| `OM_PAGE_URL` | Format string with `{{name}}` where a Context Center article's name goes. Unset means the article is named in prose rather than linked, because the Context Center route changed between versions and is not documented — copy it out of the browser once | unset |
| `OM_GLOSSARY` | Which glossary root the importer writes to | `PAY_4_2` |

### `BA_*` — the warehouse

Read by `ba_form_cell.py`, the overlay that answers what a physical column actually carries.

| Variable | What it is | Default |
|---|---|---|
| `BA_SERVER` | SQL Server host. **Unset is not an error**: the warehouse is simply not consulted, and the answer says so rather than going quiet | unset |
| `BA_DATABASE` | Database | `FIDW_BI` |
| `BA_TABLE`, `BA_AXIS_TABLE` | The cell table and the axis table, joined on `Cell_sk` | `dbo.BA_Form_Cell`, `dbo.BA_Form_Axis` |
| `BA_TRUSTED_CONNECTION` | Kerberos. Set `false` to use the two below | `true` |
| `BA_USERNAME`, `BA_PASSWORD` | SQL login, only when `BA_TRUSTED_CONNECTION=false` | unset |
| `BA_DRIVER` | ODBC driver name | `ODBC Driver 18 for SQL Server` |
| `BA_ENCRYPT`, `BA_TRUST_SERVER_CERTIFICATE` | TLS on, and whether to accept a self-signed certificate | `true`, `false` |
| `BA_DEBUG` | Log the statement that ran with its parameters filled in, ready to paste into SSMS | `false` |

### `PAY42_*` — this pack's DuckDB store

| Variable | What it is | Default |
|---|---|---|
| `PAY42_DB` | The store | `pay42.duckdb` |
| `PAY42_TEMP_DIR` | Where DuckDB spills. **The one that matters in anger**: left alone it writes scratch files next to the database, so a read-only mount holding the store has nowhere to go | beside the database |
| `PAY42_EXTENSION_DIR` | Extension directory | DuckDB's own |
| `PAY42_MEMORY_LIMIT` | e.g. `2GB` | unlimited |

### `MSSQL_*` — loading the dictionary into SQL Server

Read by `source/load_to_mssql.py`. Kerberos by default, so with `MSSQL_SERVER` set and a
`kinit` ticket there is nothing else to configure and no password to keep.

| Variable | What it is | Default |
|---|---|---|
| `MSSQL_SERVER` | Host. No default: there is nothing sensible to guess | — |
| `MSSQL_PORT` | | `1433` |
| `MSSQL_DATABASE` | The target database, which must already exist | `DPM2` |
| `MSSQL_SCHEMA` | The target schema, created if absent. Also accepted as `MSSQL_DB_SCHEMA`, because the field cannot be called `schema` — Pydantic has that name | `dpm` |
| `MSSQL_TRUSTED_CONNECTION` | Kerberos. `Trusted_Connection=yes` resolves to `authenticator=krb5` on POSIX. Set `false` to use the two below | `true` |
| `MSSQL_USERNAME`, `MSSQL_PASSWORD` | A SQL login; both are required once the trusted connection is off | unset |
| `MSSQL_ENCRYPT`, `MSSQL_TRUST_SERVER_CERTIFICATE` | TLS on, and whether to accept a self-signed certificate | `true`, `false` |

So the default target is `DPM2.dpm`. The T-SQL in
[`README_DPM2.md`](README_DPM2.md) writes that schema literally, as `dpm.RuleSum` and
`dpm.Operation`; point `MSSQL_SCHEMA` somewhere else and those queries need the same
rename.

### `DPM2_*` — the DPM 2.0 database

| Variable | What it is | Default |
|---|---|---|
| `DPM2_DIR` | The download directory: the zip, the Access file and the DuckDB database | `source/dpm2/` |
| `DPM2_DB` | The database file alone. It wins over the release being fetched, so a second release wants it unset on the way in and set on the way out | `dpm2.duckdb` inside `DPM2_DIR`, and `dpm2_4_3.duckdb` for a release that is not the default |

### Seeing what is actually set

```bash
source env.sh                     # .env, then the defaults, then the report
source env.sh --release 4.4       # point DPM2_DB at another release's database
source env.sh --quiet             # set without the report; `pack_env` prints it later
source env.sh --env-file other.env   # read that instead of ./.env
source env.sh --no-env-file          # ignore it
```

It reads `.env` first, then fills in what has a safe local default - the two stores and
the download directory. The precedence is pydantic-settings' own: **the environment wins
over `.env`, and `.env` wins over the defaults here**, so exporting a variable for one
command still overrides the file, and a release pinned for one shell stays pinned. This
is also what closes the gap the next section describes: `DPM2_*` is read with `os.environ`
and never reaches pydantic-settings, so until now a `.env` could not pin it.

The file is read, never executed. `source .env` runs whatever is in it, and a file holding
a password is the last one to hand a shell, so this parses `NAME=VALUE` only: `export` is
allowed, comments and blanks skipped, one pair of surrounding quotes removed, and nothing
expanded - `$HOME` in a value stays the five characters it is. Secrets and hostnames are
still never *assigned* by the script itself: a committed file that sets `OM_JWT_TOKEN` is
a committed file that leaks it, and a default SQL Server host is a wrong host.

The report names every variable the pack reads, marks the ones this run took from the
file with `(.env)`, says whether each path exists, counts a secret rather than printing
it, and for `DPM2_DB` opens the database to say which releases it contains and what its
highest datapoint id is:

```
DPM2_DB    .../source/dpm2/dpm2_4_4.duckdb  [158M]
           releases 3.4, 3.5, 4.0, 4.1, 4.2, 4.2.1, 4.2.1.1, 4.2.1.2, 4.3, 4.3.0.1, 4.4;
           highest datapoint id 1010005111
```

That last line is the one worth having. No variable says which release a file holds, and
a datapoint that will not resolve is almost always a database older than the report.

### A `.env` file does not cover all of them

`OM_*`, `BA_*` and `PAY42_*` as the lookup reads them go through pydantic-settings, which
reads `.env`. `DPM2_*` everywhere, and `PAY42_DB` and `PAY42_TEMP_DIR` as
`source/build_duckdb.py` reads them, use `os.environ` and do not.

So a `PAY42_DB` in `.env` steers where a lookup reads but not where the build writes: you
can build one file and read another with nothing complaining, and `DPM2_*` in `.env` does
nothing at all — to the tools. `source env.sh` is the way round it: it reads the file
itself and exports what it finds, so one `.env` then governs every variable here.

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

# What the guard is for is text that reaches the OpenMetadata viewer, and the importer
# names the files it publishes rather than globbing the repository. README_DPM2.md is not
# among them: it documents the local DuckDB copy of the DPM database, for someone writing
# SQL against it, and it is never imported anywhere.
#
# Scoping this was not cosmetic. A section on how validation rules add up cannot be
# written without a plus sign - the operator is the subject - so an unscoped guard made a
# correct document impossible to generate.
_NOT_IMPORTED = {"README_DPM2.md"}

# The same scoping, by directory: `source`, `obs` and `web` hold code. `obs/src/t/[code].md`
# is an Observable page - JavaScript in a markdown file, never imported - and the regex in
# it that keeps a file name safe cannot be written without a plus.
_NOT_IMPORTED_FROM = {"source", "obs", "web"}

_GUARDED = [
    p for p in sorted(OUT.rglob("*.md")) if not (_NOT_IMPORTED_FROM & set(p.parts)) and p.name not in _NOT_IMPORTED
]
_problems = [
    f"{path.relative_to(OUT)}:{n}: {reason}\n    {line.strip()[:100]}"
    for path in _GUARDED
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
    for char, reason in _OFFENDERS.items()
    if char in line
]
if _problems:
    raise SystemExit("Characters that do not survive the OpenMetadata viewer:\n  " + "\n  ".join(_problems))
print(f"guard: no offending characters in {len(_GUARDED)} markdown files that reach OpenMetadata")
