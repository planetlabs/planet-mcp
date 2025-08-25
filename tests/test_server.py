import pytest
from fastmcp import FastMCP, Client


@pytest.fixture
def test_server():
    mcp = FastMCP("Planet MCP Test Server")

    ## a very simple "search" test
    @mcp.tool
    def search(item_type: str) -> dict:
        items = {"PSScene": 123, "SkySat": 456, "Tanager": 789}
        return {"item_type": item_type, "temp": items.get(item_type)}

    return mcp


@pytest.mark.asyncio
async def test_search_tool(test_server):
    async with Client(test_server) as client:
        result = await client.call_tool("search", {"item_type": "SkySat"})
        assert result.data == {"item_type": "SkySat", "temp": 456}
