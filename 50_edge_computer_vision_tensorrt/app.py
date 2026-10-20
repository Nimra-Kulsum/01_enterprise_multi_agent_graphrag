"""
Hardware-Accelerated Edge Computer Vision & TensorRT Engine
Multi-camera stream inference simulator with INT8 quantization metrics and tracking.
"""
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Edge Computer Vision & TensorRT Engine", version="1.0.0")

class DetectionBox(BaseModel):
    class_name: str
    confidence: float
    bbox: List[int] # [x1, y1, x2, y2]
    track_id: int

class CameraFrameInference(BaseModel):
    camera_id: str
    frame_number: int
    detections: List[DetectionBox]
    inference_latency_ms: float
    quantization_mode: str = "INT8_TENSORRT"

@app.post("/api/v1/vision/infer-frame", response_model=CameraFrameInference)
def process_camera_frame(camera_id: str, frame_num: int):
    # Simulated high-speed INT8 detection output
    detections = [
        DetectionBox(class_name="person", confidence=0.96, bbox=[120, 80, 240, 410], track_id=101),
        DetectionBox(class_name="safety_helmet", confidence=0.93, bbox=[135, 82, 185, 130], track_id=101),
        DetectionBox(class_name="forklift", confidence=0.91, bbox=[450, 200, 800, 600], track_id=204)
    ]
    
    return CameraFrameInference(
        camera_id=camera_id,
        frame_number=frame_num,
        detections=detections,
        inference_latency_ms=6.4, # 6.4ms sub-frame latency
        quantization_mode="INT8_TENSORRT"
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8050)
