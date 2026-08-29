from http import HTTPStatus
import json

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
            "sdk_data_search",
            {
                "item_types": ["SkySatScene"],
                "start_date": "2023-01-01",
                "end_date": "2023-01-02",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
            },
        )
    assert len(result.content) == 1
    assert result.content[0].type == "text"
    assert result.content[0].text == '[{"type":"Feature"}]'

    request = json.loads(respx.calls.last.request.content)
    assert request["geometry"] == {"type": "Point", "coordinates": [0, 0]}


@pytest.mark.asyncio
@respx.mock
async def test_search_tool_feature_reference():
    respx.request(
        "POST", "https://api.planet.com/data/v1/quick-search"
    ).return_value = httpx.Response(
        HTTPStatus.OK, json={"features": [{"type": "Feature"}]}
    )
    ref = "pl:features/my/test-collection-123/my-feature-id"
    async with client:
        result = await client.call_tool(
            "sdk_data_search",
            {
                "item_types": ["SkySatScene"],
                "start_date": None,
                "end_date": None,
                "geometry": {"type": "ref", "content": ref},
            },
        )
    assert result.content[0].text == '[{"type":"Feature"}]'

    request = json.loads(respx.calls.last.request.content)
    assert request["geometry"] == {"type": "ref", "content": ref}
