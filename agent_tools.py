"""The tool definitions an agent registers, and the one dispatcher that runs them.

Nine tools, from three modules, assembled here so a host application imports one name
instead of nine and cannot end up with a definition registered but not dispatched:

    lookup_datapoint        resolve a column name to its datapoint, and to the display
                            name to use for it                      (pay42_lookup.py)
    read_table_metadata     what a table and its columns say now
    write_column_metadata   set one column's description, display name and terms
    write_table_metadata    the same for the table itself            (describe_table.py)
    lookup_dpm_table        a template from any framework in the DPM, with its axes
    lookup_dpm_cell         one cell of any template: dimensions, type, rules
    lookup_dpm_dimensions   what a template breaks down by, and under which wording
    lookup_dpm_cells        the cells one dimension member covers - an aggregate's codes
    lookup_dpm_sums         which rows add up to which, from the validation rules
                                                                    (dpm_lookup.py)

Registration, with the OpenAI-shaped tools parameter:

    from agent_tools import TOOLS, dispatch
    response = client.chat.completions.create(model=..., messages=..., tools=list(TOOLS))

Dispatch, from a tool call:

    result = dispatch(call.function.name, call.function.arguments)

`arguments` arrives as a JSON string, not a dict, which is the mistake this function
exists to absorb - it takes either. Every tool here is synchronous and blocks on a socket
or a file, so from an async loop:

    result = await asyncio.to_thread(dispatch, call.function.name, call.function.arguments)

Reading needs `PAY42_DB` to point at the built store; the catalogue tools need `OM_HOST`
and `OM_JWT_TOKEN`; the warehouse enrichment needs `BA_SERVER`. Each tool reports what it
is missing rather than failing the turn.

The two DPM tools are the exception: they need a 139 MB database that a checkout does not
have, so they are registered only when it is there. A tool whose every answer is "not
downloaded" costs a turn and teaches the model to stop calling it. `dispatch` still knows
them either way, so a host that registered them before the file moved does not break.
"""

import datetime
import decimal
import enum
import json
from typing import Any

import describe_table
import dpm_lookup
import pay42_lookup


class ToolName(enum.StrEnum):
    """The names as the definitions spell them. One source, so they cannot drift."""

    LOOKUP_DATAPOINT = pay42_lookup.LOOKUP_DATAPOINT_TOOL_NAME
    READ_TABLE_METADATA = describe_table.READ_TABLE_METADATA_TOOL_NAME
    WRITE_COLUMN_METADATA = describe_table.WRITE_COLUMN_METADATA_TOOL_NAME
    WRITE_TABLE_METADATA = describe_table.WRITE_TABLE_METADATA_TOOL_NAME
    LOOKUP_DPM_TABLE = dpm_lookup.LOOKUP_DPM_TABLE_TOOL_NAME
    LOOKUP_DPM_CELL = dpm_lookup.LOOKUP_DPM_CELL_TOOL_NAME
    LOOKUP_DPM_DIMENSIONS = dpm_lookup.LOOKUP_DPM_DIMENSIONS_TOOL_NAME
    LOOKUP_DPM_CELLS = dpm_lookup.LOOKUP_DPM_CELLS_TOOL_NAME
    LOOKUP_DPM_SUMS = dpm_lookup.LOOKUP_DPM_SUMS_TOOL_NAME


TOOLS = (
    pay42_lookup.LOOKUP_DATAPOINT_TOOL_DEFINITION,
    *describe_table.CATALOGUE_TOOL_DEFINITIONS,
    *(dpm_lookup.DPM_TOOL_DEFINITIONS if dpm_lookup.available() else ()),
)


