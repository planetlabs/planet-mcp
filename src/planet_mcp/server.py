import functools
import inspect
from planet_mcp import descriptions, tiles
from fastmcp import FastMCP
import planet
from typing import Union, Optional

from pydantic import PydanticSchemaGenerationError


DEFAULT_IGNORE = {
    "data_wait_asset",
    "orders_wait",
}


class MCPService:
    """MCP service for the Planet API

    member `mcp` contains the FastMCP app instance.
    """

    def __init__(
        self,
        mcp: FastMCP,
        session: planet.Session,
        ignore: set[str] | None = None,
    ):
        self.mcp = mcp
        self.session = session

        self.ignore = ignore if ignore is not None else DEFAULT_IGNORE

        self.make_tools(planet.FeaturesClient, "features")
        self.make_tools(planet.DataClient, "data")
        self.make_tools(planet.OrdersClient, "orders")
        self.make_tools(planet.SubscriptionsClient, "subscriptions")
        self.make_tools(planet.MosaicsClient, "mosaics")
        self.make_tools(planet.DestinationsClient, "destinations")

        # add tiles tools
        tiles.init(self.mcp, self.session)

    def make_tools(self, client_class, prefix: str):
        for name, func in inspect.getmembers(client_class(self.session)):
            if inspect.ismethod(func) and name[0] != "_":
                full_name = f"{prefix}_{name}"

                if full_name in self.ignore:
                    continue

                # extended tool options
                opts = {}

                # check if there is a description override for this tool
                if full_name in descriptions.overrides:
                    opts["description"] = descriptions.overrides[full_name]

                # async generator functions have an incompatible return type.
                # ensure they are converted to a list[dict] return type.
                if inspect.isasyncgenfunction(func):
                    func = _async_get_wrapper(func, prefix)

                # no return functions end up with a "self" parameter so this
                # works around by adding a simple response
                # @todo - upstream bug?
                sig = inspect.signature(func)
                if sig.return_annotation is None:
                    func = _return_wrapper(func)

                try:
                    self.mcp.tool(func, name=full_name, **opts)
                except PydanticSchemaGenerationError:
                    # there's a few functions we need to modify again because of custom types.
                    modified_func = _create_param_modified_wrapper(func)
                    try:
                        self.mcp.tool(modified_func, name=full_name, **opts)
                    except Exception as e:
                        print("Unable to add tool", full_name, e)


def _async_get_wrapper(f, prefix):
    """wrap an async generator to return a list[dict]"""

    @functools.wraps(f)
    async def generate_async(*args, **kwargs) -> list[dict]:
        return [i async for i in (f(*args, **kwargs))]

    # functool.wraps annotates using the original function return
    generate_async.__annotations__["return"] = list[dict]
    return generate_async


def _return_wrapper(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
        return {"status": "ok"}

    wrapper.__annotations__["return"] = dict
    return wrapper


def _create_param_modified_wrapper(original_func):
    """
    Some functions that accept special types (typing.Protocol) fail during
    FastMCP tool registration. This wrapper modifies the function's signature,
    replacing the type hints with simple types that FastMCP can handle.
    """

    @functools.wraps(original_func)
    async def wrapper(*args, **kwargs):
        return await original_func(*args, **kwargs)

    try:
        sig = inspect.signature(original_func)

        for param_name, param in sig.parameters.items():
            # Convert problematic types into useable ones.
            # we want to override the GeojsonLike field
            # and remove the union of the Feature which accepts a dict or a GeoInterface
            if param_name in ("feature", "quad", "mosaic", "series"):
                wrapper.__annotations__[param_name] = dict
            elif param_name == "geometry" and "planet.models" in str(param.annotation):
                wrapper.__annotations__[param_name] = Optional[Union[dict, str]] | None

    except Exception as e:
        print(f"Error modifying signature: {e}")
        wrapper.__annotations__ = {}

    return wrapper
