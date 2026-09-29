# How to describe PAY 4.2 assets in OpenMetadata

Instructions for an agent writing table, column and glossary descriptions for assets
derived from the EBA PAY 4.2 (FRPPAY 4.2) reporting framework.

## Anatomy of an identifier

A fully qualified datapoint has four parts. Physical table and column names usually
encode some of them:

    Y_03.01 ( 0010 )      R0080          C0020            437613
    template  variant     row code       column code      datapoint id
    |         |           |              |                |
    |         |           |              |                +-- unique on its own
    |         |           |              +-- only unique within a template
    |         |           +-- only unique within a template
    |         +-- metric x geography; only unique within a template
    +-- subject area

**The numeric datapoint id is the only part that is unique on its own.** Row code `0010`
exists in every template and means something different in each. Never describe a column
from its row or column code alone.


## Lookup procedure

1. If you have a datapoint id, look it up in `05-datapoints.csv`. That row gives you the
   template, the variant, the metric, the geography, the row and column labels and every
   dimension member. Write the description from those fields and stop.
2. If you have a template code, read `04-tables/<TEMPLATE>.md`.
3. If you have a label but no code, search `05-datapoints.csv` on `row_label`. Labels
   repeat across templates, so confirm against the template before you commit.
4. If you cannot resolve an identifier, say so in the description rather than guessing.
   A wrong regulatory description is worse than a missing one.

## Writing the description

State, in this order: what is measured, for which payment instrument, under which
breakdown, and the source. Keep it to two or three sentences.

> Number of fraudulent card-based payment transactions initiated electronically and
> authenticated via strong customer authentication, reported by the issuing payment
> service provider, for transactions cross-border within the EEA. Datapoint 437613 of
> template Y_03.01 (EBA PAY 4.2), row 0080, column 0020. Unit: count, non-negative.

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
    |-- Domains
    |   |-- Payment transaction characteristics (31 members)
    |   |-- Fraud event types (12 members)
    |   |-- Payment related parties (8 members)
    |   +-- Geographical breakdown (3 members)
    |-- Dimensions (14, each drawing values from one domain)
    +-- Metrics (3)

Several dimensions share a domain, so a member code alone does not identify a dimension.
`Form of payment` and `Type of authentication` both draw on domain `qPY`. Resolve the
dimension from the datapoint row, never from the member code.
