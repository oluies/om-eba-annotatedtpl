# How to describe PAY 4.2 assets in OpenMetadata

Instructions for an agent writing table, column and glossary descriptions for assets
derived from the EBA PAY 4.2 (FRPPAY 4.2) reporting framework.

## Anatomy of an identifier

A fully qualified datapoint has four parts. Physical table and column names usually
encode some of them:

    Y_03.01 ( 0010 )      R0080          C0020            437613
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

**Datapoint columns** match `^[A-Za-z][0-9]4_r[0-9]4_c[0-9]4$` - for example
`Y0101_r0010_c0010`. These are the reported figures and the ones this pack describes.
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
| 437810 | 0010 | Amount of payment | Domestic | €£$ |
| 436590 | 0020 | Number of transactions | Domestic | # |
| 437768 | 0030 | Amount of payment | European Economic Area (EEA) | €£$ |
| 436548 | 0040 | Number of transactions | European Economic Area (EEA) | # |
| 437789 | 0050 | Amount of payment | Non-European Economic Area (EEA) | €£$ |
| 436569 | 0060 | Number of transactions | Non-European Economic Area (EEA) | # |

Resolve the variant from the table, not the column: which metric and which geography the
table holds is a property of the table, whether that is in its name, a partition, or a
filter in the pipeline that loads it. If you cannot establish it, describe what the
column means across all six and say the variant is set by the table - do not pick one.

The row and column parts are shared, so everything except metric, geography, unit and
the datapoint id is the same for all six: same row label, same column label, same
dimension members. That common part is what a description can always state.

## Lookup procedure

1. If you have a warehouse column name, match it against `column_name` in
   `05-datapoints.csv`. Six rows come back for a `.01` template; establish the variant
   from the table, then use that row.
2. If you have a datapoint id, look it up in `05-datapoints.csv`. That row gives you the
   template, the variant, the metric, the geography, the row and column labels and every
   dimension member. Write the description from those fields and stop.
3. If you have a template code, read `04-tables/<TEMPLATE>.md`.
4. If you have a label but no code, search `05-datapoints.csv` on `row_label`. Labels
   repeat across templates, so confirm against the template before you commit.
5. If you cannot resolve an identifier, say so in the description rather than guessing.
   A wrong regulatory description is worse than a missing one.

## Writing the description

State, in this order: what is measured, for which payment instrument, under which
breakdown, and the source. Keep it to two or three sentences.

```text
Number of fraudulent card-based payment transactions initiated electronically and
authenticated via strong customer authentication, reported by the issuing payment
service provider, for transactions cross-border within the EEA. Datapoint 437613 of
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
