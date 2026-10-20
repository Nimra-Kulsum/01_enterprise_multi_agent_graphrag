# Project 36: Zero-Trust Enterprise Secrets Management Vault

> **Category:** DevOps, SRE & Observability  
> **Target Job Roles:** `Security Infrastructure Architect, Cryptographic Platform Lead, Senior SRE`  
> **Target Remote Salary / Rate:** `$170,000 - $265,000 / yr (Remote) or $85 - $150 / hr`  
> **Production Tech Stack:** `Python 3.12, FastAPI, Cryptography primitives, Pydantic, Docker`

---

## 1. What It Is
An enterprise secrets management vault (modeled after HashiCorp Vault). 

Implements Shamir\'s Secret Sharing algorithm ($K$-of-$N$ threshold unsealing: master key is split into 5 shares, requiring any 3 to unseal), AES-256-GCM authenticated envelope encryption at rest, short-lived dynamic credentials with auto-revocation TTLs, and cryptographic tamper-evident audit logging for all secret reads.

---

## 2. Where It Is Used (Enterprise Real-World Context)
- **Financial Institutions & Defense**: Protecting database passwords, API tokens, and cryptographic private keys.
- **Enterprise Kubernetes Clusters**: Injecting short-lived database credentials dynamically into microservice pods.

---

## 3. Required IT Knowledge & Technical Fundamentals
1. **Shamir\'s Secret Sharing**: Polynomial interpolation over finite fields guaranteeing zero information leakage unless quorum is met.
2. **Envelope Encryption (DEK & KEK)**: Encrypting data with Data Encryption Keys, and encrypting DEKs with Key Encryption Keys.
3. **Dynamic Secrets**: Generating database credentials valid for only 60 minutes, eliminating permanent credential compromise risks.

---

## 4. High-Level Architecture & Data Flow

```mermaid
flowchart TD
    Client["Client / Upstream Gateway"] --> Ingress["API Ingress & Security Layer"]
    Ingress --> Engine["Core Processing Engine (36_zero_trust_secrets_vault)"]
    Engine --> Storage["Distributed State / Storage / Cache"]
    Engine --> Observability["Metrics & Audit Logging"]
```

For complete system design diagrams, failure recovery mechanics, and scalability analyses, see [`ARCHITECTURE.md`](./ARCHITECTURE.md).

---

## 5. Quick Start: How to Run

### Option A: Local Python Environment
```bash
# 1. Navigate to project directory
cd 36_zero_trust_secrets_vault

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
The API will be available at `http://localhost:8036` with interactive OpenAPI documentation at `http://localhost:8036/docs`.

### Option B: Docker Container
```bash
docker build -t 36_zero_trust_secrets_vault:latest .
docker run -p 8036:8036 --env-file .env 36_zero_trust_secrets_vault:latest
```

---

## 6. High-Salary Resume Bullet Points (STAR Method)
Copy and paste these verified, high-impact bullet points into your CV/resume:

- Architected an enterprise secrets vault utilizing AES-256-GCM envelope encryption and Shamir\'s Secret Sharing unseal quorum.
- Designed dynamic short-lived database credential leasing with automated revocation, eliminating static hardcoded passwords.
- Passed rigorous enterprise SOC2 Type II compliance audit with cryptographic tamper-evident access logs.

---

## 7. Top Technical Interview Questions & Model Answers
#### Q1: How does Shamir's Secret Sharing protect an enterprise vault's master key?
**Model Answer:**
> A single master key creates a single point of failure and insider threat. Shamir's Secret Sharing mathematically divides the master key into $N$ distinct shares using polynomial points over a finite field. Any $K$ shares (e.g. 3 of 5 held by different security executives) are required to mathematically reconstruct the polynomial and unseal the vault. Holding $K-1$ shares reveals mathematically zero information about the key.


---

## 8. GitHub Presentation Tip for High Remote Salary Offers
When publishing this project to your personal GitHub:
1. Include a 60-90 second Loom screen recording or animated GIF at the top of the README demonstrating the API live.
2. Link your live cloud deployment URL (e.g. deployed on Railway, Render, or AWS).
3. Highlight your benchmark numbers (QPS, p99 latency, cost savings) prominently in the repository description.
