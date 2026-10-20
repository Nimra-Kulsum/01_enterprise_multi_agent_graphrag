"""
Decentralized AMM & Cross-Chain Bridge Simulator
Constant product x * y = k liquidity pool and slippage simulation.
"""
from typing import Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="DeFi AMM & Cross-Chain Bridge Engine", version="1.0.0")

class LiquidityPool:
    def __init__(self, reserve_a: float, reserve_b: float, fee_percent: float = 0.003):
        self.reserve_a = reserve_a
        self.reserve_b = reserve_b
        self.fee = fee_percent # 0.3% Uniswap fee

    def swap_a_for_b(self, amount_a_in: float) -> dict:
        amount_a_with_fee = amount_a_in * (1.0 - self.fee)
        # New reserve A = reserve_a + amount_a_with_fee
        # New reserve B = (reserve_a * reserve_b) / New reserve A
        new_reserve_a = self.reserve_a + amount_a_with_fee
        new_reserve_b = (self.reserve_a * self.reserve_b) / new_reserve_a
        amount_b_out = self.reserve_b - new_reserve_b

        spot_price_before = self.reserve_b / self.reserve_a
        effective_price = amount_b_out / amount_a_in
        slippage_percent = (1.0 - (effective_price / spot_price_before)) * 100.0

        self.reserve_a += amount_a_in
        self.reserve_b -= amount_b_out

        return {
            "amount_in_a": amount_a_in,
            "amount_out_b": round(amount_b_out, 4),
            "effective_price": round(effective_price, 4),
            "slippage_percent": round(slippage_percent, 2),
            "new_pool_reserves": {"token_a": round(self.reserve_a, 2), "token_b": round(self.reserve_b, 2)}
        }

pool = LiquidityPool(reserve_a=1000.0, reserve_b=3000000.0) # ETH / USDC pool

@app.post("/api/v1/amm/swap")
def execute_swap(amount_eth_in: float):
    if amount_eth_in <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    return pool.swap_a_for_b(amount_eth_in)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8027)
