import math


class SpeedEstimator:
    def __init__(self, fps=30, pixel_per_meter=10):
        self.fps = fps
        self.pixel_per_meter = pixel_per_meter
        self.speeds = {}

    def estimate_speed(self, tracked_objects):
        for obj in tracked_objects:
            track_id = obj['track_id']
            traj = obj['trajectory']

            if len(traj) < 2:
                continue

            p1, p2 = traj[-2], traj[-1]
            distance_pixels = math.dist(p1, p2)
            distance_meters = distance_pixels / self.pixel_per_meter
            time_seconds = 1 / self.fps
            speed_mps = distance_meters / time_seconds
            speed_kmph = speed_mps * 3.6

            self.speeds[track_id] = round(speed_kmph, 2)

        return self.speeds
