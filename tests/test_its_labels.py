"""The parsing of the Official Journal, without fetching 63 MB of it.

The fixtures below are the shape the real document has, cut down to the few rows that
each distinguish a case. What they are not is a sample of the real thing: for that,
`uv run source/fetch_its_labels.py --report` reads the real document and says what it
made of it.
"""

import fetch_its_labels as its

TEMPLATE = """
<p class="oj-ti-grseq-1">C 01.00 - OWN FUNDS (CA1)</p>
<table><tr><td><p>Rows</p></td><td><p>ID</p></td><td><p>Amount</p></td></tr>
<tr><td><p>OWN FUNDS</p></td><td><p>0010</p></td><td><p>1</p></td></tr>
<tr><td><p>TIER 1 CAPITAL</p></td><td><p>0015</p></td><td><p>1.1</p></td></tr></table>
<p class="oj-ti-grseq-1">C 02.00 - OWN FUNDS REQUIREMENTS (CA2)</p>
<table><tr><td><p>TOTAL RISK EXPOSURE AMOUNT</p></td><td><p>0010</p></td></tr></table>
"""

SWEDISH = """
<p class="oj-ti-grseq-1">C 01.00 – KAPITALBAS (CA1)</p>
<table><tr><td><p>Rader</p></td><td><p>ID</p></td><td><p>Belopp</p></td></tr>
<tr><td><p>KAPITALBAS</p></td><td><p>0010</p></td><td><p>1</p></td></tr>
<tr><td><p>PRIM&#196;RKAPITAL</p></td><td><p>0015</p></td><td><p>1.1</p></td></tr></table>
<p class="oj-ti-grseq-1">C 02.00 – KAPITALBASKRAV (CA2)</p>
<table><tr><td><p>TOTALT RISKVÄGT EXPONERINGSBELOPP</p></td><td><p>0010</p></td></tr></table>
"""


def test_a_row_belongs_to_the_heading_above_it():
    """Row 0010 exists in nearly every template, so a row without its template is not a
    coordinate at all - which is what parsing the tables alone produces."""
    found = [row for row in its.rows(TEMPLATE) if row.code]
    assert [(row.template, row.code, row.text) for row in found] == [
        ("C_01.00", "0010", "OWN FUNDS"),
        ("C_01.00", "0015", "TIER 1 CAPITAL"),
        ("C_02.00", "0010", "TOTAL RISK EXPOSURE AMOUNT"),
    ]


def test_a_heading_is_recognised_whichever_dash_it_uses():
    """A hyphen in the templates, an en dash in the instructions, and not consistently
    the same one across languages."""
    assert its.rows("<p>C 01.00 - OWN FUNDS</p><table><tr><td>x</td></tr></table>")[0].template == "C_01.00"
    assert its.rows("<p>C 01.00 – OWN FUNDS</p><table><tr><td>x</td></tr></table>")[0].template == "C_01.00"
    assert its.rows("<p>F 18.00.a - Information</p><table><tr><td>x</td></tr></table>")[0].template == "F_18.00.a"


def test_a_numbered_section_is_not_a_template_heading():
    """`1.2. C 01.00 – OWN FUNDS (CA1)` heads the instructions, not a template, and
    treating it as one attributes the prose tables to the template."""
    assert its.rows("<p>1.2. C 01.00 - OWN FUNDS</p><table><tr><td>x</td></tr></table>")[0].template is None


def test_the_languages_are_joined_without_asking_them_where_a_row_belongs():
    """English attributes; the others only say what a row reads. Joining on (template,
    row) per language instead loses coverage - 2027 rows against 2499 - because the
    heading that announces a template is typeset differently in each one."""
    labels, counts = its.aligned({"en": its.rows(TEMPLATE), "sv": its.rows(SWEDISH)})
    assert labels == [
        {"template": "C_01.00", "row": "0010", "en": "OWN FUNDS", "sv": "KAPITALBAS"},
        {"template": "C_01.00", "row": "0015", "en": "TIER 1 CAPITAL", "sv": "PRIMÄRKAPITAL"},
        {
            "template": "C_02.00",
            "row": "0010",
            "en": "TOTAL RISK EXPOSURE AMOUNT",
            "sv": "TOTALT RISKVÄGT EXPONERINGSBELOPP",
        },
    ]
    assert counts["unpaired"] == 0


