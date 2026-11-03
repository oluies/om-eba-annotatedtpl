"""What a .bim says, and what the DPM says about it.

The parsing is pure and is tested against a fixture small enough to read. The resolving
needs the database and is tested on the shapes that actually went wrong when this was
written against a real model: a variant written `.A` where the DPM has `.a`, a column code
written three digits wide where the DPM has four, and a template that exists in an older
release but in none of the published ones.
"""

import json

import pytest

import explain_bim as bim
from conftest import DPM2_DB, needs_dpm2


# One measure of each shape that matters: a coordinate, a measure with none, and a measure
# whose expression TMSL stored as a list of lines rather than as a string.
def cell(dimension: str, template: str, row: str, column: str) -> str:
    """One DPM coordinate as this model's DAX writes it."""
    return (
        f"'{dimension}'[TabellKod] = \"{template}\", "
        f"'{dimension}'[RadKod] = \"{row}\", "
        f"'{dimension}'[KolumnKod] = \"{column}\""
    )


A_MODEL = {
    "name": "Small",
    "compatibilityLevel": 1500,
    "model": {
        "culture": "sv-SE",
        "dataSources": [
            {"name": "SQL/somewhere;report", "connectionDetails": {"address": {"server": "s", "database": "d"}}}
        ],
        "relationships": [{"name": "r1"}],
        "roles": [{"name": "Read Only"}],
        "tables": [
            {
                "name": "Matvarden",
                "columns": [{"name": "Varde"}],
                "partitions": [{"source": {"type": "calculated"}}],
                "measures": [
                    {
                        "name": "One cell",
                        "displayFolder": "Kapital",
                        "expression": f"CALCULATE ( SUM ( x ), {cell('Dim_C', 'C 28.00', '999', '330')} )",
                    },
                    {
                        "name": "Two cells",
                        "expression": [
                            f"VAR a = CALCULATE ( SUM ( x ), {cell('Dim_F', 'F 04.04.1', '0090', '0010')} )",
                            f"VAR b = CALCULATE ( SUM ( x ), {cell('Dim_F', 'F 04.04.1', '0110', '0010')} )",
                            "RETURN a + b",
                        ],
                    },
                    {"name": "No cell at all", "expression": "SELECTEDVALUE ( 'Institut'[PeerGroup] )"},
                    {
                        "name": "A template and nothing else",
                        "expression": "CALCULATE ( SUM ( x ), 'Dim_C'[TabellKod] = \"C 01.00\" )",
                    },
                ],
            },
            {
                "name": "Kalender",
                "columns": [{"name": "Datum"}],
                "partitions": [{"source": {"type": "m"}}],
                "measures": [],
            },
        ],
    },
}


@pytest.fixture
def small(tmp_path):
    path = tmp_path / "Model.bim"
    path.write_text(json.dumps(A_MODEL), encoding="utf-8")
    return path


def test_a_bim_is_read_as_what_it_is(small):
    """TMSL carries far more than this reads, so the model ignores what it does not know
    and validates the handful of fields it does."""
    model = bim.read(small)
    assert model.culture == "sv-SE"
    assert [t.name for t in model.tables] == ["Matvarden", "Kalender"]
    assert model.tables[0].kinds() == {"calculated"}
    assert len(model.relationships) == 1


def test_an_expression_is_a_string_or_a_list_of_lines(small):
    """TMSL writes a short expression as a string and a long one as a list, and a measure
    read as `['VAR a = …', 'RETURN a']` has no coordinates in it at all."""
    found = {m.name: m for m in bim.measures_of(bim.read(small))}
    assert "RETURN a + b" in found["Two cells"].expression
    assert len(found["Two cells"].coordinates) == 2


def test_the_coordinates_are_paired_in_document_order(small):
    found = {m.name: m for m in bim.measures_of(bim.read(small))}
    assert found["One cell"].coordinates == (bim.Coordinate("C 28.00", "999", "330"),)
    assert found["Two cells"].coordinates[0].row == "0090"
    assert found["No cell at all"].coordinates == ()


