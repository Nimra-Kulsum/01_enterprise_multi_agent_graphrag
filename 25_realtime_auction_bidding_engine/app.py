"""
High-Concurrency Real-Time Bidding & Auction Engine
Optimistic concurrency versioning, anti-sniping timer extension, and bid broadcast.
"""
import time
from typing import Dict, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Real-Time Auction & Bidding Engine", version="1.0.0")

class AuctionItem(BaseModel):
    auction_id: str
    item_title: str
    current_highest_bid: float
    highest_bidder: str
    ends_at: float
    version: int

# In-memory auction state
AUCTIONS: Dict[str, AuctionItem] = {
    "lot_42": AuctionItem(
        auction_id="lot_42",
        item_title="Rare 1968 Vintage Chronograph",
        current_highest_bid=12000.0,
        highest_bidder="collector_9",
        ends_at=time.time() + 60.0, # Ends in 60s
        version=1
    )
}

class BidSubmission(BaseModel):
    bidder_id: str
    bid_amount: float
    expected_version: int

@app.post("/api/v1/auctions/{auction_id}/bid")
def place_bid(auction_id: str, bid: BidSubmission):
    if auction_id not in AUCTIONS:
        raise HTTPException(status_code=404, detail="Auction not found")
        
    auction = AUCTIONS[auction_id]
    now = time.time()
    
    if now > auction.ends_at:
        raise HTTPException(status_code=400, detail="Auction has already closed")

    # Optimistic Concurrency Control (OCC) Check
    if bid.expected_version != auction.version:
        raise HTTPException(status_code=409, detail="Price was updated by another bidder. Refresh and retry.")

    min_increment = 250.0
    if bid.bid_amount < auction.current_highest_bid + min_increment:
        raise HTTPException(status_code=400, detail=f"Minimum required bid is {auction.current_highest_bid + min_increment}")

    # Atomic Update
    auction.current_highest_bid = bid.bid_amount
    auction.highest_bidder = bid.bidder_id
    auction.version += 1

    # Anti-Sniping Rule: If bid placed within last 30s, extend auction by 60s
    time_remaining = auction.ends_at - now
    if time_remaining < 30.0:
        auction.ends_at = now + 60.0

    return {
        "status": "BID_ACCEPTED",
        "new_highest_bid": auction.current_highest_bid,
        "new_version": auction.version,
        "seconds_remaining": round(auction.ends_at - time.time(), 1)
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8025)
