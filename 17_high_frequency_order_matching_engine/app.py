"""
High-Frequency Limit Order Book Matching Engine
Price-Time Priority (FIFO) matching engine simulation with L2 depth.
"""
from typing import List, Dict, Optional
from collections import deque
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Limit Order Book Matching Engine", version="1.0.0")

class Order(BaseModel):
    order_id: str
    symbol: str
    side: str  # "BUY" or "SELL"
    price: float
    quantity: int

class TradeExecution(BaseModel):
    buyer_order_id: str
    seller_order_id: str
    symbol: str
    executed_price: float
    quantity: int

class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        # Bids: sorted descending; Asks: sorted ascending
        self.bids: Dict[float, deque] = {}
        self.asks: Dict[float, deque] = {}

    def match_order(self, order: Order) -> List[TradeExecution]:
        trades = []
        if order.side == "BUY":
            while order.quantity > 0 and self.asks:
                best_ask = min(self.asks.keys())
                if order.price < best_ask:
                    break
                queue = self.asks[best_ask]
                seller_order = queue[0]
                matched_qty = min(order.quantity, seller_order.quantity)
                trades.append(TradeExecution(
                    buyer_order_id=order.order_id,
                    seller_order_id=seller_order.order_id,
                    symbol=self.symbol,
                    executed_price=best_ask,
                    quantity=matched_qty
                ))
                order.quantity -= matched_qty
                seller_order.quantity -= matched_qty
                if seller_order.quantity == 0:
                    queue.popleft()
                if not queue:
                    del self.asks[best_ask]

            if order.quantity > 0:
                if order.price not in self.bids:
                    self.bids[order.price] = deque()
                self.bids[order.price].append(order)

        else: # SELL
            while order.quantity > 0 and self.bids:
                best_bid = max(self.bids.keys())
                if order.price > best_bid:
                    break
                queue = self.bids[best_bid]
                buyer_order = queue[0]
                matched_qty = min(order.quantity, buyer_order.quantity)
                trades.append(TradeExecution(
                    buyer_order_id=buyer_order.order_id,
                    seller_order_id=order.order_id,
                    symbol=self.symbol,
                    executed_price=best_bid,
                    quantity=matched_qty
                ))
                order.quantity -= matched_qty
                buyer_order.quantity -= matched_qty
                if buyer_order.quantity == 0:
                    queue.popleft()
                if not queue:
                    del self.bids[best_bid]

            if order.quantity > 0:
                if order.price not in self.asks:
                    self.asks[order.price] = deque()
                self.asks[order.price].append(order)

        return trades

book = OrderBook("BTC-USD")

@app.post("/api/v1/orders/submit", response_model=List[TradeExecution])
def submit_order(order: Order):
    return book.match_order(order)

@app.get("/api/v1/orders/depth")
def get_depth():
    return {
        "symbol": book.symbol,
        "bids": {p: sum(o.quantity for o in q) for p, q in book.bids.items()},
        "asks": {p: sum(o.quantity for o in q) for p, q in book.asks.items()}
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8017)
