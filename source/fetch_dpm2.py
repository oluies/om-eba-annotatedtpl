"""Download the EBA DPM 2.0 database and load it into DuckDB.

The pack is built from the annotated table layout, which is one rendering of the model.
This is the model itself: the same cells, plus the validation rules, the hierarchies and
every other framework. A local copy is what lets the pack be checked against its source
rather than against itself - see `source/check_against_dpm2.py`.

    uv run source/fetch_dpm2.py                 # download, convert, load; steps skipped if done
    uv run source/fetch_dpm2.py --force         # redo every step
    uv run source/fetch_dpm2.py --release 4.3   # a second release, beside the first

The default release is the one the pack is built from, so `check_against_dpm2.py` compares
like with like. Another release lands in its own files and its own database - releases are
separate downloads of overlapping content, and merging them would make "which release says
this" unanswerable. Point `DPM2_DB` at whichever one a lookup should read.

Reading the Access file needs mdb-export from mdbtools (`brew install mdbtools`); version
1.0 or newer, because the file is ACE12 and older releases only read Jet .mdb.

Everything lands in source/dpm2/, which is gitignored: 167 MB of zip, 539 MB of Access
and 139 MB of DuckDB are not things to put in a repository.
"""

import argparse
import os
import shutil
import subprocess
import sys
import zipfile
from collections.abc import Iterable
from hashlib import sha256
from pathlib import Path
from typing import NamedTuple

import duckdb
import httpx


class Source(NamedTuple):
    """Where one release of the database comes from, and what it must hash to.

    The sha256 is checked on download. The EBA republishes under the same URL when it
    hotfixes a release, so a mismatch means the upstream file moved on, not that the
    download broke. A release added here starts with an empty hash: the first download
    prints what it got, and that goes in.
    """

    url: str
    sha256: str


# 4.2.1 is the release the pack is built from - the annotated table layout comes from the
# same one, which is what makes the two comparable at all - so it stays the default.
# 4.3 is published on the reporting framework 4.3 page rather than the data dictionary
# page, and from the EBA's blob storage rather than the main site.
DEFAULT_RELEASE = "4.2.1"
SOURCES = {
    "4.2.1": Source(
        url="https://www.eba.europa.eu/sites/default/files/2026-02/ad0d2577-a1eb-4826-a249-a1f7701c6796/DPM2%20Database_v_4_2_1.zip",
        sha256="0d1c0e608c98f01dc338a98e8e5f700c0fa2a2437cbef724fb8fc52618b4b74d",
    ),
    "4.3": Source(
        url="https://ebprstaewspublic01.blob.core.windows.net/public/tools-prod/documents/Big_Files/files/Reporting%20framework%204.3/DPM2%20Database_v%204_3.zip",
        sha256="f2d802f1430879cf085d21e2279630d7a10e1207e2a100ab01188136cf0b2cac",
    ),
    # Reporting framework 4.4, Phase 1. This was the draft technical package when it was
    # first pinned here; the EBA published the final one on 2026-10-12, which is the file
    # recorded below. A package is republished as it is revised, so this hash goes stale;
    # when it does, the file has moved on and the recorded one is the thing to update,
    # deliberately, rather than to drop.
    #
    # It went stale once already, which is the pin earning its keep: the copy taken on
    # 2026-10-17 was 189936198 bytes, and the one published on 2026-10-15 and served from
    # 2026-10-18 is 189939275. Same URL, different file, and nothing but the hash would
    # have said so.
    "4.4": Source(
        url="https://ebprstaewspublic01.blob.core.windows.net/public/tools-prod/assets/Reporting%20Framework/DPM2%20Database_v%204_4.zip",
        sha256="76cffcfe7430ff8fc66c6566bcaf8feb7bf02e48501525212061fcb0eabd96e5",
    ),
}

REPO = Path(__file__).resolve().parent.parent
DIR = Path(os.environ.get("DPM2_DIR") or REPO / "source" / "dpm2")