def test_a_template_without_a_row_and_column_is_reported_not_guessed(small):
    """Pairing by document order is only sound while the three lists balance. One that
    names a template and no row is a filter over the whole template, and inventing a
    coordinate for it would be a fact nobody wrote."""
    found = {m.name: m for m in bim.measures_of(bim.read(small))}
    assert found["A template and nothing else"].coordinates == ()
    assert found["A template and nothing else"].unpaired


def test_a_variant_written_in_capitals_is_the_same_template():
    """The DPM writes `C_66.01.a` and this model writes `C 66.01.A`. That one letter made
    476 coordinates look withdrawn when they were not."""
    assert bim.template_variants("C 66.01.A") == ["C_66.01.A", "C_66.01.a"]
    assert bim.template_variants("C 28.00") == ["C_28.00"]


def test_a_code_is_tried_at_the_widths_people_write():
    """FINREP rows are four digits and COREP large-exposure columns are three, and a model
    may carry either."""
    assert bim.variants("330")[:2] == ["330", "0330"]
    assert "330" in bim.variants("0330")


@needs_dpm2
def test_a_coordinate_resolves_to_what_the_regulation_calls_it(small, monkeypatch):
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    cells = bim.published(None)
    found = bim.resolve(bim.Coordinate("F 04.04.1", "0090", "0010"), cells)
    assert found.found, "F 04.04.1 r0090 c0010 is in the model and should resolve"
    assert found.exact, "it is written exactly as the DPM has it"
    assert found.found["row_label"]


@needs_dpm2
def test_a_withdrawn_template_is_told_apart_from_one_that_never_existed(monkeypatch):
    """The distinction is the whole value of the missing list: one needs the measure
    rewritten against what replaced it, the other has never returned anything."""
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    every = bim.published(None)
    withdrawn = bim.Coordinate("C 02.00", "0010", "0010")
    assert "older release" in bim.elsewhere(withdrawn, every), "C 02.00 was split into .a and .b"
    assert "no release" in bim.elsewhere(bim.Coordinate("C 99.99", "0010", "0010"), every)


@needs_dpm2
def test_an_open_table_is_matched_rather_than_called_missing(monkeypatch):
    """C_28.00 is large exposures: the reporter files one row per exposure, so the DPM
    writes the row as `*` and the model writes `999` as its own convention. Matched
    literally it looks withdrawn, which reads as broken when it is not - and the first
    measure of the model this was written for is exactly that case.
    """
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    cells = bim.published(None)
    found = bim.resolve(bim.Coordinate("C 28.00", "999", "330"), cells)
    assert found.found, "C 28.00 c330 is a real column of an open table"
    assert bim.is_open(found), "it should be reported as open rather than as exact"
    assert found.found["column_label"] == "Total"


@needs_dpm2
def test_a_fixed_row_is_preferred_over_the_open_one(monkeypatch):
    """The open form is tried only after the literal ones, so a template that has both a
    real row and an open axis is never reported as open when the row exists."""
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    cells = bim.published(None)
    found = bim.resolve(bim.Coordinate("F 04.04.1", "0090", "0010"), cells)
    assert found.exact and not bim.is_open(found)


def test_the_tool_reads_only_bim_files_inside_the_configured_directory(tmp_path, monkeypatch, small):
    """Every other tool in this pack reads a database or an API. This one takes a path,
    and a tool that takes a path is a file reader unless it is told where to stop.

    The resolving happens before the check, which is the point: `../../etc/passwd` and a
    symlink out of the directory both look like a name inside it until resolved.
    """
    monkeypatch.setenv("BIM_ROOT", str(small.parent))
    outside = tmp_path.parent / "elsewhere.bim"
    outside.write_text("{}", encoding="utf-8")

    assert bim.within_root("Model.bim") == small.resolve()
    for refused in ("../../../../etc/passwd", "/etc/passwd", str(outside), "Model.txt"):
        with pytest.raises(ValueError):
            bim.within_root(refused)


def test_a_symlink_out_of_the_directory_is_refused(tmp_path, monkeypatch, small):
    """A name inside the directory that is not a file inside the directory."""
    monkeypatch.setenv("BIM_ROOT", str(small.parent))
    secret = tmp_path.parent / "secret.bim"
    secret.write_text("{}", encoding="utf-8")
    pointer = small.parent / "innocent.bim"
    pointer.symlink_to(secret)
    with pytest.raises(ValueError):
        bim.within_root("innocent.bim")


