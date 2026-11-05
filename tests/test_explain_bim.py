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
                    # A measure holding no coordinate of its own, which is what 499 of the
                    # 2 131 measures of the model this was written for look like.
                    {
                        "name": "A ratio of other measures",
                        "expression": "DIVIDE ( [One cell] + [Two cells], [No cell at all] )",
                    },
                    {"name": "A ratio of the ratio", "expression": "[A ratio of other measures] * 100"},
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


def test_a_filter_list_is_the_cells_of_its_cross_product():
    """`RadKod IN {0110, 0210, 0260, 0310}` with five columns is twenty cells. That is
    what the measure says, not an inference about it - the nine measures this could not
    read were all of this shape, and they are the balance-sheet aggregates.
    """
    dax = (
        "CALCULATE ( SUM ( x ), "
        "'Dim_F'[TabellKod] = \"F 08.01.A\", "
        '\'Dim_F\'[RadKod] IN { "0110", "0210", "0260", "0310" }, '
        '\'Dim_F\'[KolumnKod] IN { "0010", "0020", "0030", "0034", "0035" } )'
    )
    coordinates, unpaired = bim.coordinates_in(dax)
    assert not unpaired
    assert len(coordinates) == 20, "four rows by five columns"
    assert bim.Coordinate("F 08.01.A", "0110", "0010") in coordinates
    assert bim.Coordinate("F 08.01.A", "0310", "0035") in coordinates


def test_a_list_of_templates_is_read_too():
    """`TabellKod IN { "C 02.00", "C 02.00.A" }` is one measure covering a template and
    the variant that replaced it - which is how a model survives a split."""
    dax = (
        'CALCULATETABLE ( t, \'Dim_C\'[TabellKod] IN { "C 02.00", "C 02.00.A" }, '
        "'Dim_C'[RadKod] = \"0010\", 'Dim_C'[KolumnKod] = \"0010\" )"
    )
    coordinates, unpaired = bim.coordinates_in(dax)
    assert not unpaired
    assert {c.template for c in coordinates} == {"C 02.00", "C 02.00.A"}


def test_filters_out_of_order_are_still_refused():
    """The reason for reading them in groups is that a group is a cell. Two rows and no
    column is not one, and guessing which column was meant would invent a fact."""
    _, unpaired = bim.coordinates_in("'Dim_C'[RadKod] = \"0010\", 'Dim_C'[RadKod] = \"0020\"")
    assert unpaired


def test_the_rendering_replaces_the_whole_filter_including_its_table():
    """Replacing from the bracket leaves `'Dim_F'` standing in front of what replaced it."""
    dax = (
        "CALCULATE ( SUM ( x ), "
        "'Dim_F'[TabellKod] = \"F 99.99\", 'Dim_F'[RadKod] = \"0010\", 'Dim_F'[KolumnKod] = \"0010\" )"
    )
    said = bim.in_words(dax, {})
    assert "'Dim_F'«" not in said, said
    assert "«F 99.99" in said


def test_the_shapes_dax_allows_are_all_read():
    """The model this was written for quotes its table qualifiers, writes its filters in
    template-row-column order and separates them with commas. DAX requires none of that,
    and a reader that assumes all three answers nothing for a model written otherwise.
    """
    shapes = {
        "quoted": "'Dim_C'[TabellKod] = \"C 01.00\", 'Dim_C'[RadKod] = \"0010\", 'Dim_C'[KolumnKod] = \"0010\"",
        "unquoted": 'Dim_C[TabellKod] = "C 01.00", Dim_C[RadKod] = "0010", Dim_C[KolumnKod] = "0010"',
        "joined with &&": (
            "FILTER ( t, 'Dim_C'[TabellKod] = \"C 01.00\" && 'Dim_C'[RadKod] = \"0010\" "
            "&& 'Dim_C'[KolumnKod] = \"0010\" )"
        ),
        "row first": "'Dim_C'[RadKod] = \"0010\", 'Dim_C'[KolumnKod] = \"0010\", 'Dim_C'[TabellKod] = \"C 01.00\"",
    }
    for name, dax in shapes.items():
        coordinates, unpaired = bim.coordinates_in(dax)
        assert not unpaired, f"{name} was left dangling"
        assert coordinates == (bim.Coordinate("C 01.00", "0010", "0010"),), name