def test_two_extra_rows_in_one_language_do_not_refuse_the_document():
    """The 2021 text had the same 13 838 table rows in every language; the 2024
    consolidation does not - German has two the others lack - and position-for-position
    refused the whole document over them. A sequence match absorbs them as an insertion."""
    padded = SWEDISH.replace(
        "<table><tr><td><p>TOTALT RISKVÄGT EXPONERINGSBELOPP</p></td><td><p>0010</p></td></tr></table>",
        "<table><tr><td><p>en rubrikrad</p></td></tr>"
        "<tr><td><p>TOTALT RISKVÄGT EXPONERINGSBELOPP</p></td><td><p>0010</p></td></tr></table>",
    )
    labels, counts = its.aligned({"en": its.rows(TEMPLATE), "sv": its.rows(padded)})
    assert counts["unpaired"] == 0
    assert [row["row"] for row in labels] == ["0010", "0015", "0010"]
    assert labels[-1]["sv"] == "TOTALT RISKVÄGT EXPONERINGSBELOPP"


def test_a_row_that_pairs_with_nothing_is_dropped_not_shifted():
    """Two of 7 768 rows are out of step in the real document. A label hung on the wrong
    row is worse than a missing one, because nothing downstream can tell."""
    shifted = SWEDISH.replace("<p>0015</p>", "<p>0017</p>")
    labels, counts = its.aligned({"en": its.rows(TEMPLATE), "sv": its.rows(shifted)})
    assert counts["unpaired"] == 1
    assert all(row["row"] != "0015" for row in labels)


def test_the_consolidations_are_listed_newest_last():
    """`newest` picks what the build reads. The bare CELEX is the act as adopted - the
    2021 text, five years behind the releases it is matched against - and asking for it
    by accident is how 2024's wording went missing."""
    found = its.CONSOLIDATIONS[its.CELEX]
    assert found == sorted(found), "oldest first, so the last is the newest"
    assert its.newest(its.CELEX) == found[-1]
    assert its.newest("32099R9999") == "32099R9999", "an act with no consolidation is itself"


def test_comparing_labels_looks_past_numbering_and_dashes():
    """The Journal numbers a label and the model does not, and they disagree about which
    dash. Neither is a different row."""
    assert its.normal("1.1.1 Capital instruments") == its.normal("Capital instruments")
    assert its.normal("Past due – 30 days") == its.normal("Past due - 30 days")
    assert its.normal("OWN FUNDS") == its.normal("Own funds")
    assert its.normal("Cash on hand") != its.normal("Cash at bank")


FINREP_ANNEX = """
<p>ANNEX III</p>
<p>FINREP TEMPLATES FOR IFRS</p>
<table>
<tr><td><p>TEMPLATE NUMBER</p></td><td><p>TEMPLATE CODE</p></td><td><p>NAME</p></td></tr>
<tr><td><p>1.1</p></td><td><p>F 01.01</p></td><td><p>Balance Sheet Statement: assets</p></td></tr>
<tr><td><p>1.2</p></td><td><p>F 01.02</p></td><td><p>Balance Sheet Statement: liabilities</p></td></tr>
</table>
<p>1. Balance Sheet Statement [Statement of Financial Position]</p>
<p>1.1 Assets</p>
<table><tr><td><p>Cash, cash balances at central banks</p></td><td><p>0010</p></td></tr></table>
<p>1.2 Liabilities</p>
<table><tr><td><p>Deposits</p></td><td><p>0010</p></td></tr></table>
"""


def test_a_finrep_template_is_found_through_the_annex_index():
    """FINREP does not head a template with its code the way COREP does: Annex III has an
    index of number, code and name, and then heads each template with the number alone."""
    found = [row for row in its.rows(FINREP_ANNEX) if row.code and row.text]
    assert [(row.template, row.code, row.text) for row in found] == [
        ("F_01.01", "0010", "Cash, cash balances at central banks"),
        ("F_01.02", "0010", "Deposits"),
    ]


