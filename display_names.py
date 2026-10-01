"""The rule for what a table and its columns are called in the catalogue.

A display name replaces the identifier in the UI, so `Y0101_r0060_c0010` becomes something
a reader can act on. The obvious rule - row label, then column label - is not enough on
its own, because the EBA layout nests its rows: "Of which: authenticated via strong
customer authentication" appears under several parents, and the label alone is identical
in each. Measured on this framework, 63 of 214 label pairs collide that way.

What actually distinguishes those rows is in their dimensions, which is where the parent
context ends up once the layout is flattened. So a colliding label is extended with the
dimension members that differ inside its own group, and only those: adding every member
would turn a label into the description that is already underneath it.

This lives on its own because two tools need the same answer. The lookup tool suggests
the name and the writer writes it; if they disagreed, the catalogue would end up with
whichever ran last.

Pure, and the only input is rows as `05-datapoints.csv` spells them.
"""

from collections import defaultdict
from collections.abc import Mapping, Sequence

Row = Mapping[str, str]


def members(dimensions: str) -> dict[str, str]:
    """`Form of payment=Credit transfers; Type of authentication=...` as a mapping."""
    pairs = {}
    for part in filter(None, (p.strip() for p in dimensions.split(";"))):
        dimension, _, member = part.partition("=")
        if member:
            pairs[dimension.strip()] = member.strip()
    return pairs


def base_name(row: Row) -> str:
    """Row label then column label: what the coordinate means, with no codes in it.

    The variant is deliberately absent. It belongs to the table or, with an open axis, to
    the row, so naming one here would make six columns claim to be the same one.
    """
    return f"{row['row_label']} - {row['column_label']}"


def table_name(row: Row) -> str:
    """The table's own name: the template code as the DPM writes it, then its name."""
    return f"{row['template'].replace('_', ' ')} {row['template_name']}"


def display_names(rows: Sequence[Row]) -> dict[str, str]:
    """Column name to display name, unique within the table by construction.

    Pass every datapoint row of one table, one per column; variants do not matter here
    because none of the fields used varies by variant.
    """
    by_column = {row["column_name"]: row for row in rows}
    groups: dict[str, list[Row]] = defaultdict(list)
    for row in by_column.values():
        groups[base_name(row)].append(row)

    names: dict[str, str] = {}
    for label, group in groups.items():
        if len(group) == 1:
            names[group[0]["column_name"]] = label
            continue
        dimensions = [members(row.get("row_dimensions", "")) for row in group]
        varying = [
            dimension
            for dimension in dict.fromkeys(key for mapping in dimensions for key in mapping)
            if len({mapping.get(dimension) for mapping in dimensions}) > 1
        ]
        for row, mapping in zip(group, dimensions, strict=True):
            distinguishing = ", ".join(mapping[d] for d in varying if d in mapping)
            names[row["column_name"]] = f"{label} ({distinguishing})" if distinguishing else label

    # Last resort. Nothing in this framework needs it, but a label that is still not
    # unique would show up in the UI as several identical columns, which is worse than a
    # code in the name.
    seen: dict[str, str] = {}
    for column_name, label in names.items():
        if label in seen:
            names[column_name] = f"{label} ({by_column[column_name]['row_code']})"
            other = seen[label]
            names[other] = f"{label} ({by_column[other]['row_code']})"
        else:
            seen[label] = column_name
    return names
