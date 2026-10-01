"""The tool definitions an agent registers, and the one dispatcher that runs them.

Four tools, from two modules, assembled here so a host application imports one name
instead of four and cannot end up with a definition registered but not dispatched:

    lookup_datapoint        resolve a column name to its datapoint, and to the display
                            name to use for it                      (pay42_lookup.py)
    read_table_metadata     what a table and its columns say now
    write_column_metadata   set one column's description, display name and terms
    write_table_metadata    the same for the table itself            (describe_table.py)

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
"""

import enum
import json
from typing import Any

import describe_table
import pay42_lookup


class ToolName(enum.StrEnum):
    """The names as the definitions spell them. One source, so they cannot drift."""

    LOOKUP_DATAPOINT = pay42_lookup.LOOKUP_DATAPOINT_TOOL_NAME
    READ_TABLE_METADATA = describe_table.READ_TABLE_METADATA_TOOL_NAME
    WRITE_COLUMN_METADATA = describe_table.WRITE_COLUMN_METADATA_TOOL_NAME
    WRITE_TABLE_METADATA = describe_table.WRITE_TABLE_METADATA_TOOL_NAME


TOOLS = (pay42_lookup.LOOKUP_DATAPOINT_TOOL_DEFINITION, *describe_table.CATALOGUE_TOOL_DEFINITIONS)


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
    except json.JSONDecodeError as exc:
        return {"error": f"arguments were not JSON: {exc}"}

    try:
        return _run(name, args)
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
        case _:
            return {
                "error": f"no such tool: {name}",
                "available": [tool.value for tool in ToolName],
            }


if __name__ == "__main__":
    # Prints the definitions, so what the model will be shown can be read before it is.
    print(json.dumps({"tools": list(TOOLS)}, ensure_ascii=False, indent=2))
