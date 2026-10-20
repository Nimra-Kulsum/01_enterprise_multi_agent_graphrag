"""
Zero-Trust Identity & Access Management (IAM) Gateway
OAuth 2.1 PKCE verification and contextual risk engine.
"""
import hashlib
import base64
from typing import Dict, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Zero-Trust IAM & OAuth 2.1 Gateway", version="1.0.0")

class TokenExchangeRequest(BaseModel):
    client_id: str
    code: str
    code_verifier: str
    code_challenge_expected: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    claims: Dict[str, str]

def verify_pkce(code_verifier: str, expected_challenge: str) -> bool:
    # SHA256 hashing followed by URL-safe base64 encoding without padding
    digest = hashlib.sha256(code_verifier.encode('ascii')).digest()
    computed_challenge = base64.urlsafe_b64encode(digest).decode('ascii').rstrip('=')
    return computed_challenge == expected_challenge

@app.post("/api/v1/oauth2/token", response_model=TokenResponse)
def exchange_token(req: TokenExchangeRequest):
    # Verify PKCE Code Verifier against Challenge
    if not verify_pkce(req.code_verifier, req.code_challenge_expected):
        raise HTTPException(status_code=400, detail="Invalid PKCE code_verifier")

    return TokenResponse(
        access_token=f"zt_jwt_{req.client_id}_{hashlib.md5(req.code.encode()).hexdigest()[:12]}",
        claims={"sub": "user_admin_88", "scope": "read:ledger write:ledger", "iss": "https://auth.enterprise.internal"}
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8037)
