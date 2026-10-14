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


# --- the env file -----------------------------------------------------------------------


def with_env_file(
    contents: str,
    script: str,
    shell: str,
    tmp: Path,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Source env.sh against a written env file, then run `script`."""
    path = tmp / "sample.env"
    path.write_text(contents, encoding="utf-8")
    done = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh --quiet --env-file {path} && {script}"],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(Path.home()), **(env or {})},
    )
    return done


@pytest.mark.parametrize("shell", SHELLS)
def test_a_pair_in_the_file_reaches_the_shell(shell, tmp_path):
    done = with_env_file("OM_GLOSSARY=PAY_4_2\n", "echo $OM_GLOSSARY", shell, tmp_path)
    assert done.stdout.strip() == "PAY_4_2"


@pytest.mark.parametrize("shell", SHELLS)
def test_the_environment_wins_over_the_file(shell, tmp_path):
    """pydantic-settings' own precedence, so exporting a variable for one command still
    overrides the file rather than being silently replaced by it."""
    done = with_env_file(
        "OM_GLOSSARY=from_file\n", "echo $OM_GLOSSARY", shell, tmp_path, env={"OM_GLOSSARY": "from_shell"}
    )
    assert done.stdout.strip() == "from_shell"


@pytest.mark.parametrize("shell", SHELLS)
def test_the_file_wins_over_the_defaults_here(shell, tmp_path):
    """DPM2_* is read with os.environ and never reaches pydantic-settings, so the file is
    the only place a release can be pinned without exporting it by hand."""
    done = with_env_file("DPM2_DB=/chosen/dpm2_4_4.duckdb\n", "echo $DPM2_DB", shell, tmp_path)
    assert done.stdout.strip() == "/chosen/dpm2_4_4.duckdb"


@pytest.mark.parametrize("shell", SHELLS)
@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("OM_GLOSSARY=plain\n", "plain"),
        ('OM_GLOSSARY="double"\n', "double"),
        ("OM_GLOSSARY='single'\n", "single"),
        ("export OM_GLOSSARY=exported\n", "exported"),
        ("OM_GLOSSARY = spaced \n", "spaced"),
        ('OM_GLOSSARY="  kept  "\n', "  kept  "),  # inside the quotes is the value
        ("# OM_GLOSSARY=commented\n", ""),
        ("OM_GLOSSARY\n", ""),  # not a pair
        ("1BAD=x\nOM_GLOSSARY=after\n", "after"),  # an unusable name does not stop the file
    ],
)
def test_the_file_is_read_rather_than_executed(shell, line, expected, tmp_path):
    """`source .env` would run whatever is in it, and a file holding a password is the
    last one to hand a shell. So these are parsed, and only as NAME=VALUE."""
    done = with_env_file(line, 'printf "[%s]" "$OM_GLOSSARY"', shell, tmp_path)
    assert done.stdout.strip() == f"[{expected}]"


@pytest.mark.parametrize("shell", SHELLS)
def test_a_value_is_never_expanded(shell, tmp_path):
    """$HOME in a value is four characters, not the home directory - and a value holding
    `$(rm -rf ~)` is a string, which is the property that matters."""
    done = with_env_file("OM_PAGE_URL=$HOME/x\n", "echo $OM_PAGE_URL", shell, tmp_path)
    assert done.stdout.strip() == "$HOME/x"


@pytest.mark.parametrize("shell", SHELLS)
def test_the_report_says_where_a_value_came_from(shell, tmp_path):
    path = tmp_path / "sample.env"
    path.write_text("OM_GLOSSARY=from_file\nOM_HOST=from_file\n", encoding="utf-8")
    done = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh --env-file {path}"],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(Path.home()), "OM_HOST": "from_shell"},
    )
    assert f"env file: {path} - 1 taken, 1 already set and left alone" in done.stdout
    assert "OM_GLOSSARY                  from_file  (.env)" in done.stdout
    assert "OM_HOST                      from_shell\n" in done.stdout, "no (.env) on a value the shell gave"


@pytest.mark.parametrize("shell", SHELLS)
def test_no_env_file_ignores_one_that_is_there(shell, tmp_path):
    path = tmp_path / "sample.env"
    path.write_text("OM_GLOSSARY=from_file\n", encoding="utf-8")
    done = subprocess.run(
        [
            shell,
            "-c",
            # printf, not `echo [$X]`: in zsh an empty variable leaves a bare [] that the
            # shell tries to glob and fails on before the test ever sees it.
            f'cd {ENV_SH.parent} && source ./env.sh --no-env-file --env-file {path} && printf "[%s]" "$OM_GLOSSARY"',
        ],
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin"},
    )
    assert done.stdout.strip().endswith("[]")


@pytest.mark.parametrize("shell", SHELLS)
def test_a_named_file_that_is_missing_is_said_out_loud(shell, tmp_path):
    """An absent default .env is the normal case and says nothing; one the caller named
    and misspelled is a mistake worth hearing about."""
    done = subprocess.run(
        [shell, "-c", f"cd {ENV_SH.parent} && source ./env.sh --quiet --env-file {tmp_path}/absent.env"],
        capture_output=True,
        text=True,
    )
    assert "no such env file" in done.stderr
