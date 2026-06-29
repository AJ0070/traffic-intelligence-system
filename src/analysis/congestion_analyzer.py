from collections import defaultdict


class CongestionAnalyzer:
    def __init__(self, zones):
        self.zones = zones
        self.congestion_levels = {}

    def analyze(self, tracked_objects):
        zone_counts = defaultdict(int)

        for obj in tracked_objects:
            cx, cy = obj['center']
            for zone_id, (x1, y1, x2, y2) in enumerate(self.zones):
                if x1 <= cx <= x2 and y1 <= cy <= y2:
                    zone_counts[zone_id] += 1

        for zone_id in range(len(self.zones)):
            count = zone_counts[zone_id]
            if count < 5:
                level = "LOW"
            elif count < 15:
                level = "MEDIUM"
            else:
                level = "HIGH"
            self.congestion_levels[zone_id] = {"count": count, "level": level}

        return self.congestion_levels
