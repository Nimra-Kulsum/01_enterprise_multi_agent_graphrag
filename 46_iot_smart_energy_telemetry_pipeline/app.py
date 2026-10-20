"""
Industrial IoT Smart Grid Telemetry & Time-Series Engine
Ingests sensor readings, performs real-time window downsampling, and flags anomalies.
"""
import time
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Industrial IoT Telemetry Engine", version="1.0.0")

class SensorPing(BaseModel):
    device_id: str
    voltage_volts: float
    current_amps: float
    temperature_celsius: float
    timestamp: float

# In-memory time-series buffer
DEVICE_BUFFERS: Dict[str, List[SensorPing]] = {}

@app.post("/api/v1/telemetry/ingest")
def ingest_telemetry(ping: SensorPing):
    if ping.device_id not in DEVICE_BUFFERS:
        DEVICE_BUFFERS[ping.device_id] = []
    
    DEVICE_BUFFERS[ping.device_id].append(ping)
    
    # Alert condition: Overheating or Voltage Surge
    is_anomaly = ping.temperature_celsius > 75.0 or ping.voltage_volts > 250.0
    
    return {
        "status": "INGESTED",
        "device_id": ping.device_id,
        "is_alert": is_anomaly,
        "power_watts": round(ping.voltage_volts * ping.current_amps, 2)
    }

@app.get("/api/v1/telemetry/rollup/{device_id}")
def compute_rollup(device_id: str):
    pings = DEVICE_BUFFERS.get(device_id, [])
    if not pings:
        return {"device_id": device_id, "samples": 0}
        
    avg_voltage = sum(p.voltage_volts for p in pings) / len(pings)
    max_temp = max(p.temperature_celsius for p in pings)
    
    return {
        "device_id": device_id,
        "total_samples": len(pings),
        "avg_voltage": round(avg_voltage, 2),
        "max_temperature": round(max_temp, 2)
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8046)
