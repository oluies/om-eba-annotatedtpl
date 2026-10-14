"""The sourceable environment script.

Two properties matter and neither is obvious from reading it: that sourcing it leaves the
calling shell with the variables set, and that the report never prints a secret. Both are
checked by actually sourcing it in a subshell, because a shell script is exactly the kind
of file where reading it and running it disagree.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

ENV_SH = Path(__file__).resolve().parent.parent / "env.sh"
SHELLS = [shell for shell in ("bash", "zsh") if shutil.which(shell)]


def source(script: str, shell: str = "bash", env: dict[str, str] | None = None) -> str:
    """Source env.sh in a fresh shell, then run `script`, and return what it printed."""
    done = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh --quiet && {script}"],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(Path.home()), **(env or {})},
    )
    return done.stdout.strip()


@pytest.mark.parametrize("shell", SHELLS)
def test_sourcing_it_leaves_the_stores_set(shell):
    assert source("echo $PAY42_DB", shell).endswith("/pay42.duckdb")
    assert source("echo $DPM2_DB", shell).endswith("/source/dpm2/dpm2.duckdb")
    assert source("echo $DPM2_DIR", shell).endswith("/source/dpm2")


@pytest.mark.parametrize("shell", SHELLS)
def test_a_release_picks_the_file_that_release_was_loaded_into(shell):
    """The names mirror paths_for() in source/fetch_dpm2.py: the default release keeps the
    unsuffixed one, every other release is suffixed."""
    out = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh --quiet --release 4.4 && echo $DPM2_DB"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert out.endswith("/dpm2_4_4.duckdb")

    default = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh --quiet --release 4.2.1 && echo $DPM2_DB"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert default.endswith("/dpm2.duckdb")


@pytest.mark.parametrize("shell", SHELLS)
def test_a_variable_already_set_is_left_alone(shell):
    """Sourcing this must not overrule a caller who has already chosen - that is how a
    release pinned for one shell would quietly become the default again."""
    chosen = "/somewhere/else/mine.duckdb"
    assert source("echo $DPM2_DB", shell, env={"DPM2_DB": chosen}) == chosen
    assert source("echo $PAY42_DB", shell, env={"PAY42_DB": "/mine/pay.duckdb"}) == "/mine/pay.duckdb"


@pytest.mark.parametrize("shell", SHELLS)
def test_the_release_flag_overrules_an_inherited_database(shell):
    """Asking for a release and getting whatever was in the environment would be worse
    than either, so --release is the one thing that does overrule it."""
    out = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh --quiet --release 4.4 && echo $DPM2_DB"],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin", "DPM2_DB": "/stale/dpm2.duckdb"},
    ).stdout.strip()
    assert out.endswith("/dpm2_4_4.duckdb")


@pytest.mark.parametrize("shell", SHELLS)
def test_a_secret_is_counted_and_never_printed(shell):
    """The report exists to be pasted into a bug report. A token in it is a leaked token."""
    secret = "jwt-aaaaaaaaaaaaaaaaaaaaaaaa"  # noqa: S105 - a fixture, not a credential
    report = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh"],
        capture_output=True,
        text=True,
        env={
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "HOME": str(Path.home()),
            "OM_JWT_TOKEN": secret,
            "MSSQL_PASSWORD": secret,
            "BA_PASSWORD": secret,
        },
    ).stdout
    assert secret not in report
    assert report.count(f"set, {len(secret)} characters (not shown)") == 3


@pytest.mark.parametrize("shell", SHELLS)
def test_a_path_that_is_not_there_says_so(shell):
    """A lookup reading an empty store is the failure this report is for."""
    report = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh"],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(Path.home()), "PAY42_DB": "/nope/absent.duckdb"},
    ).stdout
    assert "/nope/absent.duckdb  [DOES NOT EXIST]" in report


@pytest.mark.parametrize("shell", SHELLS)
def test_an_unknown_argument_is_named_and_the_rest_still_runs(shell):
    """Sourced, not run: it cannot exit, because exiting closes the caller's terminal."""
    done = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh --quiet --nonsense && echo $DPM2_DB"],
        capture_output=True,
        text=True,
    )
    assert "unknown argument --nonsense" in done.stderr
    assert done.stdout.strip().endswith(".duckdb")
