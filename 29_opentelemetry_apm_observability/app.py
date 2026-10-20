"""
Distributed Tracing & OpenTelemetry APM Platform
Trace parent header parsing, span tree aggregation, and latency percentiles.
"""
import uuid
import time
from typing import List, Dict, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException
import uvicorn

app = FastAPI(title="Distributed Tracing & APM Collector", version="1.0.0")

class Span(BaseModel):
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    service_name: str
    operation: str
    duration_ms: float
    status_code: int = 200

# Central trace storage
TRACES: Dict[str, List[Span]] = {}

@app.post("/api/v1/traces/spans")
def record_span(span: Span):
    if span.trace_id not in TRACES:
        TRACES[span.trace_id] = []
    TRACES[span.trace_id].append(span)
    return {"status": "recorded", "trace_id": span.trace_id, "span_id": span.span_id}

@app.get("/api/v1/traces/{trace_id}")
def get_trace_tree(trace_id: str):
    if trace_id not in TRACES:
        raise HTTPException(status_code=404, detail="Trace ID not found")
    spans = TRACES[trace_id]
    total_latency = sum(s.duration_ms for s in spans if not s.parent_span_id)
    return {
        "trace_id": trace_id,
        "total_spans": len(spans),
        "root_latency_ms": total_latency,
        "spans": spans
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8029)
