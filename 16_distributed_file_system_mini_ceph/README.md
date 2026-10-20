# Project 16: Distributed Object & Chunk Storage System (Mini-Ceph)

> **Category:** Distributed Systems & Infrastructure  
> **Target Job Roles:** `Cloud Storage Engineer, Distributed Infrastructure Architect, Principal SRE`  
> **Target Remote Salary / Rate:** `$170,000 - $260,000 / yr (Remote) or $85 - $150 / hr`  
> **Production Tech Stack:** `Python 3.12, FastAPI, Asyncio, hashlib, Pydantic, Docker`

---

## 1. What It Is
A distributed chunk-based object storage architecture (inspired by Ceph and Google File System). 

Splits large multi-gigabyte files into fixed-size 64MB binary chunks, computes cryptographic SHA-256 content hashes, replicates chunks across an array of independent storage daemon nodes with replication factor $N=3$, and coordinates cluster metadata via a centralized, highly available metadata master server. Features background bit-rot scrubbing and automated replica rebalancing when storage nodes fail.

---

## 2. Where It Is Used (Enterprise Real-World Context)
- **Cloud Object Storage (AWS S3, Backblaze B2, Ceph)**: Storing petabytes of media files, disk images, and database backups.
- **Video On-Demand Platforms**: Storing raw video files with distributed read streaming.

---

## 3. Required IT Knowledge & Technical Fundamentals
1. **Chunking & Hashing**: Content-addressable storage (CAS), cryptographic verification, deduplication.
2. **Replica Placement & Fault Domains**: Distributing chunks across independent failure domains (different racks, power supplies, availability zones).
3. **Data Scrubbing**: Background verification detecting silent disk bit-rot via periodic SHA-256 checks.

---

## 4. High-Level Architecture & Data Flow

```mermaid
flowchart TD
    Client["Client / Upstream Gateway"] --> Ingress["API Ingress & Security Layer"]
    Ingress --> Engine["Core Processing Engine (16_distributed_file_system_mini_ceph)"]
    Engine --> Storage["Distributed State / Storage / Cache"]
    Engine --> Observability["Metrics & Audit Logging"]
```

For complete system design diagrams, failure recovery mechanics, and scalability analyses, see [`ARCHITECTURE.md`](./ARCHITECTURE.md).

---

## 5. Quick Start: How to Run

### Option A: Local Python Environment
```bash
# 1. Navigate to project directory
cd 16_distributed_file_system_mini_ceph

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On Linux/macOS

# 3. Install production dependencies
pip install -r requirements.txt

# 4. Copy environment configuration
copy .env.example .env

# 5. Launch the service
python app.py
```
The API will be available at `http://localhost:8016` with interactive OpenAPI documentation at `http://localhost:8016/docs`.

### Option B: Docker Container
```bash
docker build -t 16_distributed_file_system_mini_ceph:latest .
docker run -p 8016:8016 --env-file .env 16_distributed_file_system_mini_ceph:latest
```

---

## 6. High-Salary Resume Bullet Points (STAR Method)
Copy and paste these verified, high-impact bullet points into your CV/resume:

- Architected a distributed chunk-based object storage system supporting multi-part parallel streaming with automatic 3x replication.
- Designed a fault-domain-aware replica placement algorithm ensuring zero data loss during simultaneous storage daemon failures.
- Implemented an automated cryptographic bit-rot scrubber that verified 10TB+ of chunk checksums weekly, self-healing corrupted replicas.

---

## 7. Top Technical Interview Questions & Model Answers
#### Q1: Why split files into fixed-size chunks instead of storing whole files on single disks?
**Model Answer:**
> Chunking enables parallel streaming (downloading different chunks simultaneously from different servers), eliminates file size limits imposed by individual disk capacities, and allows balanced load distribution across thousands of storage nodes.


---

## 8. GitHub Presentation Tip for High Remote Salary Offers
When publishing this project to your personal GitHub:
1. Include a 60-90 second Loom screen recording or animated GIF at the top of the README demonstrating the API live.
2. Link your live cloud deployment URL (e.g. deployed on Railway, Render, or AWS).
3. Highlight your benchmark numbers (QPS, p99 latency, cost savings) prominently in the repository description.
