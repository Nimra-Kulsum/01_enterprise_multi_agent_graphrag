"""
Privacy-Preserving Federated Learning Network
Simulates Federated Averaging (FedAvg) with Differential Privacy noise.
"""
from typing import List, Dict
import numpy as np
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Federated Learning Privacy Network", version="1.0.0")

class ClientUpdate(BaseModel):
    client_id: str
    sample_count: int
    weights_summary: List[float]

class AggregationRequest(BaseModel):
    round_number: int
    client_updates: List[ClientUpdate]
    differential_privacy_epsilon: float = 1.0

class AggregationResponse(BaseModel):
    round_number: int
    aggregated_weights: List[float]
    clients_participated: int
    privacy_budget_consumed: float

@app.post("/api/v1/aggregate-round", response_model=AggregationResponse)
def aggregate_round(req: AggregationRequest):
    if not req.client_updates:
        return AggregationResponse(round_number=req.round_number, aggregated_weights=[], clients_participated=0, privacy_budget_consumed=0.0)

    total_samples = sum(u.sample_count for u in req.client_updates)
    weights_len = len(req.client_updates[0].weights_summary)
    aggregated = np.zeros(weights_len)

    # Federated Averaging (FedAvg)
    for update in req.client_updates:
        weight_factor = update.sample_count / total_samples
        aggregated += np.array(update.weights_summary) * weight_factor

    # Differential Privacy: Inject calibrated Gaussian noise
    noise_sigma = 1.0 / req.differential_privacy_epsilon * 0.01
    noise = np.random.normal(0, noise_sigma, size=weights_len)
    private_weights = (aggregated + noise).round(4).tolist()

    return AggregationResponse(
        round_number=req.round_number,
        aggregated_weights=private_weights,
        clients_participated=len(req.client_updates),
        privacy_budget_consumed=req.differential_privacy_epsilon
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8009)
