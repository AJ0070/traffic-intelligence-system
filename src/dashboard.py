import cv2
import streamlit as st

from src.config import PipelineConfig
from src.video_processing import VideoProcessor

st.set_page_config(page_title="Traffic Intelligence Dashboard", layout="wide")
st.title("Traffic Intelligence Dashboard")


@st.cache_resource
def load_processor():
    return VideoProcessor(PipelineConfig())


processor = load_processor()
tab1, tab2 = st.tabs(["Video Analysis", "System Scope"])

with tab1:
    uploaded_file = st.file_uploader("Upload Traffic Video", type=["mp4", "avi", "mov"])

    if uploaded_file and st.button("Process Video"):
        result = processor.process_video(uploaded_file.read(), suffix=uploaded_file.name)
        latest = result["latest_result"]

        metrics = st.columns(4)
        metrics[0].metric("Tracked Vehicles", latest["total_vehicles"])
        metrics[1].metric("Lane Counts", sum(latest["lane_counts"].values()))
        metrics[2].metric("Parking Violations", len(latest["parking_violations"]))
        high_congestion = sum(1 for zone in latest["congestion"].values() if zone["level"] == "HIGH")
        metrics[3].metric("High Congestion Zones", high_congestion)

        if result["latest_snapshot"] is not None:
            frame_rgb = cv2.cvtColor(result["latest_snapshot"], cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, channels="RGB", caption="Annotated sample frame", use_container_width=True)

        speed_rows = [
            {"track_id": track_id, "speed_kmph": speed}
            for track_id, speed in latest["speeds"].items()
        ]
        if speed_rows:
            st.subheader("Estimated Speeds")
            st.dataframe(speed_rows, use_container_width=True, hide_index=True)

        if latest["events"]:
            st.subheader("Detected Events")
            st.dataframe(latest["events"], use_container_width=True, hide_index=True)

        st.subheader("Congestion")
        st.json(latest["congestion"])

with tab2:
    st.write(
        """
        This minimal build covers the resume scope only:
        vehicle detection with YOLOv11, ByteTrack-based multi-object tracking,
        lane-wise counting, congestion analysis, speed estimation, illegal parking
        detection, a FastAPI endpoint for processing videos, and a Streamlit dashboard
        for reviewing detections and traffic statistics.
        """
    )
