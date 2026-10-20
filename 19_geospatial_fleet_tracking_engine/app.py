"""
Geospatial Fleet Tracking & Hexagonal Geofencing Engine
Real-time GPS coordinate ingestion and geofence containment verification.
"""
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Geospatial Fleet Tracking Service", version="1.0.0")

class GPSPing(BaseModel):
    vehicle_id: str
    latitude: float
    longitude: float
    timestamp: float

class GeofenceZone(BaseModel):
    zone_id: str
    name: str
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float

# Predefined municipal zones (e.g., Downtown Airport Zone)
ACTIVE_ZONES = [
    GeofenceZone(zone_id="zone_airport", name="International Airport Restricted Zone", min_lat=37.61, max_lat=37.63, min_lon=-122.39, max_lon=-122.37),
    GeofenceZone(zone_id="zone_downtown", name="Downtown Congestion Zone", min_lat=37.77, max_lat=37.80, min_lon=-122.42, max_lon=-122.39)
]

@app.post("/api/v1/telemetry/ping")
def ingest_gps_ping(ping: GPSPing):
    breached_zones = []
    
    # Geofence containment check
    for zone in ACTIVE_ZONES:
        if zone.min_lat <= ping.latitude <= zone.max_lat and zone.min_lon <= ping.longitude <= zone.max_lon:
            breached_zones.append(zone.name)

    return {
        "vehicle_id": ping.vehicle_id,
        "processed": True,
        "current_zones": breached_zones,
        "requires_alert": len(breached_zones) > 0
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8019)
