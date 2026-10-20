"""
Client-Side WebAssembly In-Browser Analytics Engine
Serves WebAssembly analytical bundles and simulates columnar SQL execution.
"""
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Wasm Client-Side Analytics Platform", version="1.0.0")

class ColumnarQuery(BaseModel):
    selected_column: str
    aggregation: str # "SUM", "AVG", "COUNT"

# Mock in-memory columnar dataset (representing Parquet columns in memory)
COLUMNAR_DATA = {
    "transaction_amount": [120.5, 450.0, 32.1, 890.4, 55.0, 1200.0, 310.2],
    "user_age": [28, 34, 45, 23, 52, 41, 30]
}

@app.post("/api/v1/analytics/query")
def execute_columnar_query(query: ColumnarQuery):
    if query.selected_column not in COLUMNAR_DATA:
        return {"error": "Column not found in dataset"}

    col = COLUMNAR_DATA[query.selected_column]
    
    if query.aggregation == "SUM":
        val = sum(col)
    elif query.aggregation == "AVG":
        val = sum(col) / len(col)
    else:
        val = len(col)

    return {
        "execution_location": "CLIENT_WASM_SANDBOX",
        "column": query.selected_column,
        "aggregation": query.aggregation,
        "result": round(val, 2),
        "rows_processed": len(col)
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8047)
