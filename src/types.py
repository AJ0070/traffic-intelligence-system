from typing import TypedDict


class Detection(TypedDict):
    bbox: list[float]
    confidence: float
    class_id: int
    class_name: str


class TrackedObject(TypedDict):
    track_id: int
    bbox: list[float]
    center: list[float]
    class_id: int
    class_name: str
    confidence: float
    trajectory: list[list[float]]
