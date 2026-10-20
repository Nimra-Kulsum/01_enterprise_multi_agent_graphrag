"""
Multi-Cloud FinOps Cost Optimization & Idle Resource Sweeper
Scans for unattached storage, idle compute, and calculates projected monthly savings.
"""
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Cloud FinOps Cost Optimizer", version="1.0.0")

class WasteItem(BaseModel):
    resource_id: str
    resource_type: str
    monthly_cost_usd: float
    reason: str
    action_recommended: str

@app.get("/api/v1/finops/audit-report")
def run_cost_audit():
    # Simulated discovery of orphaned cloud resources
    findings = [
        WasteItem(resource_id="vol-0a817bca8", resource_type="EBS Volume", monthly_cost_usd=96.0, reason="Unattached for 42 days", action_recommended="Snapshot and Delete"),
        WasteItem(resource_id="eipalloc-01726a", resource_type="Elastic IP", monthly_cost_usd=7.20, reason="Not associated with running instance", action_recommended="Release IP"),
        WasteItem(resource_id="i-091823761", resource_type="EC2 Instance (r5.2xlarge)", monthly_cost_usd=365.0, reason="Average CPU < 1.2% over past 14 days", action_recommended="Downsize to t3.medium or Terminate")
    ]
    
    total_monthly_waste = sum(f.monthly_cost_usd for f in findings)
    
    return {
        "status": "AUDIT_COMPLETED",
        "total_monthly_savings_potential_usd": round(total_monthly_waste, 2),
        "total_annualized_savings_usd": round(total_monthly_waste * 12, 2),
        "waste_items_found": len(findings),
        "recommendations": findings
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8035)
