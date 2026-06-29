from src.analysis.congestion_analyzer import CongestionAnalyzer
from src.analysis.lane_counter import LaneCounter
from src.analysis.parking_detector import ParkingDetector
from src.analysis.speed_estimator import SpeedEstimator
from src.config import PipelineConfig
from src.detection.detector import VehicleDetector
from src.tracking.tracker import VehicleTracker


class TrafficPipeline:
    def __init__(self, config: PipelineConfig | None = None):
        self.config = config or PipelineConfig()
        self.detector = VehicleDetector(self.config.model_path)
        self.tracker = VehicleTracker()
        self.lane_counter = LaneCounter(self.config.lane_lines)
        self.speed_estimator = SpeedEstimator(
            fps=self.config.fps,
            pixel_per_meter=self.config.pixel_per_meter,
        )
        self.congestion_analyzer = CongestionAnalyzer(self.config.congestion_zones)
        self.parking_detector = ParkingDetector(
            self.config.parking_zones,
            time_threshold=self.config.parking_threshold_seconds,
            stationary_distance_threshold=self.config.stationary_distance_threshold,
        )

    def process_frame(self, frame, timestamp_seconds: float) -> dict:
        detections = self.detector.detect(frame)
        tracked_objects = self.tracker.update(detections)

        lane_counts = self.lane_counter.count(tracked_objects)
        speeds = self.speed_estimator.estimate_speed(tracked_objects)
        congestion = self.congestion_analyzer.analyze(tracked_objects)
        parking_violations = self.parking_detector.detect_violations(tracked_objects, timestamp_seconds)

        events = []
        for track_id, violation in parking_violations.items():
            events.append(
                {
                    "type": "illegal_parking",
                    "track_id": track_id,
                    "duration_seconds": violation["duration"],
                    "position": violation["position"],
                }
            )

        return {
            "detections": detections,
            "tracked_objects": tracked_objects,
            "lane_counts": lane_counts,
            "speeds": speeds,
            "congestion": congestion,
            "parking_violations": parking_violations,
            "events": events,
            "total_vehicles": len(tracked_objects),
        }
