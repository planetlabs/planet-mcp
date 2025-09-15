from typing import Annotated
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
import httpx
import mercantile
from pydantic import Field

from planet_mcp.clients import session

mcp = FastMCP("tiles")


@mcp.tool(tags={"tiles", "scene"})
async def get_scene_tile(
    item_type: Annotated[str, Field(pattern=r"^\w+$")],
    item_id: Annotated[str, Field(pattern=r"^\w+$")],
    lat: Annotated[float, Field(ge=-90.0, le=90.0)],
    long: Annotated[float, Field(ge=-180.0, le=180.0)],
    zoom: Annotated[int, Field(ge=10, le=15)] = 14,
) -> Image:
    """
    Get a tile image for a specific item at a given latitude and longitude.

    Latitude and longitude must be in decimal degrees.

    item_type and item_id are required. Suitable items can be found with the data_search tool.
    """

    # Convert latitude and longitude to tile xyz
    tile = mercantile.tile(long, lat, zoom)
    x, y = tile.x, tile.y

    req = httpx.Request(
        "GET",
        f"https://tiles3.planet.com/data/v1/{item_type}/{item_id}/{zoom}/{x}/{y}.png",
    )
    data = await session()._send(req)

    if data.status_code != 200:
        # we are using an external facing API, so we can relay the error message back
        # to the user. It may indicate an invalid input.
        if data.text:
            raise ValueError(f"Failed to fetch tile: {data.text}")
        raise ValueError("Failed to fetch tile. Please try again.")
    return Image(
        data=data.content,
        format="png",
    )


@mcp.tool(tags={"tiles", "thumbnail"})
async def get_scene_thumbnail(
    item_type: Annotated[str, Field(pattern=r"^\w+$")],
    item_id: Annotated[str, Field(pattern=r"^\w+$")],
) -> Image:
    """
    Get a thumbnail image for a specific item.

    item_type and item_id are required. Suitable items can be found with the data_search tool.
    item_id accepts alphanumeric characters and underscores.
    """
    thumbnail = (
        f"https://tiles.planet.com/data/v1/item-types/{item_type}/items/{item_id}/thumb"
    )
    data = await session()._send(httpx.Request("GET", thumbnail))

    if data.status_code != 200:
        if data.text:
            raise ValueError(f"Failed to fetch tile: {data.text}")
        raise ValueError("Failed to fetch thumbnail. Please try again.")
    return Image(
        data=data.content,
        format="png",
    )
