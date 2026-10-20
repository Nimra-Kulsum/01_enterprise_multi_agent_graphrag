"""
Distributed Object & Chunk Storage System (Mini-Ceph)
Demonstrates file chunking, SHA-256 content addressing, and replica metadata mapping.
"""
import hashlib
from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Distributed Chunk Storage Service", version="1.0.0")

class ChunkMetadata(BaseModel):
    chunk_index: int
    chunk_hash: str
    byte_size: int
    replica_nodes: List[str]

class FileMetadata(BaseModel):
    filename: str
    total_size_bytes: int
    chunks: List[ChunkMetadata]

# Master metadata table
files_registry: Dict[str, FileMetadata] = {}

class UploadSimulationRequest(BaseModel):
    filename: str
    file_content: str
    chunk_size: int = 16 # Small simulated chunk size for demo

@app.post("/api/v1/storage/upload", response_model=FileMetadata)
def upload_file_simulation(req: UploadSimulationRequest):
    content_bytes = req.file_content.encode('utf-8')
    total_size = len(content_bytes)
    chunks_meta = []
    
    idx = 0
    for offset in range(0, total_size, req.chunk_size):
        chunk_slice = content_bytes[offset:offset + req.chunk_size]
        chunk_hash = hashlib.sha256(chunk_slice).hexdigest()[:16]
        
        # Replica placement strategy: distribute across mock nodes
        nodes = [f"storage-node-{(idx + i) % 3 + 1}" for i in range(3)]
        
        chunks_meta.append(ChunkMetadata(
            chunk_index=idx,
            chunk_hash=chunk_hash,
            byte_size=len(chunk_slice),
            replica_nodes=nodes
        ))
        idx += 1

    file_meta = FileMetadata(
        filename=req.filename,
        total_size_bytes=total_size,
        chunks=chunks_meta
    )
    files_registry[req.filename] = file_meta
    return file_meta

@app.get("/api/v1/storage/meta/{filename}", response_model=FileMetadata)
def get_file_metadata(filename: str):
    if filename not in files_registry:
        raise HTTPException(status_code=404, detail="File metadata not found")
    return files_registry[filename]

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8016)
