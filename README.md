# om-eba-annotatedtpl

The EBA **PAY 4.2 (FRPPAY 4.2)** annotated table layout — payment and fraud reporting
under PSD2 — normalised from a 55-sheet spreadsheet into documentation an agent can use
when describing tables, columns and glossary terms in OpenMetadata.

**1830 datapoints · 14 templates · 14 dimensions over
4 domains · 54 controlled values.**

![The pack loaded as Knowledge Pages in OpenMetadata](docs/knowledge-pages.png)

## What is in here

| File | What it is | Read it when |
|---|---|---|
| `01-framework.md` | What PAY 4.2 is, the 14 templates, the shape of the data | You need orientation |
| `02-agent-instructions.md` | How to decode an identifier and write a description | **Start here** |
| `07-agent-prompt.md` | The stanza to paste into an agent's system prompt, covering every framework | You are configuring an agent |
| `describe_table.py` | Writes descriptions and glossary terms onto a table's columns, by name | You are describing a real table |
| `pay42_lookup.py` | Deterministic datapoint lookup over DuckDB, and its tool definition | You are giving an agent a lookup tool |
| `agent_tools.py` | All six tool definitions and one dispatcher | You are wiring the tools into an agent |
| `dpm_lookup.py` | Lookup over the whole DPM 2.0 database, for frameworks this pack does not cover | A warehouse table is COREP, FINREP or anything but PAY and DORA |
| `display_names.py` | The rule for what a table and its columns are called | You are setting display names |
| `08-lookup-tool.md` | How to register and dispatch that tool | You are wiring it into an agent |
| `03-glossary/domains-and-members.md` | The 54 controlled values across 4 domains | You need the vocabulary |
| `03-glossary/dimensions.md` | The 14 breakdown axes | You need to know which axis a value belongs to |
| `03-glossary/metrics.md` | The 3 metrics and their units | You need the unit |
| `04-tables/<TEMPLATE>.md` | One per template: variants, columns, rows, datapoint ids | You are describing a table |
| `05-datapoints.csv` | All 1830 datapoints, keyed by `table_name` and `column_name` | You have a column to describe |
| `06-openmetadata-glossary.csv` | Bulk glossary import, 93 terms | You are loading the glossary |
| `09-validation-rules.csv` | The 185 EBA validation rules of both modules, and every cell each one reaches | You want to know what constrains a column |
| `README_DPM2.md` | The DPM 2.0 database's data model, as diagrams, with worked queries | You are querying the model directly |

## Warehouse column names

One table per template — `Y_01.01` lands in `Y_01_01` — with datapoint columns named
`Y0101_r0010_c0010`: template with its separators stripped, then row and column code.
`05-datapoints.csv` is keyed by both, as its first two fields.

Everything that does not match `^[A-Za-z][0-9]{4}_r[0-9]{4}_c[0-9]{4}$` is warehouse
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
[the DPM data dictionary](https://www.eba.europa.eu/risk-and-data-analysis/reporting/dpm-data-dictionary). 167 MB of zip, 539 MB of Access, 139 MB of
DuckDB, all under `source/dpm2/` and all gitignored. Reading the Access file needs
`mdbtools` 1.0 or newer — the file is ACE12, and older releases read only Jet `.mdb`.

`check_against_dpm2.py` is the one check this pack cannot do on itself. It matches every
pack datapoint against the module's reportable cells, both directions, and exits non-zero
on a difference:

```
DPM 2.0 release 4.2.1 (2026-02-15)
PSD_FRP 1.1.0: all 1830 pack rows match the model, none missing
DORA 1.1.0: all 85 pack rows match the model, none missing
```

Two details it has to absorb. The DPM writes a table code `Y_01.01` where the layout and
the warehouse write `Y 01.01`. And a cell with `IsExcluded` set is a greyed-out box in
the template — in the model, not reportable — which the pack leaves out, so the
comparison does too. `Y_01.01` has 396 cells, 72 of them excluded, and the pack has 324.

### What the model has that the layout does not

Validation rules, nesting and every other framework. The first two are extracted into the
pack; the third is reachable through `dpm_lookup.py`, which reads the database directly
and so needs the download.

There are no member definitions to harvest. Of the 54 controlled values this pack
documents, the DPM publishes a definition for **none** — the 1453 items that do carry one
belong to COREP, PILLAR3, MiCA and the rest. The definitions in this pack are the only
ones there are, which is also why they must not be invented.

## Validation rules

`09-validation-rules.csv` holds the 114 rules of PSD_FRP 1.1.0 and the
71 of DORA 1.1.0, one row per rule and each cell it reaches:

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

The expression is deliberately not in it. 93 of the 114 PAY expressions contain a plus
sign, which the OpenMetadata viewer renders as a literal `&amp;#43;` — the same reason the
build guard refuses one anywhere in this pack. The code is the handle: the EBA's own rule
lists are indexed by it, the CSV has the expression, and `lookup_datapoint` hands an agent
the whole thing under `validation_rules`.

A rule can reach only some of a column's six variants — 186 of the 845 PAY rule-column
pairs do — so the description says which, and a table that holds one variant does not
list a rule belonging to another.

### A rule code is not one rule

The same code is re-issued per module version, and both the expression and the severity
change between them. `v09247_s` is a `warning` in PSD_FRP 1.1.0 and an `error` in 1.2.0.
`09-validation-rules.csv` is scoped to the two module versions this pack describes;
`lookup_dpm_cell` is not, and returns one entry per version with the versions listed, so
two entries with the same code there are a change, not a duplicate.

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

curl -X POST "$OM_HOST/v1/glossaries" -H "$AUTH" -H 'Content-Type: application/json' -d '{"name": "PAY_4_2", "displayName": "PAY 4.2 (FRPPAY 4.2)", "description": "..."}'

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
