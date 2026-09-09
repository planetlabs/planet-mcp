from datetime import datetime

from fastmcp import FastMCP
from planet import DataClient

from planet_mcp import models
from planet_mcp.clients import session
from planet_mcp.servers import descriptions

# technically not using the sdk to make the tool but we can add it to that

mcp = FastMCP("sdk")


@mcp.tool(
    name="data_search",
    description=descriptions.overrides["data_search"],
    tags={"data", "search"},
)
async def data_search(
    item_types: list[str],
    start_date: str | None,
    end_date: str | None,
    geometry: models.Geometry,
):
    data_client = DataClient(session=session())

    cloud_filter = {
        "type": "RangeFilter",
        "field_name": "cloud_cover",
        "config": {"lte": 0.2},
    }
    filter = {
        "type": "AndFilter",
        "config": [cloud_filter],
    }
    if start_date is not None or end_date is not None:
        datefilter_config = {}
        if start_date is not None:
            datefilter_config["gte"] = datetime.fromisoformat(start_date).isoformat()
        if end_date is not None:
            datefilter_config["lte"] = datetime.fromisoformat(end_date).isoformat()
        datefilter = {
            "type": "DateRangeFilter",
            "field_name": "acquired",
            "config": datefilter_config,
        }
        filter["config"].append(datefilter)

    results = data_client.search(
        item_types=item_types,
        geometry=dict(geometry),
        search_filter=filter,
        limit=10,
    )
    return [r async for r in results]
