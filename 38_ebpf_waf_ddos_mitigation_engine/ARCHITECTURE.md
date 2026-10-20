# Architecture Deep Dive: eBPF-Powered Web Application Firewall (WAF) & DDoS Defense

## 1. System Topology Overview
The **eBPF-Powered Web Application Firewall (WAF) & DDoS Defense** is engineered as a cloud-native, high-throughput microservice adhering to strict Twelve-Factor App principles and clean hexagonal architecture.

```mermaid
graph LR
    subgraph Ingestion
        A[Client Ingress / Load Balancer]
        B[Authentication & Rate Limiting]
    end
    subgraph ExecutionCore
        C[eBPF-Powered Web Application Firewall (WAF) & DDoS Defense Core Engine]
        D[Concurrency Manager / Workers]
    end
    subgraph PersistenceLayer
        E[(State Store / Database)]
        F[(Distributed Cache / Message Queue)]
    end
    subgraph Observability
        G[Prometheus Metrics]
        H[OpenTelemetry Traces]
    end

    A --> B
    B --> C
    C <--> D
    C <--> E
    C <--> F
    C -.-> G
    C -.-> H
```

---

## 2. Component Breakdown

### A. Ingress & Security Layer
- Validates request payload schemas strictly using Pydantic v2 data models.
- Enforces mutual TLS (mTLS) and token authentication before routing to internal handlers.
- Tracks ingress request rates with sliding-window token bucket limiters to prevent resource exhaustion.

### B. Execution Engine
- Pure asynchronous I/O (`asyncio`) event loop preventing blocking system calls.
- Encapsulated business domain logic decoupled from external framework dependencies.
- Modular handler pattern enabling zero-downtime hot-reloading and unit testability.

### C. State & Persistence Strategy
- Read-heavy paths served from in-memory distributed cache layers with deterministic invalidation TTLs.
- Write paths enforce ACID transaction semantics and cryptographic idempotency key deduplication.
- Failover replicas maintained across multiple independent cloud availability zones.

---

## 3. High-Load Scaling & Failure Mitigation

| Failure Scenario | Immediate Impact | Automated Mitigation Mechanism |
| :--- | :--- | :--- |
| **Downstream Service Crash** | Upstream requests accumulate | Circuit breaker trips within 3 consecutive errors; falls back to cached response. |
| **Sudden 10x Traffic Surge** | CPU / Memory pressure rises | Horizontal Pod Autoscaler (HPA) scales pods based on latency percentiles; rate limiter sheds excess load gracefully. |
| **Network Partition / Split-Brain** | Inconsistent node cluster state | Quorum-based consensus ($R + W > N$) and monotonic fencing tokens reject stale split-brain writes. |
| **Data Corruption / Bad Mutation** | Potential state drift | Append-only audit logs allow point-in-time state reconstruction with zero data loss. |

---

## 4. Benchmark Targets & Production SLAs
- **Availability Target:** 99.99% uptime (< 4.38 minutes downtime per month).
- **p95 Latency:** < 25ms under baseline load.
- **p99 Latency:** < 65ms under peak load.
- **Throughput Capability:** Scales linearly with horizontal container replicas.
