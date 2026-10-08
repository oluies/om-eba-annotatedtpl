"""Download the EBA DPM 2.0 database and load it into DuckDB.

The pack is built from the annotated table layout, which is one rendering of the model.
This is the model itself: the same cells, plus the validation rules, the hierarchies and
every other framework. A local copy is what lets the pack be checked against its source
rather than against itself - see `source/check_against_dpm2.py`.

    uv run source/fetch_dpm2.py          # download, convert, load; each step skipped if done
    uv run source/fetch_dpm2.py --force  # redo every step

Reading the Access file needs mdb-export from mdbtools (`brew install mdbtools`); version
1.0 or newer, because the file is ACE12 and older releases only read Jet .mdb.

Everything lands in source/dpm2/, which is gitignored: 167 MB of zip, 539 MB of Access
and 139 MB of DuckDB are not things to put in a repository.
"""

import os
import shutil
import subprocess
import sys
import zipfile
from collections.abc import Iterable
from hashlib import sha256
from pathlib import Path

import duckdb
import httpx

# Reporting framework 4.2.1, linked from the DPM data dictionary page as "DPM 2.0 database".
# The annotated table layout the pack is built from comes from the same release, which is
# what makes the two comparable at all.
RELEASE = "4.2.1"
URL = "https://www.eba.europa.eu/sites/default/files/2026-02/ad0d2577-a1eb-4826-a249-a1f7701c6796/DPM2%20Database_v_4_2_1.zip"
# Checked on download. The EBA republishes under the same URL when it hotfixes a release,
# so a mismatch means the upstream file moved on, not that the download broke.
ZIP_SHA256 = "0d1c0e608c98f01dc338a98e8e5f700c0fa2a2437cbef724fb8fc52618b4b74d"

REPO = Path(__file__).resolve().parent.parent
DIR = Path(os.environ.get("DPM2_DIR") or REPO / "source" / "dpm2")
ZIP = DIR / f"DPM2_Database_v_{RELEASE.replace('.', '_')}.zip"
ACCDB = DIR / f"dpm2_{RELEASE.replace('.', '_')}.accdb"
CSV_DIR = DIR / "csv"
DB = Path(os.environ.get("DPM2_DB") or DIR / "dpm2.duckdb")


def digest(path: Path, chunk: int = 1 << 20) -> str:
    h = sha256()
    with path.open("rb") as fh:
        while block := fh.read(chunk):
            h.update(block)
    return h.hexdigest()


def download(url: str, target: Path) -> None:
    """Stream to a sibling .part first, so an interrupted run leaves no half file behind."""
    part = target.with_suffix(target.suffix + ".part")
    target.parent.mkdir(parents=True, exist_ok=True)
    with httpx.stream("GET", url, follow_redirects=True, timeout=120) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        with part.open("wb") as fh:
            for block in response.iter_bytes(1 << 20):
                fh.write(block)
                if total:
                    print(f"\r  {fh.tell() / 1e6:6.0f} / {total / 1e6:.0f} MB", end="", file=sys.stderr)
    print(file=sys.stderr)
    part.replace(target)


def unpack(archive: Path, target: Path) -> None:
    """The zip holds one .accdb under a name with spaces in it; give it a plain one."""
    with zipfile.ZipFile(archive) as zf:
        (member,) = [m for m in zf.infolist() if m.filename.lower().endswith(".accdb")]
        with zf.open(member) as src, target.open("wb") as dst:
            shutil.copyfileobj(src, dst, 1 << 20)


def mdb(*argv: str) -> bytes:
    """Run one mdbtools command and return its stdout as the bytes it produced.

    Bytes, not text: `text=True` turns on universal newlines, which rewrites a carriage
    return inside a quoted field. One such field in `Category` made the export a byte
    shorter than what mdbtools wrote, and silently rewriting a value in a regulatory
    dictionary is not a trade worth making for the convenience of a str.

    The whole argv rather than a path appended to it, because the two commands want the
    file in different places: `mdb-tables -1 <file>` but `mdb-export <file> <table>`.
    Appending it worked for the first and silently produced nothing for the second.

    And the exit code is not the signal. `mdb-export` given arguments it cannot use
    writes to stderr, leaves stdout empty and exits 0, so anything on stderr is a failure.
    """
    try:
        done = subprocess.run(argv, capture_output=True, check=True)
    except FileNotFoundError:
        raise SystemExit(f"{argv[0]} is not on PATH - install mdbtools (brew install mdbtools)") from None
    if done.stderr.strip():
        raise SystemExit(f"{' '.join(argv)}\n  {done.stderr.decode(errors='replace').strip()}")
    return done.stdout


