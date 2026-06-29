from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class PipelineConfig:
    model_path: str = "yolo11n.pt"
    fps: float = 30.0
    pixel_per_meter: float = 12.0
    frame_sample_rate: int = 3
    lane_lines: list[list[int]] = field(
        default_factory=lambda: [
            [180, 260, 1100, 260],
            [180, 430, 1100, 430],
        ]
    )
    congestion_zones: list[list[int]] = field(
        default_factory=lambda: [
            [0, 0, 640, 720],
            [640, 0, 1280, 720],
        ]
    )
    parking_zones: list[list[int]] = field(
        default_factory=lambda: [
            [40, 80, 320, 330],
        ]
    )
    parking_threshold_seconds: float = 8.0
    stationary_distance_threshold: float = 12.0


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
