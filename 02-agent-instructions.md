# How to describe PAY 4.2 assets in OpenMetadata

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
^(?P<prefix>[A-Za-z]{1,})(?P<major>[0-9]{2})(?P<minor>[0-9]{2})_r(?P<row>[0-9]{4})_c(?P<col>[0-9]{4})$
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
| 3264309 | 0010 | Amount of payment | Domestic | €£$ |
| 3260072 | 0020 | Number of transactions | Domestic | # |
| 3260968 | 0030 | Amount of payment | European Economic Area (EEA) | €£$ |
| 3263386 | 0040 | Number of transactions | European Economic Area (EEA) | # |
| 3260980 | 0050 | Amount of payment | Non-European Economic Area (EEA) | €£$ |
| 3263397 | 0060 | Number of transactions | Non-European Economic Area (EEA) | # |

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
   saying how to settle it from the warehouse rather than by asking: count the datapoint
   columns on the table. One variant's worth means the loader picked one and only the
   pipeline knows which.
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
  wording. Where a precise definition is needed, cite EBA Guidelines on fraud reporting under PSD2 (EBA/GL/2018/05, as amended) rather than paraphrasing.
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
  {"op": "replace", "path": "/description", "value": "Credit transfers transactions..."},
  {"op": "replace", "path": "/columns/20/description", "value": "Amount of credit..."},
  {"op": "replace", "path": "/columns/21/description", "value": "Amount of credit..."}
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

    GET /v1/tables/name/{fqn}/export           text/plain CSV of the current columns
    PUT /v1/tables/name/{fqn}/import?dryRun=   the same CSV back

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
[{"op": "replace", "path": "/description", "value": "Credit transfers transactions..."}]
```

### Linking the glossary

A column can carry the matching glossary term instead of repeating its definition:

```json
[{"op": "add", "path": "/columns/20/tags/-", "value": {
    "tagFQN": "PAY_4_2.Domains.Payment transaction characteristics.Credit transfers",
    "source": "Glossary", "labelType": "Manual", "state": "Suggested"}}]
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
    ├── Dimensions (14, each drawing values from one domain)
    └── Metrics (3)

Several dimensions share a domain, so a member code alone does not identify a dimension.
`Form of payment` and `Type of authentication` both draw on domain `qPY`. Resolve the
dimension from the datapoint row, never from the member code.
