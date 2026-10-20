# Project 39: Cloud Security Posture Management (CSPM) & Compliance Engine

> **Category:** Cyber Security & Identity  
> **Target Job Roles:** `Cloud Security Architect, DevSecOps Lead, Security Compliance Engineer`  
> **Target Remote Salary / Rate:** `$165,000 - $250,000 / yr (Remote) or $85 - $145 / hr`  
> **Production Tech Stack:** `Python 3.12, FastAPI, Pydantic, Compliance rule engines, Docker`

---

## 1. What It Is
An automated Cloud Security Posture Management (CSPM) and infrastructure compliance auditing engine (modeled after Wiz, Prisma Cloud, and ScoutSuite). 

Scans live cloud environments (AWS, GCP, Azure) and Terraform manifests against CIS Benchmarks, SOC2, and ISO 27001 standards. Flags critical security misconfigurations: publicly accessible S3 buckets, unrestricted SSH/RDP security groups (`0.0.0.0/0` on port 22/3389), root account API keys lacking MFA, and unencrypted database snapshots.

---

## 2. Where It Is Used (Enterprise Real-World Context)
- **Enterprise Security Teams (Wiz, Palo Alto Networks, Datadog)**: Automated continuous security audits across thousands of corporate cloud accounts.
- **FinTech & HealthTech Startups**: Achieving rapid SOC2 Type II and HIPAA certification readiness.

---

## 3. Required IT Knowledge & Technical Fundamentals
1. **CIS Cloud Benchmarks**: Standardized security configuration baselines for AWS, Azure, and Kubernetes.
2. **Graph-Based Attack Path Analysis**: Calculating whether a minor misconfiguration can chain into full account takeover.
3. **Software Bill of Materials (SBOM) & Vulnerability Scanning**: Inspecting container base images for known CVEs.

---

## 4. High-Level Architecture & Data Flow

```mermaid
flowchart TD
    Client["Client / Upstream Gateway"] --> Ingress["API Ingress & Security Layer"]
    Ingress --> Engine["Core Processing Engine (39_cloud_security_posture_scanner)"]
    Engine --> Storage["Distributed State / Storage / Cache"]
    Engine --> Observability["Metrics & Audit Logging"]
```

For complete system design diagrams, failure recovery mechanics, and scalability analyses, see [`ARCHITECTURE.md`](./ARCHITECTURE.md).

---

## 5. Quick Start: How to Run

### Option A: Local Python Environment
```bash
# 1. Navigate to project directory
cd 39_cloud_security_posture_scanner

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
The API will be available at `http://localhost:8039` with interactive OpenAPI documentation at `http://localhost:8039/docs`.

### Option B: Docker Container
```bash
docker build -t 39_cloud_security_posture_scanner:latest .
docker run -p 8039:8039 --env-file .env 39_cloud_security_posture_scanner:latest
```

---

## 6. High-Salary Resume Bullet Points (STAR Method)
Copy and paste these verified, high-impact bullet points into your CV/resume:

- Architected an automated CSPM engine scanning 45 AWS cloud accounts daily against 120+ CIS security benchmarks.
- Eliminated 100% of high-severity cloud exposure risks including public S3 buckets and open SSH security groups.
- Built automated Slack security alerting and remediation webhooks, cutting Mean Time to Remediate (MTTR) from 4 days to 15 minutes.

---

## 7. Top Technical Interview Questions & Model Answers
#### Q1: What is Graph-Based Attack Path Analysis in Cloud Security Posture Management (CSPM)?
**Model Answer:**
> Traditional vulnerability scanners look at security issues in isolation (e.g. an unpatched EC2 instance, or an IAM role with S3 write permissions). Graph-Based Attack Path Analysis connects the dots into an attack graph: an internet-facing EC2 instance has an IAM role that allows reading an S3 bucket containing customer credentials. This reveals that an external attacker can breach the entire company.


---

## 8. GitHub Presentation Tip for High Remote Salary Offers
When publishing this project to your personal GitHub:
1. Include a 60-90 second Loom screen recording or animated GIF at the top of the README demonstrating the API live.
2. Link your live cloud deployment URL (e.g. deployed on Railway, Render, or AWS).
3. Highlight your benchmark numbers (QPS, p99 latency, cost savings) prominently in the repository description.
