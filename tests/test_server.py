from http import HTTPStatus
import httpx
import pytest
from fastmcp import Client
import respx
from planet_mcp.server import init

client = Client(init())


@pytest.mark.asyncio
@respx.mock
async def test_search_tool():
    respx.request(
        "POST", "https://api.planet.com/data/v1/quick-search"
    ).return_value = httpx.Response(
        HTTPStatus.OK, json={"features": [{"type": "Feature"}]}
    )
    async with client:
        result = await client.call_tool(
            "sdk_data_search", {"item_types": ["SkySatScene"]}
        )
    assert result.structured_content == {"result": [{"type": "Feature"}]}
