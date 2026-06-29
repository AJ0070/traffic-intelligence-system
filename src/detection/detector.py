from ultralytics import YOLO

from src.types import Detection


class VehicleDetector:
    def __init__(self, model_path="yolo11n.pt", conf_threshold=0.3):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck

    def detect(self, frame) -> list[Detection]:
        results = self.model(frame, conf=self.conf_threshold, classes=self.vehicle_classes, verbose=False)[0]
        detections: list[Detection] = []
        for box in results.boxes:
            x1, y1, x2, y2 = map(float, box.xyxy[0].tolist())
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            detections.append({
                'bbox': [x1, y1, x2, y2],
                'confidence': conf,
                'class_id': cls,
                'class_name': results.names[cls]
            })
        return detections
