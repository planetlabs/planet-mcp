"""
This is the entry point for a local MCP server and when the package
is installed, this is installed as an executable named planet-mcp.
"""

from fastmcp import FastMCP
import planet
from planet_mcp.server import MCPService

# note - the mcp dev tooling (e.g. uv run fastmcp dev src/main.py)
# wants to find a server object named `mcp` (or it won't work)
mcp = FastMCP("Planet local/stdio MCP")
sess = planet.Session()
svc = MCPService(mcp=mcp, session=sess)


# this is the entry point for the executable script installed via package
# and also supports execution via `uv run fastmcp run src/main.py`
def main():
    svc.mcp.run(transport="stdio")
