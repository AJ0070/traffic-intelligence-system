import warnings
import numpy as np
from collections import defaultdict
import supervision as sv

from src.types import Detection, TrackedObject


class VehicleTracker:
    def __init__(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            self.tracker = sv.ByteTrack()
        self.tracks = defaultdict(list)

    def update(self, detections: list[Detection]) -> list[TrackedObject]:
        if not detections:
            return []

        xyxy = np.array([d['bbox'] for d in detections])
        confidence = np.array([d['confidence'] for d in detections])
        class_id = np.array([d['class_id'] for d in detections])
        data = {"class_name": np.array([d["class_name"] for d in detections], dtype=object)}

        det = sv.Detections(xyxy=xyxy, confidence=confidence, class_id=class_id, data=data)
        tracked = self.tracker.update_with_detections(det)

        tracked_objects: list[TrackedObject] = []
        for i in range(len(tracked)):
            track_id = int(tracked.tracker_id[i])
            bbox = tracked.xyxy[i].tolist()
            center = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]

            self.tracks[track_id].append(center)

            tracked_objects.append({
                'track_id': track_id,
                'bbox': bbox,
                'center': center,
                'class_id': int(tracked.class_id[i]),
                'class_name': str(tracked.data["class_name"][i]),
                'confidence': float(tracked.confidence[i]),
                'trajectory': [list(point) for point in self.tracks[track_id]],
            })

        return tracked_objects
