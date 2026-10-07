"""Where the two derived stores are, and when a test that needs one has to be skipped.

Nothing here touches a network or a real server.

`pay42.duckdb` and the DPM 2.0 database are both derived and gitignored, so a fresh
checkout has neither. Tests that need one skip with the command that builds it: `pytest`
on a clone should report what it could check, not a wall of errors about a file the
repository never promised.

The paths are taken from the modules that read them rather than resolved again here. That
matters for `PAY42_DB`, which `pay42_lookup` reads through pydantic-settings and so also
picks up from a `.env` file; resolving it with `os.environ` alone meant a store configured
there was found by the lookup and reported as missing by the skip condition - silent loss
of coverage rather than a visible failure.
"""

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))  # the pack's modules live at the repository root
sys.path.insert(0, str(REPO / "source"))  # and the generators in source/, imported for their pure parts

# After the path setup, necessarily: these are the modules it exists to make importable.
import dpm_lookup  # noqa: E402
import pay42_lookup  # noqa: E402

PAY42_DB = pay42_lookup.DB
DPM2_DB = dpm_lookup.DB

needs_store = pytest.mark.skipif(
    not PAY42_DB.exists(), reason="pay42.duckdb is derived; build it with source/build_duckdb.py"
)
needs_dpm2 = pytest.mark.skipif(
    not DPM2_DB.exists(), reason="the DPM 2.0 database is a 139 MB download; source/fetch_dpm2.py"
)
