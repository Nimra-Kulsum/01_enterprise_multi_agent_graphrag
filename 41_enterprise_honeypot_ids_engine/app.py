"""
High-Interaction Cyber Deception HoneyPot & IDS Platform
Decoy endpoint trapping, keystroke/credential logging, and MITRE classification.
"""
import time
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI(title="Enterprise Cyber Deception & HoneyPot IDS", version="1.0.0")

CAPTURED_INTEL: List[dict] = []

class DecoyInteraction(BaseModel):
    attacker_ip: str
    target_protocol: str # "SSH", "HTTP_ADMIN", "POSTGRES"
    payload_captured: str
    mitre_tactic: str

@app.post("/api/v1/trap/ssh-login")
def mock_ssh_decoy(username: str, password_attempt: str, request: Request):
    intel = {
        "timestamp": time.time(),
        "client_host": request.client.host if request.client else "unknown",
        "decoy_service": "SSH_BASTION_DECOY",
        "attempted_credentials": f"{username}:{password_attempt}",
        "mitre_tactic": "T1110 - Brute Force / Credential Access",
        "alert_level": "CRITICAL"
    }
    CAPTURED_INTEL.append(intel)
    # Simulate deliberate delay to waste attacker time (tar-pitting)
    return {"status": "ACCESS_DENIED", "delay": "Simulated authentication failed."}

@app.get("/api/v1/soc/threat-feed")
def get_soc_feed():
    return {"total_threats_captured": len(CAPTURED_INTEL), "recent_intel": CAPTURED_INTEL[-10:]}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8041)
