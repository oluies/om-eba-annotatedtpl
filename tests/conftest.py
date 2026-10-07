"""Shared fixtures. Nothing here touches a network or a real server.

Two of the pack's data stores are derived and gitignored, so a fresh checkout has
neither. Tests that need one are skipped rather than failed: `pytest` on a clone with no
`pay42.duckdb` should report what it could check, not a wall of errors about a file the
repository never promised.
"""

import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))  # the pack's modules live at the repository root
sys.path.insert(0, str(REPO / "source"))  # and the generators in source/, imported for their pure parts

# The same environment variables the code reads, so a store that has been moved is found
# here too - and so these conditions can be exercised by pointing them at nothing.
PAY42_DB = Path(os.environ.get("PAY42_DB") or REPO / "pay42.duckdb")
DPM2_DIR = Path(os.environ.get("DPM2_DIR") or REPO / "source" / "dpm2")
DPM2_DB = Path(os.environ.get("DPM2_DB") or DPM2_DIR / "dpm2.duckdb")

needs_store = pytest.mark.skipif(
    not PAY42_DB.exists(), reason="pay42.duckdb is derived; build it with source/build_duckdb.py"
)
needs_dpm2 = pytest.mark.skipif(
    not DPM2_DB.exists(), reason="the DPM 2.0 database is a 139 MB download; source/fetch_dpm2.py"
)


@pytest.fixture
def catalogue(monkeypatch):
    """A fake OpenMetadata, as a factory taking the handler and returning the recorded calls.

    `describe_table.client` is the one place the real client is built, so replacing it is
    enough to redirect every path - the CLI and the agent tools alike.
    """
    import httpx

    import describe_table

    monkeypatch.setenv("OM_HOST", "http://om.test/api")
    monkeypatch.setenv("OM_JWT_TOKEN", "test")

    def build(handler):
        monkeypatch.setattr(
            describe_table,
            "client",
            lambda settings: httpx.Client(base_url="http://om.test/api", transport=httpx.MockTransport(handler)),
        )
        return describe_table

    return build
