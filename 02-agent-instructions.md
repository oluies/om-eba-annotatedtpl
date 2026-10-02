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
  wording. Where a precise definition is needed, cite EBA Guidelines on fraud reporting under PSD2 (EBA/GL/2018/05, as amended) rather than paraphrasing.
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

Use the name-keyed path instead. **A column is its own entity**, addressable by FQN:

```text
GET /v1/columns/name/{fqn}?entityType=table    read one column
PUT /v1/columns/name/{fqn}?entityType=table    set description and tags together
```

The body is an `UpdateColumn`: omit `tags` and the existing ones are left alone, and the
server validates every term against the glossary, so a bad term is a 404 rather than a
silent miss.

```json
{"description": "...", "tags": [{"tagFQN": "PAY_4_2.Domains....", "source": "Glossary"}]}
```

**PATCH against a column answers 405** - verified against a live server, and the resource
carries no `@PATCH` in the source. Documentation showing a JSON patch against a column
entity does not apply to this version. The entity type is `tableColumn`, not `column`.

The table CSV export and import also work, keyed by `column.name`:

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

The **article** is named in the table description, and linked when `OM_PAGE_URL` is set:

```bash
OM_PAGE_URL='https://your-host/contextCenter/articles/{name}' uv run describe_table.py ... --commit
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

`terms` left null leaves the existing glossary terms alone; an empty list clears them.
Every term is validated against the glossary, so a term that does not exist fails the
whole write with a 404 - set the description alone if the glossary is not loaded yet.

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

Nothing in `dispatch` raises. A tool that fails returns `{"error": ...}`, which the
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
403 Principal: CatalogPrincipal{name='mcpapplicationbot'} operation EditDisplayName
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