def test_two_calculates_are_still_not_one_group():
    """Widening what counts as adjacent must not widen it to this: a template in one
    CALCULATE and a row in the next are not a cell."""
    _, unpaired = bim.coordinates_in(
        "CALCULATE ( x, 'Dim_C'[TabellKod] = \"C 01.00\" ) "
        "+ CALCULATE ( y, 'Dim_C'[RadKod] = \"0010\", 'Dim_C'[KolumnKod] = \"0010\" )"
    )
    assert unpaired


@needs_dpm2
def test_a_template_in_two_frameworks_answers_to_either(monkeypatch):
    """Thirteen templates are filed under two frameworks - C_18.00 is COREP and IF - and
    keeping one framework per cell meant asking for IF refused a cell that exists in IF,
    on the grounds that it is COREP. That is the guarantee --frameworks exists to give.
    """
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    cells = bim.published(None)
    key = next(k for k in cells if k[0] == "C_18.00")
    held = cells[key]["frameworks"]
    assert {"COREP", "IF"} <= held, f"C_18.00 should be filed under both, not {held}"

    for asked in ({"COREP"}, {"IF"}):
        found = bim.resolve(bim.Coordinate("C 18.00", key[1], key[2]), cells, asked)
        assert found.found, f"{asked} should find its own cell"
        assert bim.whose(found.found, asked) == next(iter(asked))

    refused = bim.resolve(bim.Coordinate("C 18.00", key[1], key[2]), cells, {"FINREP"})
    assert not refused.found and refused.refused == "COREP/IF"


@needs_dpm2
def test_the_tool_can_be_told_which_frameworks_apply(monkeypatch, small):
    """Without it an agent asking about the model's `S 01.01` is answered from the EBA's
    PAY template of that code - which is the mismatch --frameworks was added to prevent,
    reaching the one caller that could not pass it."""
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    monkeypatch.setenv("BIM_ROOT", str(small.parent))
    import agent_tools

    # Narrowed step by step rather than subscripted through: the definitions are literal
    # dicts whose values are themselves dicts, and a checker has one wide union for them.
    shown = {
        str(function["name"]): function
        for tool in agent_tools.TOOLS
        if isinstance(function := tool.get("function"), dict)
    }
    parameters = shown[bim.EXPLAIN_BIM_MEASURE_TOOL_NAME].get("parameters")
    assert isinstance(parameters, dict)
    properties = parameters.get("properties")
    assert isinstance(properties, dict)
    assert "frameworks" in properties, "the model is never offered the one thing that disambiguates"


def test_a_group_is_not_collapsed_by_its_first_cell_being_missing():
    """`TabellKod IN { "C 02.00", "C 02.00.A" }` is a measure written to survive a
    template being split. Reading the labels from the first cell *written* made the whole
    group render as "not in this release" - because the half it was written to outlive is
    indeed gone - and the twenty cells of a 4x5 group went the same way whenever their
    first row and column happened to be missing.
    """
    cells = {
        ("C_02.00.A", "0010", "0010"): {
            "framework": "COREP",
            "frameworks": {"COREP"},
            "table_code": "C_02.00.A",
            "row_code": "0010",
            "column_code": "0010",
            "row_label": "TOTAL RISK EXPOSURE AMOUNT",
            "column_label": "TREA",
            "datapoint": 1,
        }
    }
    dax = (
        'CALCULATETABLE ( t, \'Dim_C\'[TabellKod] IN { "C 02.00", "C 02.00.A" }, '
        "'Dim_C'[RadKod] = \"0010\", 'Dim_C'[KolumnKod] = \"0010\" )"
    )
    said = bim.in_words(dax, cells)
    assert "TOTAL RISK EXPOSURE AMOUNT" in said, said
    assert "C 02.00?" in said, "the half that is gone should be marked, not hidden"
    assert "not in this release" not in said