def jsonable(value: Any) -> Any:
    """The same answer with nothing in it that plain json.dumps refuses.

    A host serialises a tool answer before handing it back to the model, and the obvious
    way to do that is `json.dumps(dispatch(...))` - no `default=`. DuckDB hands back the
    column's own type, so the DPM's module validity window arrives as two datetime.date
    objects and that call raises TypeError, losing the turn rather than the answer. Dates
    become ISO strings, which is how the model reads them anyway; a Decimal becomes a
    float, since every numeric in these answers is a count or an amount, not money being
    added up here.

    `case dict()` and `case list()` are class patterns, not captures, so recursion is on
    shape. datetime.datetime is a subclass of date and isoformat covers both.
    """
    match value:
        case dict():
            return {key: jsonable(item) for key, item in value.items()}
        case list() | tuple():
            return [jsonable(item) for item in value]
        case datetime.date() | datetime.time():
            return value.isoformat()
        case decimal.Decimal():
            return float(value)
        case _:
            return value


def dispatch(name: str, arguments: str | dict[str, Any]) -> dict[str, Any]:
    """Run one tool call and return its answer, ready to be serialised back.

    The `case ToolName.X` arms are dotted names, so they are value patterns rather than
    capture patterns - a bare `case X` would bind every name and match the first arm for
    every tool. The final arm answers rather than raising: an unknown tool name is
    something the model can correct if it is told, and nothing if the turn dies.

    `.get` for the optional arguments. A strict schema requires every property, so they
    arrive as nulls rather than absent, but a model that drops one should not raise a
    KeyError inside the loop.
    """
    try:
        args = json.loads(arguments) if isinstance(arguments, str) else arguments
        return jsonable(_run(name, args))
    except ValueError as exc:
        # JSONDecodeError is a ValueError, but not the only one json.loads raises: an
        # integer literal over 4300 digits trips CPython's conversion limit with a plain
        # ValueError, and that would have escaped a handler written for the subclass.
        return {"error": f"arguments were not usable JSON: {type(exc).__name__}: {exc}"}
    except Exception as exc:  # noqa: BLE001 - a tool failure is a turn the model can still use
        return {"error": f"{name} failed: {type(exc).__name__}: {exc}"}


def _run(name: str, args: dict[str, Any]) -> dict[str, Any]:
    """The dispatch itself, so the error handling above reads as one thing."""
    match name:
        case ToolName.LOOKUP_DATAPOINT:
            return pay42_lookup.lookup_datapoint(args["column_name"], args.get("variant"))
        case ToolName.READ_TABLE_METADATA:
            return describe_table.read_table_metadata(args["table_fqn"])
        case ToolName.WRITE_COLUMN_METADATA:
            return describe_table.write_column_metadata(
                args["table_fqn"],
                args["column_name"],
                args.get("description"),
                args.get("display_name"),
                args.get("expect_current"),
                args.get("terms"),
            )
        case ToolName.WRITE_TABLE_METADATA:
            return describe_table.write_table_metadata(
                args["table_fqn"],
                args.get("description"),
                args.get("display_name"),
                args.get("expect_current"),
            )
        case ToolName.LOOKUP_DPM_TABLE:
            return dpm_lookup.lookup_dpm_table(args["table"])
        case ToolName.LOOKUP_DPM_CELL:
            return dpm_lookup.lookup_dpm_cell(args["table"], args["row"], args["column"], args.get("sheet"))
        case ToolName.LOOKUP_DPM_DIMENSIONS:
            return dpm_lookup.lookup_dpm_dimensions(args["table"], args.get("module"), args.get("version"))
        case ToolName.LOOKUP_DPM_CELLS:
            return dpm_lookup.lookup_dpm_cells(
                args["table"], args["dimension"], args["member"], args.get("module"), args.get("version")
            )
        case ToolName.LOOKUP_DPM_SUMS:
            return dpm_lookup.lookup_dpm_sums(args["table"], args["module"], args.get("version"))
        case _:
            return {
                "error": f"no such tool: {name}",
                "available": [tool.value for tool in ToolName],
            }


if __name__ == "__main__":
    # Prints the definitions, so what the model will be shown can be read before it is.
    print(json.dumps({"tools": list(TOOLS)}, ensure_ascii=False, indent=2))
