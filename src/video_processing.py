from __future__ import annotations

import tempfile
from pathlib import Path

import cv2

from src.config import PipelineConfig
from src.pipeline import TrafficPipeline
from src.rendering import draw_annotations


class VideoProcessor:
    def __init__(self, config: PipelineConfig | None = None):
        self.config = config or PipelineConfig()
        self.pipeline = TrafficPipeline(self.config)

    def process_video(self, video_bytes: bytes, suffix: str) -> dict:
        self.pipeline = TrafficPipeline(self.config)
        temp_path = self._write_temp_video(video_bytes, suffix)

        try:
            capture = cv2.VideoCapture(str(temp_path))
            frames_processed = 0
            sampled_frames = 0
            last_result = None
            latest_snapshot = None

            while capture.isOpened():
                ok, frame = capture.read()
                if not ok:
                    break

                if frames_processed % self.config.frame_sample_rate == 0:
                    timestamp_seconds = frames_processed / self.config.fps
                    result = self.pipeline.process_frame(frame, timestamp_seconds=timestamp_seconds)
                    annotated_frame = frame.copy()
                    draw_annotations(
                        annotated_frame,
                        result,
                        self.config.lane_lines,
                        self.config.parking_zones,
                    )
                    latest_snapshot = annotated_frame
                    last_result = result
                    sampled_frames += 1

                frames_processed += 1

            capture.release()

            return {
                "frames_processed": frames_processed,
                "sampled_frames": sampled_frames,
                "latest_result": last_result or self._empty_result(),
                "latest_snapshot": latest_snapshot,
            }
        finally:
            temp_path.unlink(missing_ok=True)

    def _write_temp_video(self, video_bytes: bytes, suffix: str) -> Path:
        suffix = Path(suffix).suffix or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(video_bytes)
            return Path(temp_file.name)

    @staticmethod
    def _empty_result() -> dict:
        return {
            "detections": [],
            "tracked_objects": [],
            "lane_counts": {},
            "speeds": {},
            "congestion": {},
            "parking_violations": {},
            "events": [],
            "total_vehicles": 0,
        }
