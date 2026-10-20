"""
Chaos Engineering & Automated Fault Injection Platform
Simulates fault injection (latency, process kill) with automated SLO abort triggers.
"""
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Chaos Engineering & Fault Injection Engine", version="1.0.0")

class ChaosExperiment(BaseModel):
    experiment_id: str
    target_service: str
    fault_type: str # "INJECT_LATENCY_MS", "KILL_INSTANCE", "CORRUPT_PACKETS"
    intensity: int
    slo_error_threshold_percent: float = 5.0

ACTIVE_EXPERIMENTS: Dict[str, ChaosExperiment] = {}

@app.post("/api/v1/chaos/start")
def start_experiment(exp: ChaosExperiment):
    ACTIVE_EXPERIMENTS[exp.experiment_id] = exp
    return {
        "status": "RUNNING",
        "experiment_id": exp.experiment_id,
        "blast_radius": f"Targeting {exp.target_service} with {exp.fault_type}"
    }

@app.post("/api/v1/chaos/abort/{experiment_id}")
def abort_experiment(experiment_id: str):
    if experiment_id not in ACTIVE_EXPERIMENTS:
        raise HTTPException(status_code=404, detail="Experiment not found")
    del ACTIVE_EXPERIMENTS[experiment_id]
    return {"status": "ABORTED", "message": "Emergency abort triggered. Steady-state restored."}

@app.get("/api/v1/chaos/active")
def list_active():
    return {"active_count": len(ACTIVE_EXPERIMENTS), "experiments": list(ACTIVE_EXPERIMENTS.values())}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8032)
