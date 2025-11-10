from typing_extensions import Literal, TypedDict


class Polygon(TypedDict):
    type: Literal["Polygon"]
    coordinates: list[list[list[float]]]


class Point(TypedDict):
    type: Literal["Point"]
    coordinates: list[float]
