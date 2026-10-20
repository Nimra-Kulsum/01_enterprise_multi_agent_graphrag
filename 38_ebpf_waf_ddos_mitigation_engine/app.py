"""
eBPF-Powered Web Application Firewall (WAF) & DDoS Defense
Layer 7 OWASP inspection simulation and IP reputation blacklist.
"""
import re
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="WAF & DDoS Mitigation Engine", version="1.0.0")

class IngressPacket(BaseModel):
    source_ip: str
    http_method: str
    path: str
    body: str

# IP Blacklist & Rate Tracker
BLOCKED_IPS = {"198.51.100.42", "203.0.113.88"}

WAF_RULES = [
    (r"(?i)(union\s+select|select\s+.*\s+from|drop\s+table)", "SQL_INJECTION"),
    (r"(?i)(\.\./\.\./|/etc/passwd)", "PATH_TRAVERSAL"),
    (r"(?i)(<script>|javascript:|onerror=)", "CROSS_SITE_SCRIPTING"),
    (r"(?i)(\|\s*nc|;\s*cat|\$\()", "COMMAND_INJECTION")
]

@app.post("/api/v1/waf/inspect")
def inspect_traffic(packet: IngressPacket):
    # Layer 3/4 Check (XDP Simulation)
    if packet.source_ip in BLOCKED_IPS:
        raise HTTPException(status_code=403, detail="XDP_DROP: Source IP blacklisted for DDoS involvement.")

    # Layer 7 Payload Deep Inspection
    combined_payload = f"{packet.path} {packet.body}"
    for pattern, attack_name in WAF_RULES:
        if re.search(pattern, combined_payload):
            # Auto-quarantine IP
            BLOCKED_IPS.add(packet.source_ip)
            raise HTTPException(status_code=403, detail=f"WAF_BLOCK: {attack_name} detected. IP quarantined.")

    return {"status": "ALLOW", "message": "Packet passed all layer-7 firewall rules."}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8038)
