#!/usr/bin/env bash
# Observable runs a .py loader with whatever `python3` is on PATH, which has no duckdb.
# This runs the same script through uv, so the catalogue comes from the project's
# environment - the same one the tests and the generators use.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
exec uv run --group docs --project "$here/../../.." python "$here/_catalogue.py"
