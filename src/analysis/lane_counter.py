from collections import defaultdict


class LaneCounter:
    def __init__(self, lane_lines):
        self.lane_lines = lane_lines
        self.lane_counts = defaultdict(int)
        self.counted_ids = defaultdict(set)

    def count(self, tracked_objects):
        for obj in tracked_objects:
            track_id = obj['track_id']
            traj = obj['trajectory']

            if len(traj) < 2:
                continue

            for lane_id, line in enumerate(self.lane_lines):
                if track_id in self.counted_ids[lane_id]:
                    continue

                if self._crossed_line(traj[-2], traj[-1], line):
                    self.lane_counts[lane_id] += 1
                    self.counted_ids[lane_id].add(track_id)

        return dict(self.lane_counts)

    def _crossed_line(self, p1, p2, line):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3, x4, y4 = line

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-10:
            return False

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

        return 0 < t < 1 and 0 < u < 1
