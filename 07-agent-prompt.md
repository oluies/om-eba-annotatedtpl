# Agent prompt for EBA reporting frameworks

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
