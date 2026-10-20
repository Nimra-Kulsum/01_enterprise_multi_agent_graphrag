# Project 40: Automated Certificate Authority & ACME Protocol Engine

> **Category:** Cyber Security & Identity  
> **Target Job Roles:** `PKI Systems Engineer, Cryptographic Security Architect, Infrastructure Security Lead`  
> **Target Remote Salary / Rate:** `$170,000 - $260,000 / yr (Remote) or $85 - $150 / hr`  
> **Production Tech Stack:** `Python 3.12, FastAPI, Cryptography library, Pydantic, Docker`

---

## 1. What It Is
An automated public-key infrastructure (PKI) and X.509 certificate authority engine implementing the ACME protocol (RFC 8555 - the protocol powering Let\'s Encrypt). 

Automates the entire TLS certificate lifecycle: processing Certificate Signing Requests (CSRs), issuing DNS-01 and HTTP-01 cryptographic domain validation challenges, verifying proof of domain ownership, issuing signed X.509 certificates using intermediate CA private keys, and publishing Certificate Revocation Lists (CRL) and OCSP endpoints.

---

## 2. Where It Is Used (Enterprise Real-World Context)
- **Internal Enterprise PKI (HashiCorp Vault, Smallstep, Let\'s Encrypt)**: Automating internal mTLS certificates across thousands of microservices and internal domains.
- **CDN Edge Terminators (Cloudflare, Fastly)**: Managing millions of automated customer SSL/TLS certificates.

---

## 3. Required IT Knowledge & Technical Fundamentals
1. **ACME Protocol (RFC 8555)**: Automated DNS-01 and HTTP-01 challenge verification workflows.
2. **X.509 Cryptography**: RSA/ECDSA key pairs, Certificate Signing Requests (CSRs), Subject Alternative Names (SANs).
3. **Certificate Revocation & OCSP**: Online Certificate Status Protocol stapling and CRL distribution.

---

## 4. High-Level Architecture & Data Flow

```mermaid
flowchart TD
    Client["Client / Upstream Gateway"] --> Ingress["API Ingress & Security Layer"]
    Ingress --> Engine["Core Processing Engine (40_decentralized_pki_acme_ca)"]
    Engine --> Storage["Distributed State / Storage / Cache"]
    Engine --> Observability["Metrics & Audit Logging"]
```

For complete system design diagrams, failure recovery mechanics, and scalability analyses, see [`ARCHITECTURE.md`](./ARCHITECTURE.md).

---

## 5. Quick Start: How to Run

### Option A: Local Python Environment
```bash
# 1. Navigate to project directory
cd 40_decentralized_pki_acme_ca

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
The API will be available at `http://localhost:8040` with interactive OpenAPI documentation at `http://localhost:8040/docs`.

### Option B: Docker Container
```bash
docker build -t 40_decentralized_pki_acme_ca:latest .
docker run -p 8040:8040 --env-file .env 40_decentralized_pki_acme_ca:latest
```

---

## 6. High-Salary Resume Bullet Points (STAR Method)
Copy and paste these verified, high-impact bullet points into your CV/resume:

- Architected an automated ACME protocol CA issuing 50,000+ short-lived internal X.509 mTLS certificates annually.
- Implemented automated DNS-01 challenge verification, enabling wildcard TLS issuance with zero manual intervention.
- Designed a high-availability OCSP responder delivering sub-5ms certificate revocation verification.

---

## 7. Top Technical Interview Questions & Model Answers
#### Q1: What is the difference between an HTTP-01 challenge and a DNS-01 challenge in the ACME protocol?
**Model Answer:**
> An HTTP-01 challenge requires the server requesting the certificate to host a specific token at `http://<domain>/.well-known/acme-challenge/<token>`, proving control of the web server on port 80. A DNS-01 challenge requires provisioning a `_acme-challenge.<domain>` TXT record in the domain's DNS zone, which is mandatory for issuing wildcard certificates (`*.example.com`) and works without exposing internal servers to the public web.


---

## 8. GitHub Presentation Tip for High Remote Salary Offers
When publishing this project to your personal GitHub:
1. Include a 60-90 second Loom screen recording or animated GIF at the top of the README demonstrating the API live.
2. Link your live cloud deployment URL (e.g. deployed on Railway, Render, or AWS).
3. Highlight your benchmark numbers (QPS, p99 latency, cost savings) prominently in the repository description.
