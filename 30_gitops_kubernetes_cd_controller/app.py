"""
Automated GitOps Continuous Delivery Controller (Mini-ArgoCD)
Detects configuration drift between desired Git state and live cluster state.
"""
from typing import Dict, List
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="GitOps Continuous Delivery Controller", version="1.0.0")

# Simulated Live Cluster State
LIVE_CLUSTER: Dict[str, dict] = {
    "payment-service": {"replicas": 3, "image": "payments:v2.1.0"},
    "auth-service": {"replicas": 2, "image": "auth:v1.9.0"}
}

# Simulated Git Repository Desired State
GIT_DESIRED: Dict[str, dict] = {
    "payment-service": {"replicas": 5, "image": "payments:v2.2.0"}, # Replicas and version changed!
    "auth-service": {"replicas": 2, "image": "auth:v1.9.0"}
}

@app.get("/api/v1/gitops/sync-status")
def check_drift():
    drift_report = []
    
    for app_name, desired in GIT_DESIRED.items():
        live = LIVE_CLUSTER.get(app_name, {})
        diffs = {}
        for key, desired_val in desired.items():
            live_val = live.get(key)
            if live_val != desired_val:
                diffs[key] = {"desired": desired_val, "live": live_val}
                
        is_synced = len(diffs) == 0
        drift_report.append({
            "application": app_name,
            "status": "SYNCED" if is_synced else "OUT_OF_SYNC",
            "drift_detected": diffs
        })
        
    return {"apps": drift_report}

@app.post("/api/v1/gitops/reconcile/{app_name}")
def reconcile_app(app_name: str):
    if app_name not in GIT_DESIRED:
        return {"error": "App not defined in Git"}
    
    # Force live cluster to match Git desired state
    LIVE_CLUSTER[app_name] = GIT_DESIRED[app_name].copy()
    return {"status": "SUCCESS", "message": f"{app_name} live state synchronized with Git source of truth."}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8030)
