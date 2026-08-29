from typing import NotRequired
from typing_extensions import TypedDict

Position = list[float]
Coordinates = (
    Position | list[Position] | list[list[Position]] | list[list[list[Position]]]
)


class Geometry(TypedDict):
    type: str
    coordinates: NotRequired[Coordinates]
    content: NotRequired[str]
