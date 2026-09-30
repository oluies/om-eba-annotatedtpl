# How to describe DORA assets in OpenMetadata

Instructions for an agent writing table and column descriptions for assets derived from
the DORA register of information. Read this instead of the PAY 4.2 instructions when the
table is a `B_*` one - the lookup rule is different.

## The column name

```text
B0101_r999_c0020
```

splits the same way as a PAY column, with the same pattern:

```text
^(?P<prefix>[A-Za-z]{1,})(?P<major>[0-9]{2})(?P<minor>[0-9]{2})_r(?P<row>[0-9]{1,})_c(?P<col>[0-9]{4})$
```

Note `row` is `[0-9]{1,}` here, not four digits: an open row is written as a record
ordinal such as `999`, which is three.

| Form | Example | Shape |
|---|---|---|
| Column prefix | `B0101` | prefix, major, minor, no separator |
| Template code | `B_01.01` | underscore, then dot |
| Table name | `B_01_01` | underscore, then underscore |

## The row does not narrow anything

**Ignore the row number when resolving a DORA column.** 66 of the 85 datapoints sit
on open rows: the register holds one row per entity, contract or provider, and the DPM
writes that as `r*`. A warehouse writes an ordinal instead - `r999` or a running number - and
it identifies the record, not the framework cell.

Template and column identify the datapoint on their own. Verified against the DPM: 85
cells, 85 distinct ids, 85 distinct template-and-column pairs.

`B_99.01` is the exception, with 19 fixed rows. There the row code does mean
something, and it is a four-digit framework code rather than an ordinal.

## Describing a column

State what the column holds, name the template it belongs to, and cite the datapoint id.
There are no variants in DORA, so unlike PAY there is nothing being withheld:

```text
Name of the entity, column 0020 of template B_01.01
(Entity maintaining the register of information) in the DORA register of information. Datapoint
3287126 (EBA DPM, module DORA 1.1.0). One row per record; the row
number in the column name is an ordinal, not a framework code.
```

## The rest is the same as PAY

Everything in the PAY 4.2 instructions about *how* to write applies here too, and is not
repeated: do not create tables or columns, do not patch columns by index, use the table
CSV export and import which is keyed by `column.name`, confirm before writing, and leave
warehouse context columns alone.
