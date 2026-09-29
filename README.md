# om-eba-annotatedtpl

The EBA **PAY 4.2 (FRPPAY 4.2)** annotated table layout — payment and fraud reporting
under PSD2 — normalised from a 55-sheet spreadsheet into documentation an agent can use
when describing tables, columns and glossary terms in OpenMetadata.

**1830 datapoints, 14 templates, 14 dimensions over 4 domains, 54 controlled values.**

![The pack loaded as Knowledge Pages in OpenMetadata](docs/knowledge-pages.png)

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
export OM_HOST=http://localhost:8585/api OM_JWT_TOKEN=...
uv run import_to_openmetadata.py --dry-run     # print the page tree, contact nothing
uv run import_to_openmetadata.py               # write 22 Knowledge Pages, dry run the glossary
uv run import_to_openmetadata.py --commit      # ... and write the glossary terms
```

`OM_HOST` must include `/api` - OpenMetadata serves its API under `/api/v1/...`. The
script preflights the base URL, the server version and the Knowledge Page endpoint, and
fails with a diagnosis instead of an opaque 405.

Pages land under an `EBA` root, so a later framework can be loaded beside this one:

    EBA
    └── PAY 4.2 (FRPPAY 4.2)
        ├── Framework
        ├── Agent instructions
        ├── Glossary      (dimensions, domains and members, metrics)
        └── Templates     (one page per template)

### Pages written but missing from the list

The UI lists pages through `/search/hierarchy`, which reads the search index, while the
write goes to the database. Indexing is asynchronous, so a fresh import can be invisible
in every list view. The importer reindexes the ids it wrote; `--verify` shows the two
counts side by side, and `--no-reindex` skips the call.

    uv run import_to_openmetadata.py --verify

## Licence

The code is MIT (see `LICENSE`). The PAY 4.2 content - codes, labels, datapoint ids,
structure and the source workbook - is EBA material, reproduced under the EBA legal
notice, which authorises reproduction provided the source is acknowledged. That is a
permission with an attribution condition, not a named open licence, and the MIT licence
does not extend to it. See `NOTICE`.

Not affiliated with or endorsed by the EBA.

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
| `05-datapoints.csv` | All 1830 datapoints, keyed by warehouse `column_name` and datapoint id | You have a column to describe |
| `06-openmetadata-glossary.csv` | Bulk glossary import | You are loading the glossary |

## Loading the glossary

The CSV holds glossary **terms only** - it populates a glossary, it does not create
one. `import_to_openmetadata.py` creates it if missing. To do it by hand:

```bash
AUTH="Authorization: Bearer $OM_JWT_TOKEN"

# 1. create the glossary (the CSV import only creates terms inside it)
curl -X POST "$OM_HOST/v1/glossaries" -H "$AUTH" -H 'Content-Type: application/json' -d '{"name": "PAY_4_2", "displayName": "PAY 4.2 (FRPPAY 4.2)", "description": "..."}'

# 2. dry run the terms, read the response, then re-run with dryRun=false
curl -X PUT "$OM_HOST/v1/glossaries/name/PAY_4_2/import?dryRun=true" -H "$AUTH" -H 'Content-Type: text/plain' --data-binary @06-openmetadata-glossary.csv
```

The header is taken from `json/data/glossary/glossaryCsvDocumentation.json` in the
OpenMetadata source: `parent, name*, displayName, description, synonyms, relatedTerms,
references, tags, reviewers, owner, glossaryStatus, color, iconURL, domains, extension`.

**Check that against your own instance** - the columns change between versions.
`GET /v1/glossaries/documentation/csv` returns the header your server expects. Always
run with `dryRun=true` first and read the response.

An empty `parent` puts a term directly under the glossary. `glossaryStatus` takes
`Draft`, `Approved` or `Deprecated`.

### `Entity not found: glossaryTerm <uuid>`

A half-finished import can leave the glossary pointing at a term that no longer
resolves - the import looks terms up excluding soft-deleted ones, so a soft-deleted
term reads as missing and the whole import 404s. Clear it out and rebuild:

    uv run import_to_openmetadata.py --glossary-only --reset-glossary

That hard-deletes the glossary and everything under it, so only use it on a glossary
this pack owns.

The glossary is named `PAY_4_2`, not `PAY 4.2`, and carries the readable form in its
displayName. OpenMetadata quotes any FQN part containing a dot, so a glossary called
`PAY 4.2` is addressed as `"PAY 4.2".Domains`; a parent column written `PAY 4.2.Domains`
then matches nothing and every child row fails with `Entity ... not found`.

Terms are created as `Draft` except the three grouping terms. Promote them once a domain
expert has checked the definitions: the descriptions here are structural - they say where
a term is used, not what it legally means.

`Payment related parties` appears twice, once as a domain and once as a dimension. That
is deliberate - dimension `qKKL` carries the same label as its domain `qRP` - and the two
have different parents, so the FQNs do not collide.

## Warehouse column names

One table per template - `Y_01.01` lands in `Y_01_01` - with datapoint columns named
`Y0101_r0010_c0010`: template with its separators stripped, then row and column code.
`05-datapoints.csv` is keyed by both, as its first two fields.

Everything that does not match `^[A-Za-z][0-9]4_r[0-9]4_c[0-9]4$` is warehouse context
(`Period_SK`, `Company_BK`, `Taxonomy_Name`, ...) and has no framework meaning.

The name carries no variant, so 302 of the 320 distinct names map to six datapoints each
(two metrics x three geographies); the 18 from the `.02` loss templates map to one. The
variant is a property of the table, not the column. `02-agent-instructions.md` has the
worked example.

![An article page](docs/agent-instructions-page.png)

## The one thing to get right

Row code `0010` and column code `0010` exist in every template and mean something
different in each. Only the numeric **datapoint id** is unique on its own. Resolve to a
datapoint id before writing any description.
