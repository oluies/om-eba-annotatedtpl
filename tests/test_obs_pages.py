"""What the Observable template pages read, checked against what the publish writes.

The pages query the published tree by URL, which is what makes the release a control
rather than a build - and which also means nothing checks the two halves against each
other. A page naming a table that is not published, or a partition that is not there, is
a page that renders with every cell blank and no error on it. That failure cost hours in
this work, twice, and it is the shape these tests exist for.

Everything here reads source files. The database is needed only for the two tests that
look at what the change tables actually contain.
"""

import json
import re
import subprocess
from pathlib import Path

import gen_wasm_data as gen
import pytest

from conftest import DPM2_DB, needs_dpm2

REPO = Path(__file__).resolve().parent.parent
OBS = REPO / "obs"
PAGE = OBS / "src" / "t" / "[code].md"

# `at(release, `cells/framework=${framework}/data_0.parquet`)` and `'${base}x.csv'`.
PARQUET = re.compile(r"at\(release, `([a-z_]+)(/framework=\$\{framework\})?/?[^`]*`\)")
CSV = re.compile(r"\$\{base\}([a-z_]+\.csv)")


def page() -> str:
    return PAGE.read_text(encoding="utf-8")


def published() -> dict[str, str | None]:
    """Every table the publish writes, and what it is partitioned by."""
    return {table.name: table.partition_by for table in gen.TABLES}


def test_the_page_reads_only_tables_the_publish_writes():
    """A table that is not published is a 404 inside DuckDB, which surfaces as a page
    where the cells below it never run - not as a missing table."""
    read = {found.group(1) for found in PARQUET.finditer(page())}
    assert read, "the page reads no parquet at all, which cannot be right"
    unknown = read - set(published())
    assert not unknown, f"the page reads {sorted(unknown)}, which gen_wasm_data does not write"


def test_a_partitioned_table_is_read_with_its_partition():
    """Reading `cells/data_0.parquet` where the publish wrote `cells/framework=X/...`
    finds nothing. Reading a partition of an unpartitioned table finds nothing either."""
    layout = published()
    for found in PARQUET.finditer(page()):
        table, partition = found.group(1), found.group(2)
        if layout[table] == "framework":
            assert partition, f"{table} is partitioned by framework and is read without one"
        else:
            assert not partition, f"{table} is not partitioned and is read as if it were"


def test_the_page_reads_only_wording_files_that_exist():
    """The three CSVs are committed, and the workflow copies them into the published
    tree. A rename on one side is silent on the other."""
    for name in {found.group(1) for found in CSV.finditer(page())}:
        here = REPO / "source" / name
        assert here.exists(), f"the page reads {name}, which is not in source/"


def test_the_wording_files_have_the_columns_the_page_selects():
    """`SELECT row, en, sv, de, celex, "from"` against a CSV with other headers is a
    binder error, and a binder error in one cell stops every cell under it."""
    wanted = {
        "its_labels.csv": {"template", "row", "en", "sv", "de", "celex", "from"},
        "its_instructions.csv": {"template", "row", "en", "sv", "celex"},
        "its_label_changes.csv": {"template", "row", "celex", "en"},
    }
    for name, columns in wanted.items():
        header = (REPO / "source" / name).read_text(encoding="utf-8").splitlines()[0]
        present = set(header.split(","))
        assert columns <= present, f"{name} is missing {sorted(columns - present)}"


def test_every_partition_of_every_table_is_named_data_0():
    """Not a wish - a hazard, pinned so that a change to it is a decision.

    DuckDB names every partition's file `data_0.parquet`, so `cells/framework=FINREP/`
    and `cell_members/framework=COREP/` collide on the basename. Observable's attachment
    handling does key on the basename: `cells` came back as the three columns it shares
    with `cell_members`, with a binder error naming a column plainly in the file. The
    pages read URLs to avoid it, and anything else that consumes this tree should know.
    """
    for table in gen.TABLES:
        statement = gen.copy_statement(table, Path("/tmp/x"))
        if table.partition_by:
            assert "PARTITION_BY" in statement
            assert statement.count(f"/{table.name}'") == 1, "the directory is the only name it gets"


def test_the_catalogue_loader_is_wired_to_the_config():
    """observablehq.config.js reads the catalogue to decide which pages exist, and the
    loader writes it. They are two files that have to agree on one name."""
    config = (OBS / "observablehq.config.js").read_text(encoding="utf-8")
    helper = (OBS / "src" / "data" / "known.js").read_text(encoding="utf-8")
    loader = (OBS / "src" / "data" / "catalogue.json.sh").read_text(encoding="utf-8")
    assert "known.js" in config, "the config reads the helper"
    assert "catalogue.json" in helper, "the helper reads what the loader writes"
    assert "_catalogue.py" in loader, "the loader runs the script that writes it"


def test_the_build_writes_the_catalogue_before_building():
    """dynamicPaths is read when the config loads, which is before any data loader has
    run - so a build that leaves it to the loader produces a site with no template pages
    and no error. That is why build.sh is two steps."""
    script = (OBS / "build.sh").read_text(encoding="utf-8")
    wrote = script.index("catalogue.json.sh")
    built = script.index("observable build")
    assert wrote < built, "the catalogue has to exist before the config is read"


