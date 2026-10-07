"""The pure parts of the BA_Form_Cell overlay: the LIKE pattern and the axis join.

None of this needs SQL Server. That is the point of keeping them pure - the join's shape
and the escaping are the two things most likely to be subtly wrong, and both are
assertable without a connection.
"""

import pytest

import ba_form_cell as ba
from ba_form_cell import fold_rows, like_prefix, literal, rendered_sql

NAMES = ("dpm_cell_code", "cell_sk", "row_column_code", "taxonomy_name", "open_axis_value_1")


def test_like_prefix_escapes_the_underscore():
    """An unescaped underscore is a single-character wildcard, so Y0101Xr0010 would match."""
    assert like_prefix("Y0101_r0010_c0010") == r"Y0101\_r0010\_c0010%"


@pytest.mark.parametrize("char", ["\\", "%", "_", "["])
def test_like_prefix_escapes_every_wildcard(char):
    assert like_prefix(f"a{char}b") == f"a\\{char}b%"


def test_fold_rows_gathers_the_axis_values_of_one_cell():
    rows = [
        ("{Y 01.01, r0010, c0010, s0010}", 1, "Y0101_r0010_c0010", "DPM_4.2", "0010"),
        ("{Y 01.01, r0010, c0010, s0010}", 1, "Y0101_r0010_c0010", "DPM_4.2", "0020"),
    ]
    (cell,) = fold_rows(NAMES, rows)
    assert cell.cell_sk == 1
    assert cell.open_axis_values == ("0010", "0020")


def test_fold_rows_keeps_distinct_cells_apart():
    rows = [
        ("{Y 01.01, r0010, c0010, s0010}", 1, "Y0101_r0010_c0010", "DPM_4.2", "0010"),
        ("{Y 01.01, r0010, c0020, s0010}", 2, "Y0101_r0010_c0020", "DPM_4.2", "0010"),
    ]
    assert [c.cell_sk for c in fold_rows(NAMES, rows)] == [1, 2]


def test_fold_rows_is_right_for_a_one_to_one_join_too():
    """The axis table may hold one row per cell or many; grouping on Cell_sk covers both."""
    rows = [("{Y 01.01, r0010, c0010, s0010}", 1, "Y0101_r0010_c0010", "DPM_4.2", None)]
    (cell,) = fold_rows(NAMES, rows)
    assert cell.open_axis_values == ()


def test_fold_rows_does_not_repeat_a_value():
    rows = [("{c}", 1, "r", "DPM_4.2", "0010")] * 3
    (cell,) = fold_rows(NAMES, rows)
    assert cell.open_axis_values == ("0010",)


def test_fold_rows_falls_back_to_the_cell_code_without_a_surrogate_key():
    rows = [("{Y 01.01, r0010, c0010, s0010}", None, "r", "DPM_4.2", "0010")]
    (cell,) = fold_rows(NAMES, rows)
    assert cell.dpm_cell_code == "{Y 01.01, r0010, c0010, s0010}"


@pytest.mark.parametrize(
    ("value", "spelled"),
    [(None, "NULL"), (True, "1"), (False, "0"), (7, "7"), ("x", "'x'"), ("O'Brien", "'O''Brien'")],
)
def test_literal_spells_a_parameter_as_t_sql_would(value, spelled):
    assert literal(value) == spelled


def test_rendered_sql_fills_the_placeholders_in_order():
    assert rendered_sql("WHERE a = ? AND b = ?", ["x", 2]) == "WHERE a = 'x' AND b = 2"


def test_rendered_sql_is_only_ever_a_rendering():
    """It escapes quotes so a pasted statement is valid, but it never executes."""
    assert rendered_sql("x = ?", ["'; DROP TABLE t --"]) == "x = '''; DROP TABLE t --'"


def test_pack_applies_only_where_the_taxonomy_matches():
    def cell(taxonomy):
        return ba.FormCell(dpm_cell_code="{c}", taxonomy_name=taxonomy)

    assert ba.pack_applies([cell("DPM_4.2")])
    assert not ba.pack_applies([cell("DPM_3.2")])
    assert not ba.pack_applies([])
