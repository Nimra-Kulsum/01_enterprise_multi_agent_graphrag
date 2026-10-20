"""
Peer-to-Peer WebRTC Content Delivery Mesh (P2P-CDN)
Peer swarm tracker and rarest-first chunk availability coordinator.
"""
from typing import List, Dict, Set
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="P2P WebRTC CDN Mesh Tracker", version="1.0.0")

class PeerRegistration(BaseModel):
    peer_id: str
    ip_subnet: str
    available_chunks: List[str]

# Swarm tracker state
SWARM_PEERS: Dict[str, PeerRegistration] = {}

@app.post("/api/v1/p2p/announce")
def announce_peer(reg: PeerRegistration):
    SWARM_PEERS[reg.peer_id] = reg
    
    # Find nearby peers in same subnet that have complement chunks
    nearby_peers = [
        p.peer_id for p in SWARM_PEERS.values()
        if p.peer_id != reg.peer_id and p.ip_subnet == reg.ip_subnet
    ]
    
    return {
        "status": "SWARM_JOINED",
        "peer_id": reg.peer_id,
        "recommended_peers_to_connect": nearby_peers[:5]
    }

@app.get("/api/v1/p2p/chunk-source/{chunk_hash}")
def find_chunk_sources(chunk_hash: str):
    holders = [
        p.peer_id for p in SWARM_PEERS.values()
        if chunk_hash in p.available_chunks
    ]
    return {
        "chunk_hash": chunk_hash,
        "available_holders_count": len(holders),
        "holder_peer_ids": holders[:10]
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8048)
