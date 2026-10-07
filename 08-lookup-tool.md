# Adding the lookup as an agent tool

`pay42_lookup.py` resolves a warehouse column name to its datapoint without anyone
counting rows on a page. Wiring it in takes three steps.

## 1. Build the store

```bash
uv sync
uv run source/build_duckdb.py
```

`pay42.duckdb` is derived and gitignored. **Rebuild it after every pull**: a pull brings
new code and new CSVs but leaves the old database in place, and a field added since it
was built is missing from it. The lookup checks for that and says to run the line above
rather than failing somewhere unhelpful. Rebuild it after `gen_pack.py`; the lookup
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

Or skip all of it: `agent_tools.py` in this pack is this dispatch for every tool here -
the lookup, the catalogue writers and the two DPM lookups - with `TOOLS` to register and
`dispatch(name, arguments)` to call. It takes `arguments` as either the string or a parsed dict, and it never raises.

`lookup_datapoint` is synchronous and reads a local file, so it needs no await and no
client. It returns a dict; serialise it the same way the other tool outputs are.

## What it answers

With a variant, the resolved datapoint. Without one, the fields common to all six plus
the six candidates, and a message saying not to state a datapoint id or a unit - those
are exactly what differs. It never picks a variant on its own.

For a name that resolves to nothing it says so and repeats the pattern, so a context
column like `Period_SK` comes back as a refusal rather than a guess.

Either way the answer carries `validation_rules`: the EBA validation rules that reach the
cell, each with its code, its severity and its DPM-XL expression verbatim. With a variant
given, the rules belonging to the other variants are dropped rather than listed. Without
one, a rule that reaches only some variants carries a `variants` key saying which.

Put the codes in a description, not the expressions - `02-agent-instructions.md` says why.

## Two more tools, for the rest of the DPM

`lookup_dpm_table` and `lookup_dpm_cell` read the EBA DPM 2.0 database itself, so they
answer for COREP, FINREP, resolution, ESG and every other framework in it - everything
`lookup_datapoint` correctly refuses. `agent_tools.TOOLS` includes them only when the
database has been downloaded, because a tool whose every answer is "not downloaded" costs
a turn and teaches the model to stop calling it:

```bash
uv run source/fetch_dpm2.py     # 167 MB download, then 539 MB of Access, then DuckDB
uv run dpm_lookup.py C_01.00    # the same answers, from the command line
```

`dispatch` knows both names whether or not they are registered, so a host that registered
them before the file moved gets an explanation rather than an exception.

## The warehouse's own form metadata, where there is one

`05-datapoints.csv` carries two keys a warehouse's form metadata also keys on:
`dpm_cell_code` in the shape `{{Y 01.01, r0010, c0010, s0010}}`, and `column_name` in the
shape `Y0101_r0010_c0010`. At FI the metadata is `FIDW_BI.dbo.BA_Form_Cell`, joined to
`dbo.BA_Form_Axis` on `Cell_sk`. Where it is reachable it is the primary source and this
pack is an overlay on it:

| From the warehouse | From this pack |
|---|---|
| form, taxonomy version, row and column labels | the dimension members |
| data type and the warehouse's own datapoint key | EBA's VariableVID |
| the open-axis values a column actually carries | the glossary terms |
| every form it holds | PAY 4.2 and DORA |

The split follows from what each side can know. The warehouse knows which release a cell
is current under and which variants a physical column holds; it cannot say what a
dimension member means. This pack is the other way round. So the warehouse states the
facts and the pack supplies the meaning, joined on `dpm_cell_code`.

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

### Which variant, answered from the database

A `.01` template has six variants and a column name that names none of them. Connected,
the tool stops guessing: `BA_Form_Axis` enumerates the `Open_Axis_value_1` values defined
for that physical column and returns them as `open_axis_values`. The warehouse stores
`Row_Column_Code` with a suffix the column name does not carry, so that lookup is a
prefix `LIKE` - with the underscores escaped, since in `LIKE` an underscore matches any
single character and these column names are full of them. Every one of them is in
that column, as rows, so a column description covers all of them and still must not name
a datapoint id or a unit - those belong to the row.

Unconnected, the tool returns the `determining_the_variant` hint instead and the agent
settles it through OpenMetadata, which is the best an agent with no database can do.

### Only where the taxonomy matches

`BA_Form_Cell` spans 33 taxonomy names, from `DPM_2.6` to `DPM_4.2`. The same cell code
can mean something else in each, so every answer carries a `pack_overlay` line saying
whether this pack's ids may be attached at all. Where the warehouse has the cell under a
release this pack does not describe, the overlay is left off rather than asserted: the
warehouse fields on their own are still a correct description, and a datapoint id
borrowed across releases is simply wrong.

### Did it actually reach SQL Server

Every answer says, in a `warehouse` field, which of the three happened:

| `warehouse` | Meaning |
|---|---|
| `not consulted - BA_SERVER is not set` | the pack answered alone |
| `no row in BA_Form_Cell for this key with Current_flg = 1` | it queried and found nothing |
| `BA_Form_Cell joined to BA_Form_Axis on <server>` | it queried and matched |
| `warehouse_lookup_failed: ...` | it tried and the query or the connection failed |

Silence would read the same as a miss, so there is none.

To test the connection on its own, before trusting any lookup, or to ask it about one
column or one cell code directly:

```bash
kinit
BA_SERVER=your-sql-server uv run ba_form_cell.py
BA_SERVER=your-sql-server uv run ba_form_cell.py Y0101_r0010_c0010
```

### Seeing the statement that ran

`BA_DEBUG=1` logs every statement the module sends, with its parameters filled in, so the
exact query can be pasted into SSMS when an answer looks wrong. It logs the row count and
the cells it folded them into as well - zero cells and six cells are both plausible
answers to the same query, and that is where the difference shows:

```bash
BA_DEBUG=1 BA_SERVER=your-sql-server uv run ba_form_cell.py Y0101_r0010_c0010
```

The log goes to stderr and the answer to stdout, so the JSON can still be piped. What
executes is the parameterised statement; the rendering is for reading. In a host
application, enable logging for the `ba_form_cell` logger instead of setting the variable.

It reports the server, the table, `SUSER_SNAME()` - who Kerberos authenticated you as -
and how many current cells the table holds. A failure comes back with the reason rather
than a traceback.

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
