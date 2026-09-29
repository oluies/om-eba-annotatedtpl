# Agent prompt for PAY 4.2 assets

Paste the block below into the system prompt of an agent that describes assets in
OpenMetadata. It is deliberately short: the trigger and the rules that must hold even if
nothing is retrieved. The content lives in OpenMetadata as Context Center articles and
glossary terms, reachable with `find_context`.

```text
When describing a table or column from an EBA reporting framework - table names like
Y_01_01 or A_00_01, columns like Y0101_r0010_c0010 - first read the article "How to
describe PAY 4.2 assets in OpenMetadata" (find_context) and follow it.

A datapoint column splits as:

  ^(?P<prefix>[A-Za-z]{1,})(?P<major>[0-9]{2})(?P<minor>[0-9]{2})_r(?P<row>[0-9]{4})_c(?P<col>[0-9]{4})$

major and minor are two digits each, row and col are four. The same identity has three
forms and only the punctuation differs: column prefix Y0101, template code Y_01.01,
table name Y_01_01. Build the template code from the column name and read the Context
Center page with that title - that page holds the row and column grid with the datapoint
ids. You do not have 05-datapoints.csv; it is what describe_table.py uses.

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
- A column name carries no variant. If the metric and geography cannot be established
  from the table, describe what holds across all six variants and say the variant is
  set by the table.
- Columns that do not match that pattern are warehouse context - Period_SK,
  Company_BK, Taxonomy_Name and the like. They have no framework meaning, so do not
  describe them from the framework.
```

## Where to put it instead

If the agent runs as an OpenMetadata persona, the same text can live in the persona
context document and be fetched with `get_persona_context`. That keeps one copy for the
organisation rather than one per agent. The trigger still belongs in the prompt, because
the agent has to know to make that call.

## Two things to check first

Retrieval only works if the server supports it. `company_context` needs vector embeddings
configured for its `query` mode - without them only `fqn` lookups work. And knowledge
pills are extracted asynchronously, so confirm the articles reached
`pageProcessingStatus: Processed` before relying on them being searchable.
