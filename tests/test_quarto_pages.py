"""The pure parts of the Quarto pages: what goes into a page, not what comes out.

Both of the things tested here broke a render of 157 pages after it had produced a
hundred good ones, which is the worst shape a failure can have - slow, late, and looking
like a Quarto problem rather than a data one.
"""

import json

import _dpm as dpm
import pages
from conftest import DPM2_DB, needs_dpm2


def test_a_title_with_quotes_and_a_colon_is_still_a_yaml_scalar():
    """F_40.02 is `Scope of the group: "instrument-by-instrument"`. Written into YAML as
    it stands, Quarto raises a YAMLException and renders nothing at all - not one bad
    page, no pages."""
    title = 'F_40.02 - Scope of the group: "instrument-by-instrument"'
    scalar = pages.yaml_string(title)
    assert scalar.startswith('"') and scalar.endswith('"')
    assert json.loads(scalar) == title, "a YAML 1.2 double-quoted scalar is a JSON string"


def test_a_stub_names_its_template_and_includes_the_body():
    page = pages.stub("F_18.00.a", "Information on exposures", None)
    assert 'table_code = "F_18.00.a"' in page
    assert "{{< include _body.qmd >}}" in page
    assert page.count("---") >= 2, "the front matter is closed"


def test_a_table_with_no_rows_says_so_rather_than_rendering_a_header():
    assert dpm.markdown_table([]) == "_nothing to show_"


def test_a_pipe_in_a_value_does_not_become_a_column():
    table = dpm.markdown_table([{"label": "a | b"}], ["label"])
    assert table.splitlines()[-1] == "| a \\| b |"


def test_a_table_keeps_the_columns_it_was_given_in_the_order_given():
    table = dpm.markdown_table([{"b": 2, "a": 1}], ["a", "b"])
    assert table.splitlines()[0] == "| a | b |"


def test_a_description_is_composed_from_the_parts_that_exist():
    """There is no sentence to copy - VariableVersion.Name is NULL throughout - so a
    description is the template, the row and the column, and the sheet only when there is
    one."""
    cell = {"row_code": "0010", "row_label": "Loans", "column_code": "0020", "column_label": "Gross", "sheet_code": ""}
    assert dpm.described(cell, "F 18.00") == "F 18.00 / Row: 0010 - Loans / Column: 0020 - Gross"
    assert "Sheet: 0030" in dpm.described(cell | {"sheet_code": "0030"}, "F 18.00")


@needs_dpm2
def test_a_template_with_no_datapoint_placed_elsewhere_counts_zero_not_none():
    """sum() over no rows is NULL, and an f-string formatting None with :, raises
    TypeError - which failed the build a hundred pages in rather than on this template."""
    con = dpm.connect(DPM2_DB)
    for code in ("B_01.01", "F_18.00.a"):
        current = dpm.versions(con, code)[-1]
        drift = dpm.moved(con, current["table_vid"])
        assert drift["moved"] is not None and drift["shared"] is not None, code
        assert f"{drift['moved']:,}"


@needs_dpm2
def test_a_framework_lists_only_templates_that_have_reportable_cells():
    con = dpm.connect(DPM2_DB)
    found = dpm.templates_of(con, "DORA")
    assert found, "DORA is a framework in every release this pack supports"
    for row in found:
        assert dpm.cells(con, row["table_vid"]), f"{row['table_code']} was listed with nothing to report"


@needs_dpm2
def test_the_index_names_a_template_as_its_own_page_does():
    """max() over versions picks an arbitrary one, so the index said RT.01.01 where the
    page said something else. Both read the version in force."""
    con = dpm.connect(DPM2_DB)
    listed = {row["table_code"]: row["name"] for row in dpm.templates_of(con, "DORA")}
    for code, name in listed.items():
        assert dpm.versions(con, code)[-1]["name"] == name
