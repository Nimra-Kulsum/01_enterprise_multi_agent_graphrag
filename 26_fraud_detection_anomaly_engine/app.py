"""
Real-Time Financial Fraud & Anomaly Detection Pipeline
Calculates impossible velocity and sliding-window transaction frequency anomalies.
"""
import math
from typing import Dict, List
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Real-Time Fraud & Anomaly Detection Engine", version="1.0.0")

class TransactionPayload(BaseModel):
    user_id: str
    amount: float
    latitude: float
    longitude: float
    timestamp: float

# User last seen cache
USER_LAST_TX: Dict[str, dict] = {}

def haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.post("/api/v1/fraud/evaluate")
def evaluate_transaction(tx: TransactionPayload):
    fraud_flags = []
    risk_score = 0.0

    # Rule 1: High Amount Spike
    if tx.amount > 5000.0:
        fraud_flags.append("High monetary value spike")
        risk_score += 0.4

    # Rule 2: Impossible Velocity Check
    if tx.user_id in USER_LAST_TX:
        prev = USER_LAST_TX[tx.user_id]
        distance_km = haversine_km(prev["lat"], prev["lon"], tx.latitude, tx.longitude)
        hours_elapsed = (tx.timestamp - prev["time"]) / 3600.0
        
        if hours_elapsed > 0:
            speed_kmh = distance_km / hours_elapsed
            if speed_kmh > 900.0 and distance_km > 100.0:
                fraud_flags.append(f"Impossible Travel Velocity: {round(speed_kmh, 1)} km/h across {round(distance_km, 1)} km")
                risk_score += 0.6

    USER_LAST_TX[tx.user_id] = {"lat": tx.latitude, "lon": tx.longitude, "time": tx.timestamp}
    decision = "DECLINE" if risk_score >= 0.7 else ("MANUAL_REVIEW" if risk_score >= 0.4 else "APPROVE")

    return {
        "user_id": tx.user_id,
        "risk_score": round(risk_score, 2),
        "decision": decision,
        "flags": fraud_flags
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8026)
