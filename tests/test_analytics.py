import unittest

from src.analysis.congestion_analyzer import CongestionAnalyzer
from src.analysis.lane_counter import LaneCounter
from src.analysis.parking_detector import ParkingDetector
from src.analysis.speed_estimator import SpeedEstimator


class AnalyticsTestCase(unittest.TestCase):
    def test_lane_counter_counts_single_crossing(self):
        counter = LaneCounter([[0, 5, 10, 5]])
        tracked = [{"track_id": 1, "trajectory": [[5, 2], [5, 8]]}]

        counts = counter.count(tracked)

        self.assertEqual(counts, {0: 1})

    def test_speed_estimator_returns_kmph(self):
        estimator = SpeedEstimator(fps=10, pixel_per_meter=5)
        tracked = [{"track_id": 7, "trajectory": [[0, 0], [0, 10]]}]

        speeds = estimator.estimate_speed(tracked)

        self.assertEqual(speeds[7], 72.0)

    def test_congestion_analyzer_assigns_levels(self):
        analyzer = CongestionAnalyzer([[0, 0, 100, 100]])
        tracked = [{"center": [10, 10]} for _ in range(6)]

        congestion = analyzer.analyze(tracked)

        self.assertEqual(congestion[0]["level"], "MEDIUM")

    def test_parking_detector_flags_stationary_vehicle(self):
        detector = ParkingDetector([[0, 0, 100, 100]], time_threshold=4.0, stationary_distance_threshold=5.0)
        tracked = [{"track_id": 11, "center": [10, 10], "trajectory": [[10, 10], [11, 10], [10.5, 10.5]]}]

        detector.detect_violations(tracked, current_time=1.0)
        violations = detector.detect_violations(tracked, current_time=6.0)

        self.assertEqual(violations[11]["duration"], 5.0)


if __name__ == "__main__":
    unittest.main()
