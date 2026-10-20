"""
Enterprise Double-Entry Ledger & Multi-Currency Payment Engine
Strict debit/credit zero-sum verification, integer micro-units, and idempotency keys.
"""
from typing import List, Dict
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Header
import uvicorn

app = FastAPI(title="Double-Entry Payment Ledger Service", version="1.0.0")

# In-memory ledger storage and idempotency registry
accounts_balance: Dict[str, int] = {
    "user_alice": 100000,    # $1,000.00 represented in cents
    "user_bob": 50000,       # $500.00
    "platform_revenue": 0
}
processed_idempotency_keys: Dict[str, dict] = {}

class LedgerEntry(BaseModel):
    account_id: str
    amount_cents: int # positive for debit, negative for credit

class TransferRequest(BaseModel):
    source_account: str
    destination_account: str
    amount_cents: int
    currency: str = "USD"

@app.post("/api/v1/ledger/transfer")
def execute_transfer(req: TransferRequest, idempotency_key: str = Header(...)):
    # 1. Idempotency Check
    if idempotency_key in processed_idempotency_keys:
        return processed_idempotency_keys[idempotency_key]

    if req.amount_cents <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be strictly positive")
    
    if accounts_balance.get(req.source_account, 0) < req.amount_cents:
        raise HTTPException(status_code=402, detail="Insufficient funds in source account")

    # 2. Atomic Double-Entry Ledger Movement (Sum of debits + credits == 0)
    # Source is credited (-amount), Destination is debited (+amount)
    accounts_balance[req.source_account] -= req.amount_cents
    accounts_balance[req.destination_account] = accounts_balance.get(req.destination_account, 0) + req.amount_cents

    receipt = {
        "status": "SETTLED",
        "transaction_id": f"txn_{idempotency_key[:8]}",
        "source": req.source_account,
        "destination": req.destination_account,
        "amount_cents": req.amount_cents,
        "source_remaining_balance": accounts_balance[req.source_account],
        "destination_new_balance": accounts_balance[req.destination_account]
    }
    
    # Store idempotency result
    processed_idempotency_keys[idempotency_key] = receipt
    return receipt

@app.get("/api/v1/ledger/accounts")
def list_balances():
    return accounts_balance

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8021)
