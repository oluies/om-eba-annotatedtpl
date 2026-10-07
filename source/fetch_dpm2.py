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


def mdb(accdb: Path, *args: str) -> str:
    try:
        return subprocess.run([*args, str(accdb)], capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        raise SystemExit(f"{args[0]} is not on PATH - install mdbtools 1.0+ (brew install mdbtools)") from None


def table_names(accdb: Path) -> tuple[str, ...]:
    return tuple(filter(None, (line.strip() for line in mdb(accdb, "mdb-tables", "-1").splitlines())))


def export(accdb: Path, names: Iterable[str], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name in names:
        (out / f"{name}.csv").write_text(mdb(accdb, "mdb-export", name))


def load(csv_dir: Path, names: Iterable[str], db: Path) -> dict[str, int]:
    """One DuckDB table per Access table, types sniffed over the whole file.

    Sniffing the whole file rather than a sample matters here: the model is full of codes
    like '01.01' and '0010' that a short sample can read as numbers. Over the full file
    every Code column in the 4.2.1 release comes out VARCHAR, which is what they are.
    """
    db.unlink(missing_ok=True)
    con = duckdb.connect(str(db))
    counts = {}
    for name in names:
        con.execute(
            f'CREATE TABLE "{name}" AS SELECT * FROM read_csv(?, sample_size=-1, header=true)',
            [str(csv_dir / f"{name}.csv")],
        )
        counts[name] = con.execute(f'SELECT count(*) FROM "{name}"').fetchone()[0]
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
    if force or not CSV_DIR.exists():
        print(f"exporting {len(names)} tables", file=sys.stderr)
        export(ACCDB, names, CSV_DIR)

    counts = load(CSV_DIR, names, DB)
    size = DB.stat().st_size / 1e6
    print(f"{DB}: {len(counts)} tables, {sum(counts.values())} rows ({size:.0f} MB)")


if __name__ == "__main__":
    main()
