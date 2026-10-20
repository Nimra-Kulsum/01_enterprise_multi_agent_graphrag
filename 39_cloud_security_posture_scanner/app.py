"""
Cloud Security Posture Management (CSPM) & Compliance Engine
Audits cloud asset configurations against CIS benchmarks.
"""
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Cloud Security Posture (CSPM) Auditor", version="1.0.0")

class CloudAsset(BaseModel):
    asset_id: str
    asset_type: str
    configuration: Dict[str, str]

class SecurityFinding(BaseModel):
    asset_id: str
    severity: str # "CRITICAL", "HIGH", "MEDIUM"
    cis_rule: str
    remediation_guidance: str

@app.post("/api/v1/cspm/scan", response_model=List[SecurityFinding])
def run_posture_scan(assets: List[CloudAsset]):
    findings = []
    
    for a in assets:
        # Rule 1: Public S3 Bucket
        if a.asset_type == "s3_bucket" and a.configuration.get("public_access_block") != "ENABLED":
            findings.append(SecurityFinding(
                asset_id=a.asset_id,
                severity="CRITICAL",
                cis_rule="CIS-AWS-2.1.5: S3 Bucket Public Read Access",
                remediation_guidance="Enable S3 Block Public Access on bucket and account level."
            ))
            
        # Rule 2: Open SSH Port 22
        if a.asset_type == "security_group" and a.configuration.get("port_22_ingress") == "0.0.0.0/0":
            findings.append(SecurityFinding(
                asset_id=a.asset_id,
                severity="CRITICAL",
                cis_rule="CIS-AWS-4.1: Ensure no security groups allow ingress from 0.0.0.0/0 to port 22",
                remediation_guidance="Restrict SSH ingress to corporate VPN IP CIDR only."
            ))
            
    return findings

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8039)
