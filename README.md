# AI-Based Intelligent Traffic Monitoring System

Traffic analytics project for
vehicle detection, multi-object tracking, lane-wise counting, congestion analysis,
speed estimation, illegal parking detection, and a dashboard/API layer for video-based traffic monitoring.

## Stack

- Python
- PyTorch
- OpenCV
- YOLOv11 via `ultralytics`
- ByteTrack via `supervision`
- FastAPI
- Streamlit
- Docker

## Implemented Scope

- Vehicle detection for road traffic classes
- ByteTrack-based multi-object tracking
- Lane-wise counting from configurable line segments
- Congestion analysis over configurable zones
- Speed estimation using pixel-to-meter calibration
- Illegal parking detection for stationary vehicles in restricted zones
- FastAPI endpoint for processing uploaded videos
- Streamlit dashboard for reviewing detections and traffic statistics

## Local Run

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
streamlit run src/dashboard.py
```

The first run will download the default `yolo11n.pt` model if it is not already available.

## Docker Run

```bash
docker-compose up --build
```

## API

- `GET /` returns service status and implemented features
- `GET /stats` returns the latest processed traffic summary
- `GET /history` returns recent processed summaries
- `POST /process-video` accepts a video upload and returns the latest traffic analytics snapshot

## Tests

```bash
python -m unittest discover -s tests
```
