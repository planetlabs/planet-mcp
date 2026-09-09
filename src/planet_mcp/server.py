from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastmcp import FastMCP

from planet_mcp import servers

_instructions = """
Instructions for using Planet's official MCP server.
"""


class PlanetContext:
    def __init__(self):
        pass


def _lifespan(context: PlanetContext):

    @asynccontextmanager
    async def lifespan(server: FastMCP) -> AsyncIterator[PlanetContext]:
        yield context

    return lifespan


def init(
    enabled_servers: set[str] | None = None,
    include_tags: set[str] | None = None,
    exclude_tags: set[str] | None = None,
) -> FastMCP:

    context = PlanetContext()

    mcp = FastMCP(
        "Planet MCP Server",
        lifespan=_lifespan(context),
        instructions=_instructions,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
    )

    for server in servers.all:
        try:
            # server protocol is either a variable or callable named mcp
            entry = server.mcp
        except AttributeError:
            raise AttributeError(
                f"programmer error, mcp attribute not in {server}"
            ) from None
        if callable(entry):
            entry = entry()
        if not isinstance(entry, FastMCP):
            raise TypeError(
                f"programmer error, expected FastMCP type, got {type(entry)}"
            )
        if enabled_servers is None or entry.name in enabled_servers:
            mcp.mount(entry, entry.name)  # type: ignore

    return mcp
