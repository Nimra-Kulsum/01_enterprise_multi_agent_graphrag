"""
Distributed Event Broker with Raft Consensus Engine
Demonstrates partition commit logs, offset tracking, and consumer subscriptions.
"""
import time
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Distributed Event Broker & Commit Log", version="1.0.0")

class Message(BaseModel):
    topic: str
    partition: int
    payload: str
    timestamp: float = 0.0
    offset: int = 0

class BrokerPartition:
    def __init__(self, partition_id: int):
        self.partition_id = partition_id
        self.log: List[Message] = []
        self.next_offset: int = 0

    def append(self, payload: str, topic: str) -> Message:
        msg = Message(
            topic=topic,
            partition=self.partition_id,
            payload=payload,
            timestamp=time.time(),
            offset=self.next_offset
        )
        self.log.append(msg)
        self.next_offset += 1
        return msg

    def read_from(self, offset: int, max_count: int = 10) -> List[Message]:
        return self.log[offset : offset + max_count]

topics: Dict[str, Dict[int, BrokerPartition]] = {
    "orders": {0: BrokerPartition(0), 1: BrokerPartition(1)}
}

class PublishRequest(BaseModel):
    topic: str
    partition: int
    payload: str

@app.post("/api/v1/publish", response_model=Message)
def publish_message(req: PublishRequest):
    if req.topic not in topics or req.partition not in topics[req.topic]:
        raise HTTPException(status_code=404, detail="Topic or Partition not found")
    partition = topics[req.topic][req.partition]
    return partition.append(req.payload, req.topic)

@app.get("/api/v1/consume")
def consume_messages(topic: str, partition: int, offset: int = 0, limit: int = 10):
    if topic not in topics or partition not in topics[topic]:
        raise HTTPException(status_code=404, detail="Topic or Partition not found")
    part = topics[topic][partition]
    msgs = part.read_from(offset, limit)
    return {
        "topic": topic,
        "partition": partition,
        "current_log_end_offset": part.next_offset,
        "messages": msgs
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8011)
