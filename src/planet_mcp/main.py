"""
This is the entry point for a local MCP server and when the package
is installed, this is installed as an executable named planet-mcp.
"""

import argparse
from planet_mcp.server import init


def parse_args() -> argparse.Namespace:
    def csv(value):
        return set(t.strip() for t in (value or "").split(","))

    parser = argparse.ArgumentParser(
        description="Planet MCP Server",
    )
    # when using fastmcp inspector and other tools, we handle
    # extra args here (or else the parser barfs)
    parser.add_argument("args", nargs="*")
    # default enable all tools, except download and subscriptions
    parser.add_argument(
        "--include-tags",
        type=csv,
        default={"data", "tiles", "orders", "destinations", "mosaics", "features"},
    )
    parser.add_argument("--exclude-tags", type=csv, default=None)
    parser.add_argument("--servers", type=csv, default=None)
    # similar to extra args, inspector adds this
    parser.add_argument("--no-banner", action="store_true")
    return parser.parse_args()


args = parse_args()
# note - the mcp dev tooling (e.g. uv run fastmcp dev src/main.py)
# wants to find a server object named `mcp` (or it won't work)
mcp = init(
    enabled_servers=args.servers,
    include_tags=args.include_tags,
    exclude_tags=args.exclude_tags,
)


# this is the entry point for the executable script installed via package
# and also supports execution via `uv run fastmcp run src/main.py`
def main():
    mcp.run(transport="stdio", show_banner=not args.no_banner)


if __name__ == "__main__":
    main()