def test_a_group_with_nothing_behind_it_still_says_so():
    """Anchoring on a cell that exists must not turn a group that resolves to nothing into
    a group that looks resolved."""
    said = bim.in_words(
        "CALCULATE ( x, 'Dim_C'[TabellKod] = \"C 99.99\", 'Dim_C'[RadKod] = \"0010\", 'Dim_C'[KolumnKod] = \"0010\" )",
        {},
    )
    assert "not in this release" in said, said


@needs_dpm2
def test_a_release_the_database_does_not_carry_is_refused_by_name(monkeypatch):
    """It matched no rows and returned nothing, so every coordinate read as withdrawn: a
    whole model apparently obsolete because of a typo. The lookups refuse an unknown
    release by name and list what there is; so does this."""
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    with pytest.raises(bim.UnknownRelease) as refused:
        bim.published("4.33")
    assert "4.33" in str(refused.value)
    assert "It has:" in str(refused.value), "a refusal that does not say what there is wastes the next attempt"


@needs_dpm2
def test_the_tool_answers_a_bad_release_rather_than_raising(monkeypatch, small):
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    monkeypatch.setenv("BIM_ROOT", str(small.parent))
    answered = bim.explain_bim_measure("Model.bim", "One cell", release="4.33")
    assert answered["found"] is False
    assert "4.33" in answered["message"]


def test_a_bim_with_a_byte_order_mark_is_read(tmp_path, monkeypatch):
    """Visual Studio and SSDT write one, and json.loads answers it with "Unexpected UTF-8
    BOM" rather than reading it - a traceback from the CLI and a dispatcher error from the
    tool, for a file that is perfectly well formed."""
    path = tmp_path / "WithBom.bim"
    path.write_text("﻿" + json.dumps(A_MODEL), encoding="utf-8")
    model = bim.read(path)
    assert [t.name for t in model.tables] == ["Matvarden", "Kalender"]

    monkeypatch.setenv("BIM_ROOT", str(tmp_path))
    answered = bim.explain_bim_measure("WithBom.bim", "No such measure")
    assert "no measure called" in answered["message"], "it got far enough to look for the measure"


def test_the_tool_answers_a_file_it_cannot_read(tmp_path, monkeypatch):
    """A refusal the model can read, not an exception the host has to catch."""
    monkeypatch.setenv("BIM_ROOT", str(tmp_path))
    (tmp_path / "Broken.bim").write_text("{not json", encoding="utf-8")
    answered = bim.explain_bim_measure("Broken.bim", "anything")
    assert answered["found"] is False
    assert "cannot read" in answered["message"] or "not a .bim this can read" in answered["message"]


# --- a measure written in terms of other measures ---------------------------------------


def test_a_reference_is_told_from_a_column_by_asking_the_model(small):
    """`[One cell]` is a measure and `'Dim_C'[Varde]` is a column, and unqualified they are
    the same syntax: `Dim_C[RadKod]` inside a FILTER is a column reference written exactly
    like a measure reference. The model's own measure names are what tells them apart."""
    among = frozenset(bim.by_name(bim.measures_of(bim.read(small))))
    dax = "DIVIDE ( [One cell] + [Two cells], 'Dim_C'[Varde] ) + Dim_C[RadKod] + [RadKod]"
    assert bim.references_in(dax, among) == ("One cell", "Two cells")


def test_a_reference_is_named_once_however_often_it_is_written(small):
    among = frozenset(bim.by_name(bim.measures_of(bim.read(small))))
    assert bim.references_in("[One cell] + [One cell] - [One cell]", among) == ("One cell",)


