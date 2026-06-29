import cv2


def draw_annotations(frame, result: dict, lane_lines: list[list[int]], parking_zones: list[list[int]]) -> None:
    for lane in lane_lines:
        x1, y1, x2, y2 = map(int, lane)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 215, 0), 2)

    for zone in parking_zones:
        x1, y1, x2, y2 = map(int, zone)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 140, 255), 2)

    for tracked in result["tracked_objects"]:
        x1, y1, x2, y2 = map(int, tracked["bbox"])
        label = f'{tracked["class_name"]} #{tracked["track_id"]}'
        speed = result["speeds"].get(tracked["track_id"])
        if speed is not None:
            label = f"{label} {speed:.1f} km/h"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (30, 220, 30), 2)
        cv2.putText(frame, label, (x1, max(y1 - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (30, 220, 30), 2)

    for event in result["events"]:
        if event["type"] != "illegal_parking":
            continue
        cx, cy = map(int, event["position"])
        cv2.putText(
            frame,
            f'Parking violation #{event["track_id"]}',
            (cx, cy),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
        )
