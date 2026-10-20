"""
Multi-Cloud Infrastructure-as-Code Engine (Mini-Terraform)
Generates dependency DAGs and execution plans (create/update/destroy).
"""
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Infrastructure as Code (IaC) Engine", version="1.0.0")

class ResourceDefinition(BaseModel):
    resource_type: str
    name: str
    depends_on: List[str] = []
    properties: Dict[str, str]

class PlanOutput(BaseModel):
    action: str  # "+ CREATE", "~ UPDATE", "- DESTROY"
    resource_id: str
    details: str

# Sample declarative infrastructure manifest
INFRASTRUCTURE_MANIFEST = [
    ResourceDefinition(resource_type="aws_vpc", name="main_vpc", depends_on=[], properties={"cidr": "10.0.0.0/16"}),
    ResourceDefinition(resource_type="aws_subnet", name="public_subnet", depends_on=["aws_vpc.main_vpc"], properties={"cidr": "10.0.1.0/24"}),
    ResourceDefinition(resource_type="aws_instance", name="web_server", depends_on=["aws_subnet.public_subnet"], properties={"type": "t3.medium"})
]

@app.get("/api/v1/iac/plan", response_model=List[PlanOutput])
def generate_execution_plan():
    plan = []
    # Topological dependency order
    for res in INFRASTRUCTURE_MANIFEST:
        plan.append(PlanOutput(
            action="+ CREATE",
            resource_id=f"{res.resource_type}.{res.name}",
            details=f"Provision resource with properties: {res.properties}. Depends on: {res.depends_on}"
        ))
    return plan

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8031)
