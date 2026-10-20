"""
High-Speed Deep Packet Inspection (DPI) & Flow Analyzer
Binary packet header parsing simulation and TLS SNI classification.
"""
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Deep Packet Inspection (DPI) Service", version="1.0.0")

class RawPacket(BaseModel):
    packet_id: int
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str  # "TCP", "UDP"
    payload_hex: str

class FlowAnalysisReport(BaseModel):
    packet_id: int
    detected_application: str
    domain_sni_extracted: str
    is_suspicious: bool

@app.post("/api/v1/dpi/analyze-packet", response_model=FlowAnalysisReport)
def inspect_packet(pkt: RawPacket):
    # Simulated protocol and SNI classification
    detected_app = "UNKNOWN"
    sni = "None"
    
    if pkt.dst_port == 443:
        detected_app = "TLS_HTTPS"
        sni = "internal-service.corporate.net"
    elif pkt.dst_port == 53:
        detected_app = "DNS"
    elif pkt.dst_port == 80:
        detected_app = "HTTP_CLEARTEXT"

    return FlowAnalysisReport(
        packet_id=pkt.packet_id,
        detected_application=detected_app,
        domain_sni_extracted=sni,
        is_suspicious=(pkt.dst_port == 4444 or detected_app == "HTTP_CLEARTEXT")
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8045)
