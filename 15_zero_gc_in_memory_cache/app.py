"""
Ultra-Fast Zero-GC In-Memory Cache with LRU
Demonstrates O(1) Doubly Linked List + Hash Map LRU eviction.
"""
from typing import Optional, Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="High-Performance LRU In-Memory Cache", version="1.0.0")

class Node:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class LRUCacheEngine:
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.lookup: Dict[str, Node] = {}
        # Sentinel dummy nodes
        self.head = Node("__HEAD__", "")
        self.tail = Node("__TAIL__", "")
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: str) -> Optional[str]:
        if key in self.lookup:
            node = self.lookup[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return None

    def put(self, key: str, value: str):
        if key in self.lookup:
            self._remove(self.lookup[key])
        elif len(self.lookup) >= self.capacity:
            # Evict least recently used (at tail.prev)
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.lookup[lru_node.key]

        new_node = Node(key, value)
        self._add_to_front(new_node)
        self.lookup[key] = new_node

cache = LRUCacheEngine(capacity=3)

class SetItemRequest(BaseModel):
    key: str
    value: str

@app.post("/api/v1/cache/set")
def set_item(req: SetItemRequest):
    cache.put(req.key, req.value)
    return {"status": "stored", "key": req.key}

@app.get("/api/v1/cache/get/{key}")
def get_item(key: str):
    val = cache.get(key)
    if val is None:
        raise HTTPException(status_code=404, detail="Cache miss")
    return {"key": key, "value": val}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8015)