def test_the_tool_refuses_rather_than_raises(monkeypatch, small):
    """A tool call that fails should come back as an answer the model can read, not as an
    exception the host has to catch."""
    monkeypatch.setenv("BIM_ROOT", str(small.parent))
    refused = bim.explain_bim_measure("/etc/passwd", "anything")
    assert refused["found"] is False
    assert "not a .bim" in refused["message"]


def test_the_tool_never_returns_the_connection_string(monkeypatch, small):
    """A .bim carries where someone's warehouse lives. The CLI prints it only with
    --source, and the tool has no such flag."""
    monkeypatch.setenv("BIM_ROOT", str(small.parent))
    answered = bim.explain_bim_measure("Model.bim", "No cell at all")
    assert "dataSources" not in json.dumps(answered)
    assert "somewhere" not in json.dumps(answered), "the data source's name reached the answer"


@needs_dpm2
def test_the_tool_is_registered_in_all_three_places(monkeypatch, small):
    """A tool lives as a ToolName member, a TOOLS definition and a `case` arm, and
    dropping one means dropping all three. This is the arm: dispatch by name."""
    import agent_tools

    monkeypatch.setenv("BIM_ROOT", str(small.parent))
    assert bim.EXPLAIN_BIM_MEASURE_TOOL_NAME in {name.value for name in agent_tools.ToolName}
    # Read the way test_lookups reads it: the definitions are a tuple of dicts whose
    # values are themselves dicts, and a checker has no way to know which is which.
    shown = {str(function["name"]) for tool in agent_tools.TOOLS if isinstance(function := tool.get("function"), dict)}
    assert bim.EXPLAIN_BIM_MEASURE_TOOL_NAME in shown, "the definition is not among the ones a model is shown"
    answered = agent_tools.dispatch(bim.EXPLAIN_BIM_MEASURE_TOOL_NAME, {"bim": "Model.bim", "measure": "One cell"})
    assert answered["found"], answered
    assert answered["coordinates"][0]["written"] == "C 28.00 r999 c330"


@needs_dpm2
def test_a_formula_can_be_read_with_the_coordinates_written_out(monkeypatch):
    """`r0090 c0010` is the unreadable part of a measure, not DAX. Only that is replaced,
    so a reader can still see which part of the formula they are looking at."""
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    cells = bim.published(None)
    dax = (
        "CALCULATE ( SUM ( 'Fakta_F'[VardeDecimal] ), "
        "'Dim_F'[TabellKod] = \"F 04.04.1\", 'Dim_F'[RadKod] = \"0090\", 'Dim_F'[KolumnKod] = \"0010\" )"
    )
    said = bim.in_words(dax, cells)
    assert "CALCULATE ( SUM ( 'Fakta_F'[VardeDecimal] )" in said, "the formula is otherwise untouched"
    assert "TabellKod" not in said, "the three codes are gone"
    assert "«F 04.04.1 (FINREP) ·" in said, said
    assert "Carrying amount»" in said


@needs_dpm2
def test_the_rows_are_said_in_the_regulation_s_own_swedish(monkeypatch):
    """Not a translation of the model's English: the wording the Official Journal
    published, which is what makes it usable in a Swedish review."""
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    cells = bim.published(None)
    dax = "'Dim_F'[TabellKod] = \"F 04.04.1\", 'Dim_F'[RadKod] = \"0090\", 'Dim_F'[KolumnKod] = \"0010\""
    swedish = bim.wording({"F_04.04.1"})
    if not swedish:
        pytest.skip("source/its_labels.csv is not built")
    said = bim.in_words(dax, cells, swedish)
    assert "Offentlig" in said, said


def test_filters_that_do_not_stand_together_are_left_alone():
    """Reassembling them would produce a formula nobody wrote, which is the same reason
    the parser refuses to pair unbalanced ones."""
    scattered = (
        "VAR a = CALCULATE ( x, 'Dim_C'[TabellKod] = \"C 01.00\" )\n"
        "VAR b = CALCULATE ( y, 'Dim_C'[RadKod] = \"0010\", 'Dim_C'[KolumnKod] = \"0010\" )"
    )
    assert bim.in_words(scattered, {}) == scattered


