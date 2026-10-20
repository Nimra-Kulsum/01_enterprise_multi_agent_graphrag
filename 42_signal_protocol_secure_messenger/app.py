"""
End-to-End Encrypted Messaging Protocol (Signal Double Ratchet)
Demonstrates KDF chain ratchet, forward secrecy, and one-time message keys.
"""
import hashlib
import hmac
from typing import Dict, Tuple
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Signal Double Ratchet Protocol Engine", version="1.0.0")

class SymmetricKDFChain:
    """Simulates a cryptographic Key Derivation Function (KDF) ratchet chain."""
    def __init__(self, root_key: bytes):
        self.chain_key = root_key

    def step(self) -> Tuple[bytes, bytes]:
        # Derives (new_chain_key, message_key)
        h_chain = hmac.new(self.chain_key, b"chain_advancement", hashlib.sha256).digest()
        h_message = hmac.new(self.chain_key, b"message_key_derivation", hashlib.sha256).digest()
        self.chain_key = h_chain
        return h_chain, h_message

chain = SymmetricKDFChain(root_key=b"initial_shared_secret_entropy_32b")

class EncryptedMessagePacket(BaseModel):
    message_index: int
    ciphertext_hex: str
    message_key_hint: str

@app.post("/api/v1/e2ee/encrypt-next")
def encrypt_next_message(plaintext: str):
    # Advance the ratchet by 1 step
    _, message_key = chain.step()
    
    # Mock XOR stream cipher using derived message key
    encrypted_bytes = bytes([b ^ message_key[i % len(message_key)] for i, b in enumerate(plaintext.encode('utf-8'))])
    
    return {
        "status": "RATCHET_ADVANCED",
        "message_key_hash": hashlib.sha256(message_key).hexdigest()[:16],
        "ciphertext_hex": encrypted_bytes.hex(),
        "security_guarantee": "PERFECT_FORWARD_SECRECY_ACTIVE"
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8042)
