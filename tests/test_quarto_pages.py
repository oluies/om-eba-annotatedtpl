"""The pure parts of the Quarto pages: what goes into a page, not what comes out.

Both of the things tested here broke a render of 157 pages after it had produced a
hundred good ones, which is the worst shape a failure can have - slow, late, and looking
like a Quarto problem rather than a data one.
"""

import json
from pathlib import Path

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


def test_the_switcher_marks_where_you_are_and_links_the_rest():
    html = pages.switcher("4.3", ["4.2.1", "4.3", "4.4"])
    assert 'class="release current" href="#">4.3' in html
    assert 'href="../4.4/"' in html and 'href="../4.2.1/"' in html
    assert html.count('class="release"') == 2, "every release but the current one is a link"


def test_the_switcher_links_are_relative_to_the_release_directory():
    """The whole tree moves - /templates/4.3/C_01.00.html is mounted wherever Pages puts
    it - so ../4.4/ keeps working and /templates/4.4/ would not."""
    html = pages.switcher("4.3", ["4.3", "4.4"])
    assert "/templates/" not in html
    assert html.count("../") == 1


def test_one_release_still_produces_a_switcher_without_links():
    html = pages.switcher("4.3", ["4.3"])
    assert 'class="release current"' in html
    assert "../" not in html, "nothing to switch to"


def test_a_reworded_row_keeps_every_wording_in_order():
    """The file has one entry per wording, oldest first, so a page can show what the row
    said before. A single entry is a row that never changed and is not shown."""
    import csv as _csv
    import io

    rows = list(
        _csv.DictReader(
            io.StringIO(
                "template,row,celex,en\n"
                "C_01.00,0510,02021R0451-20210319,(-) Amount exceeding the 17.65 % threshold\n"
                "C_01.00,0510,02021R0451-20230711,(-) Amount exceeding the 17.65% threshold\n"
            )
        )
    )
    assert [row["celex"] for row in rows] == sorted(row["celex"] for row in rows)
    assert rows[0]["en"] != rows[1]["en"]


def test_the_execute_daemon_is_off():
    """A kernel keeps the environment it was started with. With the daemon on, rendering
    4.3 and then 4.4 gave the second render the first one's DPM2_DB, so every page under
    /templates/4.4/ was built from the 4.3 database while saying 4.4 - and the two
    directories differed only in the switcher, which is the one thing that made it look
    right. The daemon is per file, so it bought nothing across a project either."""
    config = (Path(pages.__file__).parent / "_quarto.yml").read_text(encoding="utf-8")
    assert "daemon: false" in config, "rendering two releases needs two environments"
