"""
Enterprise LLM Guardrails & PII Security Firewall
Detects prompt injections, jailbreaks, and sensitive data leakage.
"""
import re
from typing import List, Dict, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Enterprise LLM Security Firewall", version="1.0.0")

class SecurityCheckRequest(BaseModel):
    prompt: str
    user_id: str
    tenant_id: str

class SecurityCheckResponse(BaseModel):
    is_safe: bool
    risk_level: str
    detected_threats: List[str]
    sanitized_prompt: str

KNOWN_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"disregard all prior rules",
    r"you are now in developer mode",
    r"dan mode enabled",
    r"system override"
]

@app.post("/api/v1/inspect", response_model=SecurityCheckResponse)
def inspect_prompt(req: SecurityCheckRequest):
    threats = []
    lower_prompt = req.prompt.lower()
    
    # 1. Check Injection Signatures
    for pattern in KNOWN_INJECTION_PATTERNS:
        if re.search(pattern, lower_prompt):
            threats.append(f"Prompt Injection Pattern Detected: '{pattern}'")

    # 2. Check PII
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', req.prompt))
    if has_email:
        threats.append("Sensitive PII: Email Address present")

    # Sanitization
    sanitized = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', req.prompt)

    is_safe = len(threats) == 0
    risk = "HIGH" if "Prompt Injection" in "".join(threats) else ("MEDIUM" if threats else "LOW")

    return SecurityCheckResponse(
        is_safe=is_safe,
        risk_level=risk,
        detected_threats=threats,
        sanitized_prompt=sanitized
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8007)
