# Agent prompt for EBA reporting frameworks

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
    explain_report         what a reported xBRL-CSV file is, before checking it
    check_report           that module version's rules, run against the file

  Four rules hold for all of them:

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
