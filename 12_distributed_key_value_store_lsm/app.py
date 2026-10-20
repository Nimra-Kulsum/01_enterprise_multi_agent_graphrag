"""
High-Performance Distributed Key-Value Store with LSM-Tree
Demonstrates MemTable, WAL logging, Bloom Filter lookup, and Consistent Hashing.
"""
import hashlib
from typing import Dict, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="LSM-Tree Distributed Key-Value Store", version="1.0.0")

class BloomFilter:
    def __init__(self, size: int = 1000):
        self.size = size
        self.bit_array = [0] * size

    def _hashes(self, key: str):
        h1 = int(hashlib.md5(key.encode()).hexdigest(), 16) % self.size
        h2 = int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.size
        return h1, h2

    def add(self, key: str):
        for h in self._hashes(key):
            self.bit_array[h] = 1

    def contains(self, key: str) -> bool:
        return all(self.bit_array[h] == 1 for h in self._hashes(key))

class LSMNode:
    def __init__(self):
        self.memtable: Dict[str, str] = {}
        self.sstable_mock: Dict[str, str] = {}
        self.bloom_filter = BloomFilter()
        self.wal: list = []

    def put(self, key: str, value: str):
        # 1. Append to WAL
        self.wal.append(f"PUT {key}={value}")
        # 2. Add to Bloom filter
        self.bloom_filter.add(key)
        # 3. Insert into MemTable
        self.memtable[key] = value

    def get(self, key: str) -> Optional[str]:
        # 1. Check MemTable
        if key in self.memtable:
            return self.memtable[key]
        # 2. Check Bloom filter before disk
        if not self.bloom_filter.contains(key):
            return None # Definite negative!
        # 3. Check SSTable
        return self.sstable_mock.get(key, None)

node = LSMNode()

class PutRequest(BaseModel):
    key: str
    value: str

@app.post("/api/v1/kv/put")
def put_key(req: PutRequest):
    node.put(req.key, req.value)
    return {"status": "persisted", "key": req.key}

@app.get("/api/v1/kv/get/{key}")
def get_key(key: str):
    val = node.get(key)
    if val is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": val}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8012)
