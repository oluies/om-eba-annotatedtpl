"""Apply the EBA's between-release validation rule updates to a local DPM database.

A DPM release is a snapshot. Between releases the EBA deactivates rules, reactivates
them and changes severities, and publishes each batch as a SQL script on the validation
rules packages page:

    https://www.eba.europa.eu/risk-and-data-analysis/reporting/reporting-frameworks/validation-rules-packages

    uv run source/apply_vr_updates.py <file-or-url>            # report, change nothing
    uv run source/apply_vr_updates.py <file-or-url> --commit   # apply it
    uv run source/apply_vr_updates.py <file-or-url> --db path/to/dpm2.duckdb

The script is read and parsed, never executed. It arrives as SQL over the internet, and
handing that to a database is how a dictionary acquires a statement nobody read. Only one
statement shape is recognised - `UPDATE OperationScope SET IsActive, Severity,
FromSubmissionDate WHERE OperationScopeID IN (...)` - and a file containing anything else
is refused rather than partly applied.

What it changes is `OperationScope`, which is what `lookup_dpm_rule` and the rule lists
read for `active` and `severity`. The database is a derived local file and gitignored, so
patching it is safe; `source/fetch_dpm2.py` rebuilds it from the download.
"""

import argparse
import os
import re
import zipfile
from datetime import date
from io import BytesIO
from pathlib import Path
from typing import NamedTuple

import duckdb
import httpx

REPO = Path(__file__).resolve().parent.parent
DIR = Path(os.environ.get("DPM2_DIR") or REPO / "source" / "dpm2")
DB = Path(os.environ.get("DPM2_DB") or DIR / "dpm2.duckdb")

# The one statement this understands, written as the EBA writes it. Anchored at both ends
# so a line with anything else in it does not match a prefix of itself and slip through.
UPDATE = re.compile(
    r"^UPDATE\s+OperationScope\s+SET\s+IsActive\s*=\s*(?P<active>[01])\s*,"
    r"\s*Severity\s*=\s*'(?P<severity>[A-Za-z]+)'\s*,"
    r"\s*FromSubmissionDate\s*=\s*'(?P<from>\d{2}/\d{2}/\d{4})'"
    r"\s*WHERE\s+OperationScopeID\s+IN\s*\((?P<ids>[\d,\s]+)\)\s*;?$",
    re.IGNORECASE | re.DOTALL,
)


class Update(NamedTuple):
    """One statement: a state, and the scopes to put into it."""

    active: bool
    severity: str
    from_submission_date: date
    scope_ids: tuple[int, ...]


def statements(text: str) -> list[str]:
    """The file's statements, comments and blank lines dropped. Pure."""
    without_comments = "\n".join(line for line in text.splitlines() if not line.strip().startswith("--"))
    return [statement.strip() for statement in without_comments.split(";") if statement.strip()]


def parse(text: str) -> list[Update]:
    """Every update in the file, or a refusal naming the first thing that is not one.

    Pure, and deliberately strict: this is SQL fetched over the internet, and the only
    safe way to run it is to not run it. A statement that does not match the one shape
    the EBA publishes stops the whole file, because a half-applied batch of rule
    deactivations is worse than none.
    """
    updates = []
    for statement in statements(text):
        found = UPDATE.match(statement)
        if not found:
            raise SystemExit(f"not a statement this applies:\n  {statement[:160]}")
        day, month, year = (int(part) for part in found["from"].split("/"))
        updates.append(
            Update(
                active=found["active"] == "1",
                severity=found["severity"].lower(),
                from_submission_date=date(year, month, day),
                scope_ids=tuple(int(scope) for scope in found["ids"].split(",")),
            )
        )
    return updates


def read_source(source: str) -> str:
    """The script's text, from a path or a URL, unzipped if it needs to be."""
    raw = (
        httpx.get(source, follow_redirects=True, timeout=120).raise_for_status().content
        if source.startswith(("http://", "https://"))
        else Path(source).read_bytes()
    )
    if raw[:2] != b"PK":
        return raw.decode("utf-8-sig", errors="replace")
    with zipfile.ZipFile(BytesIO(raw)) as zf:
        # The EBA zips one script, named .sql in some packages and .txt in others.
        scripts = [m for m in zf.infolist() if m.filename.lower().endswith((".sql", ".txt"))]
        if len(scripts) != 1:
            raise SystemExit(f"expected one .sql or .txt in the zip, found {[m.filename for m in scripts]}")
        return zf.read(scripts[0]).decode("utf-8-sig", errors="replace")


def effect(con: duckdb.DuckDBPyConnection, update: Update) -> dict[str, int]:
    """What this update would change in this database, without changing it.

    `IsActive <> 0` rather than `= 1`: release 4.2.1 stores the Access boolean as -1 and
    later releases as 1, so comparing to 1 reports every active scope in 4.2.1 as about
    to change.
    """
    ids = ", ".join(str(scope) for scope in update.scope_ids)
    present = con.execute(f"SELECT count(*) FROM OperationScope WHERE OperationScopeID IN ({ids})").fetchone()
    settled = con.execute(
        f"SELECT count(*) FROM OperationScope WHERE OperationScopeID IN ({ids}) "
        f"AND (IsActive <> 0) = {update.active} AND lower(Severity) = '{update.severity}'"
    ).fetchone()
    return {
        "asked": len(update.scope_ids),
        "present": present[0] if present else 0,
        "already": settled[0] if settled else 0,
    }


def apply(con: duckdb.DuckDBPyConnection, update: Update) -> int:
    ids = ", ".join(str(scope) for scope in update.scope_ids)
    con.execute(
        "UPDATE OperationScope SET IsActive = ?, Severity = ?, FromSubmissionDate = ? "
        f"WHERE OperationScopeID IN ({ids})",
        [1 if update.active else 0, update.severity, update.from_submission_date],
    )
    changed = con.execute(f"SELECT count(*) FROM OperationScope WHERE OperationScopeID IN ({ids})").fetchone()
    return changed[0] if changed else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="the EBA script: a .sql, .txt or .zip, as a path or a URL")
    parser.add_argument("--db", type=Path, default=DB, help=f"the database to patch (default {DB})")
    parser.add_argument("--commit", action="store_true", help="apply; without it, report and change nothing")
    args = parser.parse_args()

    if not args.db.exists():
        raise SystemExit(f"{args.db} does not exist - run source/fetch_dpm2.py first")
    updates = parse(read_source(args.source))
    con = duckdb.connect(str(args.db), read_only=not args.commit)
    try:
        print(f"{len(updates)} statement(s) against {args.db}")
        missing = 0
        for update in updates:
            counted = effect(con, update)
            missing += counted["asked"] - counted["present"]
            state = "active" if update.active else "deactivated"
            print(
                f"  {state:12} {update.severity:8} from {update.from_submission_date}: "
                f"{counted['asked']:4} scope(s), {counted['present']:4} in this database, "
                f"{counted['already']:4} already there, {counted['present'] - counted['already']:4} to change"
            )
        if missing:
            # A scope the database does not have is a rule from another release, not an
            # error: the scripts are published against the newest DPM, and an older one
            # simply has fewer rules.
            print(f"  {missing} scope id(s) are not in this database - they belong to a later release")
        if not args.commit:
            print("\nnothing changed. Pass --commit to apply.")
            return
        for update in updates:
            apply(con, update)
        con.execute("CHECKPOINT")
        print("\napplied.")
    finally:
        con.close()


if __name__ == "__main__":
    main()
