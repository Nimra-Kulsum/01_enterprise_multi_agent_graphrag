"""
Multimodal Intelligent Document Processing (IDP) Engine
Extracts structured financial fields and redacts PII from invoices.
"""
import re
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Multimodal Document Intelligence Service", version="1.0.0")

class InvoiceLineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float

class ExtractedInvoice(BaseModel):
    invoice_number: str
    vendor_name: str
    date: str
    line_items: List[InvoiceLineItem]
    subtotal: float
    tax: float
    total_amount: float
    is_pii_redacted: bool

class DocumentProcessingRequest(BaseModel):
    raw_text_content: str
    redact_pii: bool = True

def redact_sensitive_pii(text: str) -> str:
    # Redact SSN: XXX-XX-XXXX
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED_SSN]', text)
    # Redact Credit Cards: 16 digits
    text = re.sub(r'\b(?:\d{4}[ -]?){3}\d{4}\b', '[REDACTED_CARD]', text)
    return text

@app.post("/api/v1/extract-invoice", response_model=ExtractedInvoice)
def process_document(req: DocumentProcessingRequest):
    sanitized_text = redact_sensitive_pii(req.raw_text_content) if req.redact_pii else req.raw_text_content
    
    # Deterministic Schema Extraction Simulator
    return ExtractedInvoice(
        invoice_number="INV-2026-8891",
        vendor_name="Cloud Infrastructure Corp",
        date="2026-10-15",
        line_items=[
            InvoiceLineItem(description="GPU Node Allocation (A100)", quantity=4, unit_price=2.50, total=10.0),
            InvoiceLineItem(description="NVMe Block Storage 2TB", quantity=1, unit_price=45.0, total=45.0)
        ],
        subtotal=55.0,
        tax=4.95,
        total_amount=59.95,
        is_pii_redacted=req.redact_pii
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)
