"""
Global Distributed Token Bucket Rate Limiter
Atomic sliding-window token bucket simulation.
"""
import time
from typing import Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Response, status
import uvicorn

app = FastAPI(title="Distributed Rate Limiter Service", version="1.0.0")

class RateLimitBucket:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill = time.time()

    def allow_request(self, cost: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        # Refill tokens
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False

# In-memory tenant buckets (in production: Redis Cluster)
buckets: Dict[str, RateLimitBucket] = {
    "tenant_free": RateLimitBucket(capacity=5, refill_rate_per_sec=1.0),
    "tenant_enterprise": RateLimitBucket(capacity=100, refill_rate_per_sec=50.0)
}

@app.get("/api/v1/resource")
def get_protected_resource(tenant_id: str, response: Response):
    bucket = buckets.get(tenant_id, buckets["tenant_free"])
    
    if not bucket.allow_request():
        response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
        response.headers["Retry-After"] = "2"
        return {"error": "Too Many Requests", "message": "Rate limit exceeded. Try again in 2 seconds."}

    response.headers["X-RateLimit-Remaining"] = str(int(bucket.tokens))
    return {"status": "success", "data": "Protected enterprise resource accessed successfully."}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8013)