class Paths(NamedTuple):
    """Where one release lands. Pure function of the release and the directory.

    The default release keeps the unsuffixed names it has always had, so a copy already
    downloaded is not orphaned by this becoming configurable; every other release is
    suffixed and cannot collide with it. DPM2_DB still wins, because a caller pointing at
    one file means it.
    """

    zip: Path
    accdb: Path
    csv_dir: Path
    db: Path
    stamp: Path


def paths_for(release: str, directory: Path = DIR) -> Paths:
    tag = release.replace(".", "_")
    default = release == DEFAULT_RELEASE
    return Paths(
        zip=directory / f"DPM2_Database_v_{tag}.zip",
        accdb=directory / f"dpm2_{tag}.accdb",
        # What the derived files were derived from. Every other step keys on a file
        # existing, so without this a changed download is unpacked and exported past:
        # the zip is new, the .accdb and the CSVs are the old draft's, and the database
        # comes out labelled 4.4 holding the draft before it.
        stamp=directory / f"dpm2_{tag}.accdb.sha256",
        csv_dir=directory / ("csv" if default else f"csv_{tag}"),
        db=Path(os.environ["DPM2_DB"])
        if os.environ.get("DPM2_DB")
        else directory / ("dpm2.duckdb" if default else f"dpm2_{tag}.duckdb"),
    )


# What the rest of the pack imports: the default release's database.
DB = paths_for(DEFAULT_RELEASE).db


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
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--release", default=DEFAULT_RELEASE, choices=sorted(SOURCES), help="which release to fetch")
    parser.add_argument("--force", action="store_true", help="redo every step")
    args = parser.parse_args()

    release = args.release
    source = SOURCES[release]
    here = paths_for(release)
    DIR.mkdir(parents=True, exist_ok=True)

    if args.force or not here.zip.exists():
        print(f"downloading DPM 2.0 database {release}", file=sys.stderr)
        download(source.url, here.zip)
    found = digest(here.zip)
    if not source.sha256:
        # A release whose hash is not recorded yet: print it rather than accept anything
        # silently, so the next run of the same release is checked like every other.
        print(f"{here.zip.name}: sha256 {found} - record it in SOURCES[{release!r}]", file=sys.stderr)
    elif found != source.sha256:
        raise SystemExit(
            f"{here.zip.name}: sha256 {found}, expected {source.sha256}.\n"
            f"  The file at that URL is not the one recorded. Either the EBA republished it - a\n"
            f"  draft is revised in place - in which case record {found} in SOURCES[{release!r}],\n"
            f"  or the download is damaged, in which case delete {here.zip.name} and run again."
        )

    # The derived files are only as current as the download they came from. Everything
    # else here keys on a file existing, so a zip that changed under them has to say so.
    was = here.stamp.read_text(encoding="utf-8").strip() if here.stamp.exists() else ""
    stale = was != found
    if stale and was:
        print(f"the download changed since these were made ({was[:12]} -> {found[:12]}); redoing them", file=sys.stderr)
    here.stamp.unlink(missing_ok=True)

    if args.force or stale or not here.accdb.exists():
        print("unpacking", file=sys.stderr)
        unpack(here.zip, here.accdb)

    names = table_names(here.accdb)
    redo = args.force or stale
    if missing := missing_csvs(names, here.csv_dir):
        print(f"exporting {len(missing)} of {len(names)} tables", file=sys.stderr)
        export(here.accdb, names if redo else missing, here.csv_dir)
    elif redo:
        print(f"re-exporting all {len(names)} tables", file=sys.stderr)
        export(here.accdb, names, here.csv_dir)

    counts = load(here.csv_dir, names, here.db)
    # Written last: a stamp beside half an export would say the derived files are current
    # when they are not, which is the thing it exists to prevent.
    here.stamp.write_text(found + "\n", encoding="utf-8")
    size = here.db.stat().st_size / 1e6
    print(f"{here.db}: {len(counts)} tables, {sum(counts.values())} rows ({size:.0f} MB)")


if __name__ == "__main__":
    main()
