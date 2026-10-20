"""
Distributed Lock Manager & Leader Election Service
Monotonic fencing tokens, TTL leases, and mutual exclusion.
"""
import time
from typing import Optional, Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Distributed Lock Manager", version="1.0.0")

class LockEntry:
    def __init__(self, resource: str, owner_id: str, ttl_seconds: float, fencing_token: int):
        self.resource = resource
        self.owner_id = owner_id
        self.expires_at = time.time() + ttl_seconds
        self.fencing_token = fencing_token

    def is_expired(self) -> bool:
        return time.time() > self.expires_at

class LockManager:
    def __init__(self):
        self.locks: Dict[str, LockEntry] = {}
        self.token_counter = 1000

    def acquire(self, resource: str, client_id: str, ttl_seconds: float = 5.0) -> Optional[int]:
        now = time.time()
        current_lock = self.locks.get(resource)
        
        if current_lock and not current_lock.is_expired():
            if current_lock.owner_id == client_id:
                # Renew lease
                current_lock.expires_at = now + ttl_seconds
                return current_lock.fencing_token
            return None # Locked by another client

        # Grant lock
        self.token_counter += 1
        new_token = self.token_counter
        self.locks[resource] = LockEntry(resource, client_id, ttl_seconds, new_token)
        return new_token

    def release(self, resource: str, client_id: str) -> bool:
        current_lock = self.locks.get(resource)
        if current_lock and current_lock.owner_id == client_id:
            del self.locks[resource]
            return True
        return False

manager = LockManager()

class AcquireRequest(BaseModel):
    resource: str
    client_id: str
    ttl_seconds: float = 5.0

@app.post("/api/v1/locks/acquire")
def acquire_lock(req: AcquireRequest):
    token = manager.acquire(req.resource, req.client_id, req.ttl_seconds)
    if not token:
        raise HTTPException(status_code=409, detail="Resource currently locked")
    return {"acquired": True, "resource": req.resource, "fencing_token": token}

@app.post("/api/v1/locks/release")
def release_lock(resource: str, client_id: str):
    success = manager.release(resource, client_id)
    return {"released": success}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8020)
