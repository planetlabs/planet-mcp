"""
Description overrides.
"""

overrides = {
    "data_search": """
    Search for Planet imagery (scenes).

    item_types:
        High resolution: SkySatScene, SkySatCollect
        Medium resolution: PSScene

    geometry: a GeoJSON dictionary containing lat/lon coordinates, or a Features API feature reference. If a place
    name is supplied, use Google to find coordinates. Omit if the user does not specify a place name or
    coordinates. If using a feature reference, it must be provided in a dict like this:
        ```
        {
            "type": "ref",
            "content": "pl:features/my/test-collection-123/my-feature-id"
        }
        ```

    search_filter: a Planet Data API filter for advanced searches.

    If the user does not ask for specific item types, default to ["PSScene", "SkySatScene", "SkySatCollect"].

    Avoid using search_filter unless the user has asked for specific date ranges or other advanced parameters. If a
    user asks for a scene from "today", do a search as normal and present the first (most recent) result.
    """
}