def test_a_measure_stands_for_the_coordinates_of_the_measures_it_names(small):
    """The point of the exercise: `A ratio of other measures` holds no filter at all, and
    before this it was a formula printed back with nothing said about it."""
    measures = bim.by_name(bim.measures_of(bim.read(small)))
    walk = bim.reached(measures["A ratio of other measures"], measures)
    assert [(path, str(c)) for path, c in walk] == [
        (("One cell",), "C 28.00 r999 c330"),
        (("Two cells",), "F 04.04.1 r0090 c0010"),
        (("Two cells",), "F 04.04.1 r0110 c0010"),
    ]


def test_a_measure_names_its_own_coordinates_first_and_with_no_path(small):
    measures = bim.by_name(bim.measures_of(bim.read(small)))
    assert bim.reached(measures["One cell"], measures) == (((), bim.Coordinate("C 28.00", "999", "330")),)


def test_a_coordinate_two_measures_away_says_the_way_there(small):
    """A coordinate reached through two hops is a different thing to maintain from one the
    measure names itself, so the path is part of the answer rather than a detail."""
    measures = bim.by_name(bim.measures_of(bim.read(small)))
    walk = bim.reached(measures["A ratio of the ratio"], measures)
    assert {path for path, _ in walk} == {
        ("A ratio of other measures", "One cell"),
        ("A ratio of other measures", "Two cells"),
    }


def test_a_cycle_does_not_loop():
    """DAX forbids a circular reference and a file on disk can hold one anyway. Reading a
    model should say what it can rather than hang."""
    model = bim.BimModel.model_validate(
        {
            "tables": [
                {
                    "name": "T",
                    "measures": [
                        {"name": "A", "expression": f"[B] + CALCULATE ( x, {cell('Dim_C', 'C 28.00', '999', '330')} )"},
                        {"name": "B", "expression": "[A] * 2"},
                    ],
                }
            ]
        }
    )
    measures = bim.by_name(bim.measures_of(model))
    assert [str(c) for _, c in bim.reached(measures["B"], measures)] == ["C 28.00 r999 c330"]


def test_a_composed_measure_is_counted_in_the_summary(small):
    """The count of measures naming a coordinate reads as "the rest is not about
    reporting", and for a model written this way that is wrong by hundreds."""
    model = bim.read(small)
    said = "\n".join(bim.summarise(model, bim.measures_of(model), show_source=False))
    assert "2 more name none of their own but reference a measure that does" in said


@needs_dpm2
def test_a_reference_to_one_cell_is_written_out_in_words(monkeypatch, small):
    """A measure that is itself a sum of several is not a cell, so it stays as written and
    the list below the formula says what it holds."""
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    measures = bim.by_name(bim.measures_of(bim.read(small)))
    said = bim.in_words("DIVIDE ( [One cell], [Two cells] )", bim.published(None), measures=measures)
    assert "«C 28.00 (COREP) ·" in said, said
    assert "[Two cells]" in said, "a measure of two cells is not one cell"


@needs_dpm2
def test_the_tool_follows_the_references_and_says_which(monkeypatch, small):
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    monkeypatch.setenv("BIM_ROOT", str(small.parent))
    answered = bim.explain_bim_measure("Model.bim", "A ratio of other measures")
    assert answered["found"] is True
    assert [c["through"] for c in answered["coordinates"]] == [["One cell"], ["Two cells"], ["Two cells"]]
    # The second: C 28.00's row 999 is an open table and has no label by design, which is
    # a fact about the template rather than a coordinate that failed to resolve.
    assert answered["coordinates"][1]["row_label"], "the cell was resolved, not only reached"
    assert all(c["in_release"] for c in answered["coordinates"])


@needs_dpm2
def test_a_measure_that_reaches_nothing_says_so(monkeypatch, small):
    monkeypatch.setenv("DPM2_DB", str(DPM2_DB))
    measures = bim.by_name(bim.measures_of(bim.read(small)))
    said = "\n".join(bim.explain_measure(measures["No cell at all"], bim.published(None), None, measures=measures))
    assert "nor in any measure it references" in said