def test_both_naming_conventions_are_read():
    """A model may name a coordinate either way, and the one this was written against uses
    both: `Dim_C[TabellKod]` on its dimension tables and `Fakta_S[Table_code]` on one fact
    table - 1 565 filters of the first and 418 of the second. Reading only the first
    undercounted the model by a fifth and never looked at one framework at all.
    """
    swedish_names = "'Dim_C'[TabellKod] = \"C 01.00\", 'Dim_C'[RadKod] = \"0010\", 'Dim_C'[KolumnKod] = \"0010\""
    english_names = (
        "'Fakta_S'[Table_code] = \"S 01.01\", 'Fakta_S'[Row_code] = \"0160\", 'Fakta_S'[Column_code] = \"0010\""
    )
    for dax, expected in ((swedish_names, "C 01.00"), (english_names, "S 01.01")):
        coordinates, unpaired = bim.coordinates_in(dax)
        assert not unpaired
        assert coordinates[0].template == expected


def test_the_swedish_is_used_only_where_the_two_agree():
    """The Official Journal's grid and the DPM are keyed the same way and do not always
    agree. For F 05.01 the Journal's row 0010 is "By product" where the DPM's is "On
    demand [call] and short notice [current account]" - putting one row's Swedish against
    another is worse than showing no Swedish at all.
    """
    assert bim.agrees("Households", "Households")
    assert bim.agrees("households ", "Households")
    assert not bim.agrees("By product", "On demand [call] and short notice [current account]")
    assert not bim.agrees("", "Anything")


@needs_dpm2
def test_a_matched_coordinate_says_whose_template_it_is(monkeypatch):
    """A template code is not unique across frameworks. The DPM's S_01.01 is PAY - payment
    fraud reporting - and a model using `S 01.01` for its own national returns matches it
    and gets "Number of credit transfers" into a balance sheet. Nothing here can know which
    was meant; naming the framework is what lets a reader see it.
    """
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    cells = bim.published(None)
    found = bim.resolve(bim.Coordinate("S 01.01", "0010", "0010"), cells)
    assert found.found and found.found["framework"] == "PAY"
    said = bim.in_words(
        "'Fakta_S'[Table_code] = \"S 01.01\", 'Fakta_S'[Row_code] = \"0010\", 'Fakta_S'[Column_code] = \"0010\"", cells
    )
    assert "(PAY)" in said, said


@needs_dpm2
def test_a_code_from_another_framework_is_refused_and_named(monkeypatch):
    """`Fakta_S` in the model this was written against is described in the model itself as
    the authority's own standard report for banks, and its `S 01.01` rows 0010-0050 are
    interest-earning assets. The DPM's S_01.01 is PAY: "Number of credit transfers". Told
    which frameworks apply, the tool refuses the match and says whose template has that
    code, which is a different answer from "nothing has it".
    """
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    cells = bim.published(None)
    coordinate = bim.Coordinate("S 01.01", "0010", "0010")

    unasked = bim.resolve(coordinate, cells)
    assert unasked.found and unasked.found["framework"] == "PAY", "without a filter it matches PAY"

    asked = bim.resolve(coordinate, cells, {"COREP", "FINREP"})
    assert not asked.found, "PAY is not among the frameworks asked for"
    assert asked.refused == "PAY", "and the refusal says which framework had the code"
    assert "PAY" in bim.elsewhere(coordinate, cells, {"COREP", "FINREP"}) or "no release" in bim.elsewhere(
        coordinate, cells, {"COREP", "FINREP"}
    ), "the line under it must not contradict the refusal"


@needs_dpm2
def test_the_filter_does_not_refuse_what_it_should_keep(monkeypatch):
    """A filter that quietly dropped good matches would be worse than none."""
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    cells = bim.published(None)
    kept = bim.resolve(bim.Coordinate("F 04.04.1", "0090", "0010"), cells, {"COREP", "FINREP"})
    assert kept.found and kept.found["framework"] == "FINREP"
    assert kept.refused is None