def test_an_index_row_is_not_a_reportable_row():
    """It carries a template number beside a template code, which is a contents page.
    Emitted as a label it would put `Balance Sheet Statement: assets` at row 0010."""
    assert not [row for row in its.rows(FINREP_ANNEX) if row.text and "NAME" in (row.text or "")]
    assert all(row.text != "Balance Sheet Statement: assets" for row in its.rows(FINREP_ANNEX))


def test_the_same_number_means_different_templates_in_different_annexes():
    """1 is C 01.00 in Annex I and 1.1 is F 01.01 in Annex III. One map shared between
    them answers the wrong template, which is why the index is kept per annex."""
    both = """
    <p>ANNEX I</p>
    <table><tr><td><p>1</p></td><td><p>C 01.00</p></td><td><p>Own funds</p></td></tr></table>
    <p>1. Own funds</p>
    <table><tr><td><p>OWN FUNDS</p></td><td><p>0010</p></td></tr></table>
    <p>ANNEX III</p>
    <table><tr><td><p>1</p></td><td><p>F 01.01</p></td><td><p>Assets</p></td></tr></table>
    <p>1. Assets</p>
    <table><tr><td><p>Cash on hand</p></td><td><p>0010</p></td></tr></table>
    """
    found = [(row.template, row.text) for row in its.rows(both) if row.code and row.text]
    assert found == [("C_01.00", "OWN FUNDS"), ("F_01.01", "Cash on hand")]


def test_an_annex_boundary_forgets_the_template_in_force():
    """Otherwise the first rows of a new annex are attributed to the last template of the
    one before it, which is how a COREP label ends up on a FINREP row."""
    found = its.rows("<p>C 01.00 - Own funds</p><p>ANNEX III</p><table><tr><td>x</td></tr></table>")
    assert found[0].template is None


def test_a_variant_knows_which_template_it_varies():
    assert its.stem_of("C_75.01.a") == "C_75.01"
    assert its.stem_of("C_75.01.w") == "C_75.01"
    assert its.stem_of("C_75.01") is None


def test_a_numbered_sub_template_is_not_a_variant():
    """F 04.02.1 and F 04.02.2 have their own codes in the Journal's index; they are not
    two variants of an F 04.02, and there is usually no F 04.02 to take a grid from."""
    assert its.stem_of("F_04.02.1") is None
    assert its.stem_of("F_04.02.2") is None


INSTRUCTIONS = """
<p>ANNEX II</p>
<p>1.2. C 01.00 – OWN FUNDS (CA1)</p>
<table>
<tr><td><p>Row</p></td><td><p>Legal references and instructions</p></td></tr>
<tr><td><p>0010</p></td><td><p>1. Own funds Article 72 CRR The own funds are the sum.</p></td></tr>
<tr><td><p>0015</p></td><td><p>1.1. Tier 1 capital Article 25 CRR The Tier 1 capital is a sum.</p></td></tr>
</table>
"""


def test_the_instructions_annex_heads_a_template_with_number_and_code():
    """`1.2. C 01.00 – OWN FUNDS (CA1)`, which the template annex never writes and which
    the label parser refuses on purpose - the prose tables are not a template's grid."""
    found = [row for row in its.instruction_rows(INSTRUCTIONS) if row.text]
    assert [(row.template, row.code) for row in found] == [("C_01.00", "0010"), ("C_01.00", "0015")]
    assert (found[0].text or "").startswith("1. Own funds Article 72 CRR")


def test_a_short_second_cell_is_not_an_instruction():
    """A heading row or a continuation. Taking it would put `Own funds` where a
    definition belongs, which reads as a definition."""
    short = INSTRUCTIONS.replace("1. Own funds Article 72 CRR The own funds are the sum.", "Own funds")
    assert [row.code for row in its.instruction_rows(short) if row.text] == ["0015"]


def test_the_label_parser_still_refuses_the_instructions_heading():
    """Both parsers read the same document. If HEADING accepted `1.2. C 01.00 – ...` the
    prose tables would be attributed to the template as if they were its rows."""
    assert all(row.template is None for row in its.rows(INSTRUCTIONS))


def test_instructions_are_numbered_over_the_same_stream_as_labels():
    """Both emit a Row per table row whether or not it carries anything, which is what
    lets the languages align by position in either mode."""
    assert len(its.instruction_rows(INSTRUCTIONS)) == len(its.rows(INSTRUCTIONS))
