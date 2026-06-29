from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.config import PipelineConfig
from src.video_processing import VideoProcessor

processor = VideoProcessor(PipelineConfig())
stats_history: list[dict] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    stats_history.clear()
    yield


app = FastAPI(title="Traffic Intelligence API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessedVideoResponse(BaseModel):
    frames_processed: int
    sampled_frames: int
    total_vehicles: int
    lane_counts: dict[int, int]
    speeds: dict[int, float]
    congestion: dict[int, dict]
    parking_violations: dict[int, dict]
    events: list[dict]


@app.get("/")
async def root():
    return {
        "message": "Traffic Intelligence API",
        "status": "running",
        "features": [
            "vehicle_detection",
            "multi_object_tracking",
            "lane_counting",
            "congestion_analysis",
            "speed_estimation",
            "illegal_parking_detection",
        ],
    }


@app.get("/stats")
async def get_stats():
    if stats_history:
        return stats_history[-1]
    return {"message": "No data yet"}


@app.get("/history")
async def get_history():
    return {"history": stats_history[-100:]}


@app.post("/process-video", response_model=ProcessedVideoResponse)
async def process_video(file: UploadFile = File(...)):
    contents = await file.read()
    processed = processor.process_video(contents, suffix=file.filename or ".mp4")
    latest = processed["latest_result"]
    payload = {
        "frames_processed": processed["frames_processed"],
        "sampled_frames": processed["sampled_frames"],
        "total_vehicles": latest["total_vehicles"],
        "lane_counts": latest["lane_counts"],
        "speeds": latest["speeds"],
        "congestion": latest["congestion"],
        "parking_violations": latest["parking_violations"],
        "events": latest["events"],
    }
    stats_history.append(payload)
    return payload
