# om-eba-annotatedtpl

The EBA **PAY 4.2 (FRPPAY 4.2)** annotated table layout — payment and fraud reporting
under PSD2 — normalised from a 55-sheet spreadsheet into documentation an agent can use
when describing tables, columns and glossary terms in OpenMetadata.

**1830 datapoints, 14 templates, 14 dimensions over 4 domains, 54 controlled values.**

## Reproducing

```bash
uv sync
uv run source/extract_dpm.py    # xlsx  -> source/dpm.json      (structure)
uv run source/vocab.py          # dpm   -> source/vocab.json    (vocabulary)
uv run source/gen_pack.py       # both  -> the markdown and CSV in this repo
```

The spreadsheet is built on merged-cell blocks: the row axis sits to the right of the
data columns, the column axis in a footer block, and the sheet axis in the header. The
merge *spans* are what identify where each block starts and ends, which is why the
extraction uses openpyxl — a plain cell reader gives you the values but not the geometry.

## Importing into OpenMetadata

```bash
export OM_HOST=http://localhost:8585/api OM_JWT_TOKEN=...
uv run import_to_openmetadata.py --dry-run     # print the page tree, contact nothing
uv run import_to_openmetadata.py               # write 22 Knowledge Pages, dry run the glossary
uv run import_to_openmetadata.py --commit      # ... and write the glossary terms
```

Markdown goes to Knowledge Pages (`PUT /v1/contextCenter/pages`); the vocabulary goes to
the glossary CSV import. There is no bulk file upload and no document library —
`docStore/document.json` is a generic JSON payload store the UI uses for persona layouts.

`--commit` always dry runs first and refuses to write if that comes back with anything
other than `success` and zero rejected rows.

---

# PAY 4.2 documentation pack for OpenMetadata

Reference material for describing assets derived from the EBA **PAY 4.2 (FRPPAY 4.2)**
payment and fraud reporting framework under PSD2, written to be read by an agent that
writes table, column and glossary descriptions.

Generated from `EBA PAY 4.2 (FRPPAY 4.2) annotated table layout, 2026-01-06`.

## Files

| File | What it is | Read it when |
|---|---|---|
| `01-framework.md` | What PAY 4.2 is, the 14 templates, the shape of the data | You need orientation |
| `02-agent-instructions.md` | How to decode an identifier and write a description | **Start here** |
| `03-glossary/domains-and-members.md` | The 54 controlled values across 4 domains | You need the vocabulary |
| `03-glossary/dimensions.md` | The 14 breakdown axes | You need to know which axis a value belongs to |
| `03-glossary/metrics.md` | The 3 metrics and their units | You need the unit |
| `04-tables/<TEMPLATE>.md` | One per template: variants, columns, rows, datapoint ids, ready-to-paste descriptions | You are describing a table |
| `05-datapoints.csv` | All 1830 datapoints, one row each, fully resolved | You have a datapoint id |
| `06-openmetadata-glossary.csv` | Bulk glossary import | You are loading the glossary |

## Loading the glossary

The CSV holds glossary **terms only**. Create the glossary itself first, then import:

```bash
AUTH="Authorization: Bearer $OM_JWT_TOKEN"

# 1. create the glossary (the CSV import only creates terms inside it)
curl -X POST "$OM_HOST/v1/glossaries" -H "$AUTH" -H 'Content-Type: application/json' -d '{"name": "PAY 4.2", "displayName": "PAY 4.2 (FRPPAY 4.2)"}'

# 2. dry run the terms, read the response, then re-run with dryRun=false
curl -X PUT "$OM_HOST/v1/glossaries/name/PAY%204.2/import?dryRun=true" -H "$AUTH" -H 'Content-Type: text/plain' --data-binary @06-openmetadata-glossary.csv
```

The header is taken from `json/data/glossary/glossaryCsvDocumentation.json` in the
OpenMetadata source: `parent, name*, displayName, description, synonyms, relatedTerms,
references, tags, reviewers, owner, glossaryStatus, color, iconURL, domains, extension`.

**Check that against your own instance** - the columns change between versions.
`GET /v1/glossaries/documentation/csv` returns the header your server expects. Always
run with `dryRun=true` first and read the response.

An empty `parent` puts a term directly under the glossary. `glossaryStatus` takes
`Draft`, `Approved` or `Deprecated`.

Terms are created as `Draft` except the three grouping terms. Promote them once a domain
expert has checked the definitions: the descriptions here are structural - they say where
a term is used, not what it legally means.

`Payment related parties` appears twice, once as a domain and once as a dimension. That
is deliberate - dimension `qKKL` carries the same label as its domain `qRP` - and the two
have different parents, so the FQNs do not collide.

## The one thing to get right

Row code `0010` and column code `0010` exist in every template and mean something
different in each. Only the numeric **datapoint id** is unique on its own. Resolve to a
datapoint id before writing any description.
