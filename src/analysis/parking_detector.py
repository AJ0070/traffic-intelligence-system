from collections import defaultdict


class ParkingDetector:
    def __init__(self, parking_zones, time_threshold=5.0, stationary_distance_threshold=10.0):
        self.parking_zones = parking_zones
        self.time_threshold = time_threshold
        self.stationary_distance_threshold = stationary_distance_threshold
        self.stationary_tracks = defaultdict(lambda: {"start_time": None, "position": None})
        self.violations = {}

    def detect_violations(self, tracked_objects, current_time):
        active_ids = set()

        for obj in tracked_objects:
            track_id = obj['track_id']
            cx, cy = obj['center']
            active_ids.add(track_id)

            in_parking_zone = any(
                x1 <= cx <= x2 and y1 <= cy <= y2
                for x1, y1, x2, y2 in self.parking_zones
            )

            if not in_parking_zone:
                if track_id in self.stationary_tracks:
                    del self.stationary_tracks[track_id]
                continue

            if len(obj['trajectory']) < 3:
                continue

            recent = obj['trajectory'][-3:]
            movement = sum(
                ((recent[i][0] - recent[i-1][0])**2 + (recent[i][1] - recent[i-1][1])**2)**0.5
                for i in range(1, len(recent))
            )

            if movement < self.stationary_distance_threshold:
                if self.stationary_tracks[track_id]["start_time"] is None:
                    self.stationary_tracks[track_id]["start_time"] = current_time
                    self.stationary_tracks[track_id]["position"] = (cx, cy)

                elapsed = current_time - self.stationary_tracks[track_id]["start_time"]
                if elapsed > self.time_threshold:
                    self.violations[track_id] = {
                        "duration": round(elapsed, 2),
                        "position": self.stationary_tracks[track_id]["position"]
                    }
            else:
                if track_id in self.stationary_tracks:
                    del self.stationary_tracks[track_id]

        for track_id in list(self.stationary_tracks.keys()):
            if track_id not in active_ids:
                del self.stationary_tracks[track_id]

        return dict(self.violations)
