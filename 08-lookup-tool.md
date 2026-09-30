# Adding the lookup as an agent tool

`pay42_lookup.py` resolves a warehouse column name to its datapoint without anyone
counting rows on a page. Wiring it in takes three steps.

## 1. Build the store

```bash
uv sync
uv run source/build_duckdb.py
```

`pay42.duckdb` is derived and gitignored. Rebuild it after `gen_pack.py`; the lookup
refuses to run without it rather than answering from a stale file.

## 2. Register the tool

`LOOKUP_DATAPOINT_TOOL_DEFINITION` is the function schema, in strict mode. Add it to the
list the agent sends as `tools`:

```python
from pay42_lookup import LOOKUP_DATAPOINT_TOOL_DEFINITION

TOOLS = [
    *EXISTING_TOOLS,
    LOOKUP_DATAPOINT_TOOL_DEFINITION,
]
```

## 3. Dispatch it

Add a branch wherever local tool calls are executed - the counterpart to whatever
handles the MCP ones. The exact place depends on the app; in a Chainlit loop it is the
function the message handler calls for non-MCP tools.

**The model sends `arguments` as a JSON string, not a dict.** Parse it before use:

```python
import json

from pay42_lookup import LOOKUP_DATAPOINT_TOOL_NAME, lookup_datapoint

tool_name = raw_tool_call["function"]["name"]
arguments = json.loads(raw_tool_call["function"].get("arguments") or "{}")

match tool_name:
    case LOOKUP_DATAPOINT_TOOL_NAME:
        # strict mode always sends variant, as null when the table does not fix one.
        output = lookup_datapoint(arguments["column_name"], arguments["variant"])
    case _:
        ...
```

If the app already has a helper that parses the argument string - something like
`parse_args(raw_tool_call["function"].get("arguments", "{}"))` - use that instead of
`json.loads`, so the branch behaves like every other tool.

`lookup_datapoint` is synchronous and reads a local file, so it needs no await and no
client. It returns a dict; serialise it the same way the other tool outputs are.

## What it answers

With a variant, the resolved datapoint. Without one, the fields common to all six plus
the six candidates, and a message saying not to state a datapoint id or a unit - those
are exactly what differs. It never picks a variant on its own.

For a name that resolves to nothing it says so and repeats the pattern, so a context
column like `Period_SK` comes back as a refusal rather than a guess.

## Joining to the warehouse's own form metadata

`05-datapoints.csv` carries `dpm_cell_code` in the shape `{{Y 01.01, r0010, c0010, s0010}}`,
which is what a warehouse holding its own form metadata keys on. At FI that is
`FIDW_BI.dbo.BA_Form_Cell`, and the two sides supply different things:

| From the warehouse | From this pack |
|---|---|
| the warehouse's own datapoint key | EBA's VariableVID |
| data type, presentation format | the dimension members |
| Form_BK, Taxonomy_Name, the open-axis names | the glossary terms |
| every form it holds | PAY 4.2 and DORA |

`ba_form_cell.py` does that join when `BA_SERVER` is set, using Kerberos - no credentials
in the connection string, the ticket from `kinit` carries the identity:

```bash
kinit
export BA_SERVER=your-sql-server
uv run pay42_lookup.py Y0101_r0010_c0010
```

It scopes to `Current_flg = 1`, the definition in force. A cell code present under
several current forms is reported rather than resolved, because the column means
different things in each and only the table's own `Form_BK` says which applies.

Without `BA_SERVER` the pack answers on its own, which is what an agent with no database
access gets. The enrichment never fails a lookup: a database that is down produces a note
in the answer, not an error.

**The SQL has not been run against the real table.** Treat the first run as a test and
check the column names.

## Where the files go

DuckDB reads no environment variables of its own - every directory is a `SET` or a
connection config - so these are ours, with the usual `PAY42_` prefix and `.env` support:

| Variable | Default | What it moves |
|---|---|---|
| `PAY42_DB` | `pay42.duckdb` beside the module | the store itself |
| `PAY42_TEMP_DIR` | `<db>.tmp` | scratch files when a query spills |
| `PAY42_EXTENSION_DIR` | `~/.duckdb/extensions` | downloaded extensions |
| `PAY42_MEMORY_LIMIT` | 80% of RAM | how much it may hold before spilling |

The build script honours `PAY42_DB` and `PAY42_TEMP_DIR` too, so a build and a read
cannot disagree about the path.

`SET temp_directory` does the same job and works on a read-only connection, but it is
global to the database instance: a `SET` in one connection changes the setting for every
other one in the process, including connections opened afterwards. The lookup therefore
passes `config=` at connect time, which stays scoped to that call. The build script uses
`SET`, which is harmless in a one-shot process.

Two of these matter outside a developer checkout. Scratch files land next to the
database by default, so a read-only mount holding the store has nowhere to spill;
`PAY42_TEMP_DIR` fixes that. And in a container without a writable home, extension
downloads fail unless `PAY42_EXTENSION_DIR` points somewhere real - though this lookup
loads no extensions, so that only bites if you query the file yourself.

## Two notes on the store

Compression is automatic and per column; DuckDB chooses Dictionary for these strings and
there is no maximum to turn up. The block size is what matters at this size - the 256 KiB
default rounds a 1830-row database up past the CSV it came from, so the build uses 16 KiB
and a CHECKPOINT, which brings it to about 490 KiB with the indexes.

The same file answers ad-hoc SQL, which is often quicker than asking an agent:

```bash
duckdb pay42.duckdb -c "SELECT * FROM datapoints WHERE row_label ILIKE '%fraud%' LIMIT 5"
duckdb pay42.duckdb -c "SELECT term_fqn FROM column_terms WHERE column_name = 'Y0101_r0020_c0010'"
```