def test_a_missing_catalogue_is_a_site_with_no_pages_not_a_broken_build():
    """A fresh checkout has no catalogue.json. The config still has to load."""
    helper = OBS / "src" / "data" / "known.js"
    got = subprocess.run(
        [
            "node",
            "--input-type=module",
            "-e",
            f"import {{templates}} from {json.dumps(str(helper))};console.log(JSON.stringify(templates().length));",
        ],
        capture_output=True,
        text=True,
        cwd=OBS,
    )
    assert got.returncode == 0, got.stderr
    assert got.stdout.strip().isdigit(), got.stdout


def ask(name: str, wrapper: str) -> list[tuple]:
    """Run a published table's own SQL, with the release window bound as the publish
    binds it - the `?` in these statements is that window, not a caller's filter."""
    import duckdb

    table = gen.lookup(name)
    with duckdb.connect(str(DPM2_DB), read_only=True) as con:
        return con.execute(wrapper.format(sql=table.sql), gen.release_parameters(table, None)).fetchall()


@needs_dpm2
def test_the_change_table_counts_what_a_template_reports():
    """moved and shared are counts of this template's own datapoints, so neither can
    exceed the number of them. A join that fanned out would break this first."""
    rows = ask("template_changes", "SELECT datapoints, moved, shared FROM ({sql}) LIMIT 400")
    assert rows, "the change table is empty, which no release should be"
    for datapoints, moved, shared in rows:
        assert 0 <= moved <= datapoints
        assert 0 <= shared <= datapoints


@needs_dpm2
def test_a_relabelled_row_really_has_more_than_one_wording():
    """The table exists to say that a row's wording changed. A row listed with one
    wording is noise on a page whose whole point is that the change is invisible."""
    counts = ask(
        "relabelled",
        "SELECT count(DISTINCT label) FROM ({sql}) GROUP BY table_code, header_id LIMIT 400",
    )
    assert counts, "no reworded rows at all, which contradicts the DPM"
    assert all(found[0] > 1 for found in counts), "a row listed as reworded has one wording"


@needs_dpm2
def test_two_rows_sharing_a_code_are_not_a_rewording():
    """C_17.01.a serves 0080 from two headers - TOTAL EVENT TYPES and Total recovery from
    insurance - and grouping on the code called that a rewording. The row is the header."""
    rows = ask(
        "relabelled",
        "SELECT DISTINCT label FROM ({sql}) WHERE table_code = 'C_17.01.a' AND row_code = '0080'",
    )
    wordings = {found[0] for found in rows}
    assert wordings, "C_17.01.a row 0080 was reworded in 4.0 and should be here"
    assert not any("TOTAL EVENT TYPES" in found for found in wordings), (
        "a different row that shares the code has been listed as a rewording of this one"
    )


def test_the_tables_the_change_tests_name_exist():
    """So that a rename turns those two into a failure rather than a skip."""
    with pytest.raises(KeyError):
        gen.lookup("not_a_table")
    for name in ("template_changes", "relabelled"):
        assert gen.lookup(name).name == name


def test_the_page_never_displays_an_empty_template():
    """An empty html template literal evaluates to null, and display(null) writes the
    word "null" onto the page - which is how it appeared on C_09.01.b between the labels
    and the instructions. Nothing is displayed by not calling display.

    The needle is built rather than written, so this docstring does not match itself.
    """
    needle = "html" + "``"
    assert needle not in page(), "an empty html template reaches display as null"


def test_optional_sections_tolerate_a_missing_table():
    """A partition that holds nothing is not written: no FINREP template has a reworded
    row, so relabelled/framework=FINREP/ does not exist, and DuckDB answers a missing
    file by throwing. Through db.query that killed every cell on every FINREP page."""
    source = page()
    assert "const maybe = async" in source, "the tolerant reader is gone"
    optional = ["wording", "spelled", "reworded", "drift", "reworded_rows", "dimensions", "checks"]
    for name in optional:
        assert f"const {name} = await maybe(" in source, f"{name} reads without tolerating an absent table"
    assert "const grid = await db.query(" in source, "the grid is not optional and should still throw"


def test_no_query_reads_a_file_over_http():
    """Pages serves the parquet gzipped, and then the content-length it reports is the
    compressed length while a byte range comes from the uncompressed file. DuckDB-WASM
    reads the footer where it was told the end is and answers "No magic bytes found at end
    of file" - and since the CDN may hold either variant, the same code made every FINREP
    page lose its dimensions while the COREP pages passed. fetch() decompresses, so each
    file is fetched once and registered as a buffer.
    """
    source = page()
    assert "registerFileBuffer" in source, "the page no longer hands DuckDB the bytes"
    for reach in ("FROM '${at(", "FROM '${base}"):
        assert reach not in source, f"a query reads {reach}…, which is DuckDB over HTTP again"


def test_an_absent_table_is_iterable():
    """Inputs.table and Inputs.search take something iterable, and an object carrying a
    numRows is not one: a failed read put "TypeError: e is not iterable" on the page where
    the dimensions table belongs."""
    source = page()
    assert "Object.assign([]" in source, "the placeholder for an absent table is not an array"
