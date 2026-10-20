"""
Zero-Downtime Blue-Green & Canary Deployment Traffic Director
Weighted traffic distribution with automated rollback on 5xx error spikes.
"""
import random
from typing import Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Canary Traffic Director & Rollback Engine", version="1.0.0")

class TrafficConfig(BaseModel):
    canary_weight_percent: int = 10 # 10% to Canary, 90% to Stable
    canary_version: str = "v2.0.0-rc1"
    stable_version: str = "v1.9.4"
    auto_rollback_enabled: bool = True

config = TrafficConfig()

# Metric tracking
metrics = {"canary_requests": 0, "canary_errors": 0, "stable_requests": 0}

@app.get("/api/v1/route")
def route_request():
    # Weighted traffic decision
    roll = random.randint(1, 100)
    if roll <= config.canary_weight_percent:
        metrics["canary_requests"] += 1
        return {"routed_to": "CANARY", "version": config.canary_version}
    else:
        metrics["stable_requests"] += 1
        return {"routed_to": "STABLE", "version": config.stable_version}

@app.post("/api/v1/report-error")
def report_canary_error():
    metrics["canary_errors"] += 1
    # Check if canary error rate exceeds threshold
    if metrics["canary_requests"] > 0:
        err_rate = (metrics["canary_errors"] / metrics["canary_requests"]) * 100.0
        if err_rate > 5.0 and config.auto_rollback_enabled:
            # Trigger instant rollback!
            config.canary_weight_percent = 0
            return {"status": "EMERGENCY_ROLLBACK_TRIGGERED", "error_rate": err_rate, "canary_traffic": "0%"}
    return {"status": "recorded"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8033)