def table_names(accdb: Path) -> tuple[str, ...]:
    listed = mdb("mdb-tables", "-1", str(accdb)).decode("utf-8")
    return tuple(filter(None, (line.strip() for line in listed.splitlines())))


def missing_csvs(names: Iterable[str], out: Path) -> list[str]:
    """Which tables have no export yet. Pure, and the only thing that decides whether to
    export: that the directory exists says nothing about whether the export finished."""
    return [name for name in names if not (out / f"{name}.csv").exists()]


def export(accdb: Path, names: Iterable[str], out: Path) -> None:
    """One CSV per table, each written to a .part first and renamed when complete.

    An interrupted run used to leave a truncated file that looked finished, and a run
    interrupted before the first table left an empty directory that the old guard read as
    "already exported" - which surfaced as DuckDB failing to find a CSV it was told to read.
    """
    out.mkdir(parents=True, exist_ok=True)
    wanted = list(names)
    for n, name in enumerate(wanted, 1):
        part = out / f"{name}.csv.part"
        exported = mdb("mdb-export", str(accdb), name)
        if not exported.strip():
            raise SystemExit(f"mdb-export produced nothing for {name}")
        part.write_bytes(exported)
        part.replace(out / f"{name}.csv")
        if n % 20 == 0 or n == len(wanted):
            print(f"  exported {n}/{len(wanted)}", file=sys.stderr)
    if left := missing_csvs(wanted, out):
        raise SystemExit(f"export did not produce: {', '.join(left[:5])}")


def load(csv_dir: Path, names: Iterable[str], db: Path) -> dict[str, int]:
    """One DuckDB table per Access table, types sniffed over the whole file.

    Sniffing the whole file rather than a sample matters here: the model is full of codes
    like '01.01' and '0010' that a short sample can read as numbers. Over the full file
    every Code column in the 4.2.1 release comes out VARCHAR, which is what they are.
    """
    if absent := missing_csvs(names, csv_dir):
        raise SystemExit(f"no export for {', '.join(absent[:5])} in {csv_dir} - re-run, or pass --force")
    db.unlink(missing_ok=True)
    con = duckdb.connect(str(db))
    counts = {}
    for name in names:
        con.execute(
            f'CREATE TABLE "{name}" AS SELECT * FROM read_csv(?, sample_size=-1, header=true)',
            [str(csv_dir / f"{name}.csv")],
        )
        counted = con.execute(f'SELECT count(*) FROM "{name}"').fetchone()
        counts[name] = counted[0] if counted else 0
    con.execute("CHECKPOINT")
    con.close()
    return counts


def main() -> None:
    force = "--force" in sys.argv[1:]
    DIR.mkdir(parents=True, exist_ok=True)

    if force or not ZIP.exists():
        print(f"downloading DPM 2.0 database {RELEASE}", file=sys.stderr)
        download(URL, ZIP)
    found = digest(ZIP)
    if found != ZIP_SHA256:
        raise SystemExit(f"{ZIP.name}: sha256 {found}, expected {ZIP_SHA256} - upstream file has changed")

    if force or not ACCDB.exists():
        print("unpacking", file=sys.stderr)
        unpack(ZIP, ACCDB)

    names = table_names(ACCDB)
    if missing := missing_csvs(names, CSV_DIR):
        print(f"exporting {len(missing)} of {len(names)} tables", file=sys.stderr)
        export(ACCDB, missing if not force else names, CSV_DIR)
    elif force:
        print(f"re-exporting all {len(names)} tables", file=sys.stderr)
        export(ACCDB, names, CSV_DIR)

    counts = load(CSV_DIR, names, DB)
    size = DB.stat().st_size / 1e6
    print(f"{DB}: {len(counts)} tables, {sum(counts.values())} rows ({size:.0f} MB)")


if __name__ == "__main__":
    main()
