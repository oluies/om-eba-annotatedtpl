# Source this to set the pack's environment and see what it resolved to.
#
#     source env.sh                      # the defaults for a local checkout
#     source env.sh --release 4.4        # the DPM 2.0 database of another release
#     source env.sh --quiet              # set without the report
#
# Sourced, not run: it has to change the calling shell, so there is no shebang, no `exit`
# and no `set -e` - a failed command in a sourced script with `set -e` closes the
# terminal. Works in bash and zsh.
#
# It sets only what has a safe local default: the two DuckDB stores and the DPM download
# directory. Secrets and hostnames are reported, never assigned - a committed file that
# sets OM_JWT_TOKEN is a committed file that leaks it, and a default SQL Server host is a
# wrong host. Put those in your shell profile, a private file, or `.env` where the tool
# reads one.
#
# The report is the point. Every variable the pack reads, what it is set to, whether that
# is yours or the default, and for a path whether it exists - because the failures worth
# a debug log here are a lookup reading an empty store, and a datapoint id that does not
# resolve because DPM2_DB points at a release that predates it.

_pack_release=""
_pack_quiet=""
while [ $# -gt 0 ]; do
  case "$1" in
    --release) _pack_release="$2"; shift 2 ;;
    --release=*) _pack_release="${1#*=}"; shift ;;
    --quiet|-q) _pack_quiet=1; shift ;;
    *) echo "env.sh: unknown argument $1" >&2; shift ;;
  esac
done

# The directory this file sits in, which is the repo root. $BASH_SOURCE in bash, ${(%):-%x}
# in zsh; $0 is the shell's own name when sourced, so it cannot be used.
if [ -n "${BASH_SOURCE:-}" ]; then
  _pack_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
elif [ -n "${ZSH_VERSION:-}" ]; then
  _pack_root="$(cd "$(dirname "${(%):-%x}")" && pwd)"
else
  _pack_root="$(pwd)"
fi

export PAY42_DB="${PAY42_DB:-$_pack_root/pay42.duckdb}"
export DPM2_DIR="${DPM2_DIR:-$_pack_root/source/dpm2}"

if [ -n "$_pack_release" ]; then
  # 4.2.1 is the default release and keeps the unsuffixed name; every other release is
  # suffixed. This mirrors paths_for() in source/fetch_dpm2.py, which is what writes them.
  if [ "$_pack_release" = "4.2.1" ]; then
    export DPM2_DB="$DPM2_DIR/dpm2.duckdb"
  else
    export DPM2_DB="$DPM2_DIR/dpm2_$(echo "$_pack_release" | tr . _).duckdb"
  fi
else
  export DPM2_DB="${DPM2_DB:-$DPM2_DIR/dpm2.duckdb}"
fi

# --- the report -------------------------------------------------------------------------

_pack_row() {
  # name, and how to describe the value: path | secret | plain
  _name="$1"; _kind="${2:-plain}"
  eval "_value=\"\${$_name-}\""
  if [ -z "${_value}" ]; then
    printf '  %-28s %s\n' "$_name" "- unset"
    unset _name _kind _value
    return
  fi
  case "$_kind" in
    secret)
      printf '  %-28s %s\n' "$_name" "set, ${#_value} characters (not shown)" ;;
    path)
      if [ -e "$_value" ]; then
        # -s, or a directory prints one line per entry inside it and the report
        # grows a paragraph where it wanted a size.
        _size="$(du -sh "$_value" 2>/dev/null | cut -f1 | tr -d '[:space:]')"
        printf '  %-28s %s\n' "$_name" "$_value  [$_size]"
      else
        printf '  %-28s %s\n' "$_name" "$_value  [DOES NOT EXIST]"
      fi ;;
    *)
      printf '  %-28s %s\n' "$_name" "$_value" ;;
  esac
  unset _name _kind _value _size
}

pack_env() {
  echo "pack: $_pack_root"
  echo
  echo "PAY 4.2 store"
  _pack_row PAY42_DB path
  _pack_row PAY42_TEMP_DIR path
  _pack_row PAY42_EXTENSION_DIR path
  _pack_row PAY42_MEMORY_LIMIT
  echo
  echo "DPM 2.0 database"
  _pack_row DPM2_DIR path
  _pack_row DPM2_DB path
  # Which release that file actually is, which no variable says and every unresolved
  # datapoint id depends on. Skipped when the database is absent or duckdb is not here.
  if [ -f "${DPM2_DB:-}" ] && command -v uv >/dev/null 2>&1; then
    uv run --project "$_pack_root" python -c "
import sys, duckdb
try:
    con = duckdb.connect(sys.argv[1], read_only=True)
    releases = [row[1] for row in con.execute('SELECT ReleaseID, Code FROM Release ORDER BY ReleaseID').fetchall()]
    highest = con.execute('SELECT max(VariableID) FROM VariableVersion').fetchone()[0]
    print(f'  {\"\":28} releases {\", \".join(releases)}; highest datapoint id {highest}')
except Exception as exc:
    print(f'  {\"\":28} not readable as a DPM database: {type(exc).__name__}')
" "$DPM2_DB" 2>/dev/null
  fi
  echo
  echo "OpenMetadata"
  _pack_row OM_HOST
  _pack_row OM_JWT_TOKEN secret
  _pack_row OM_CA_BUNDLE path
  _pack_row OM_PAGE_URL
  _pack_row OM_GLOSSARY
  echo
  echo "Warehouse (ba_form_cell.py)"
  _pack_row BA_SERVER
  _pack_row BA_DATABASE
  _pack_row BA_TABLE
  _pack_row BA_AXIS_TABLE
  _pack_row BA_TRUSTED_CONNECTION
  _pack_row BA_USERNAME
  _pack_row BA_PASSWORD secret
  _pack_row BA_DRIVER
  _pack_row BA_ENCRYPT
  _pack_row BA_TRUST_SERVER_CERTIFICATE
  _pack_row BA_DEBUG
  echo
  echo "SQL Server target (source/load_to_mssql.py)"
  _pack_row MSSQL_SERVER
  _pack_row MSSQL_PORT
  _pack_row MSSQL_DATABASE
  _pack_row MSSQL_SCHEMA
  _pack_row MSSQL_DB_SCHEMA
  _pack_row MSSQL_TRUSTED_CONNECTION
  _pack_row MSSQL_USERNAME
  _pack_row MSSQL_PASSWORD secret
  _pack_row MSSQL_ENCRYPT
  _pack_row MSSQL_TRUST_SERVER_CERTIFICATE
  echo
  echo "unset is not an error: each tool falls back to its default and says what it is"
  echo "missing. Re-run this report any time with: pack_env"
}

[ -n "$_pack_quiet" ] || pack_env

unset _pack_release _pack_quiet
