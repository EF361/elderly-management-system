# Elderly Management System ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-%2303244d) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%23336791) ![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen) ![Demo](https://img.shields.io/badge/Demo-Live--Preview-purple)

## Executive Summary
The **Elderly Management System** is a secure and scalable platform designed to manage elderly care operations, such as resident records, healthcare planning, and real-time notifications. The solution prioritizes data security, compliance, and usability, leveraging AI-driven recommendations (via the OpenAI API) to enhance caregiving outcomes.

---

## Key Features
- **Role-Based Access Control (RBAC):** Enforces strict user permissions for sensitive operations server-side, validated through integration tests.
- **AI-Assisted Recommendations:** Safely integrates with OpenAI API to provide non-clinical healthcare recommendations with human oversight and auditability.
- **Secure Data Handling:** Supports AES-256 encryption, sensitive logging policies, and full auditability with documented retention and backup strategies.
- **Streamlined Frontend:** Intuitive, responsive user interface built with Streamlit for real-time caregiving updates.
- **Compliance-Ready Architecture:** Designed with compliance in mind, featuring secret management, session security, and network isolation.
- **Dockerized Infrastructure:** Fully containerized deployment with Docker Compose, database schema migrations, and sanitized seed data for local reproducibility.
- **Extensive Testing:** Authorization and integration tests ensure robust controls for sensitive data access.

---

## Architecture & Workflow
```mermaid
graph TD
    A[Frontend (Streamlit)] -->|Requests| B[API Layer (Flask)]
    B -->|Secure Queries| C[PostgreSQL Database]
    B -->|Fetch Recommendations| D[OpenAI API]
    C -->|Trigger Events| E[Notification System]
    D -->|Validated Response| B
    E --> B
    
    classDef secure fill:#f9f,stroke:#333,stroke-width:4px;
    B, C, E class secure
```
**Explanation of Workflow**: 
1. User interacts with the Streamlit-based frontend. 
2. API Layer handles input validation, access control, and secure calls to the database and OpenAI API.
3. PostgreSQL stores encrypted sensitive data and triggers actionable notifications.
4. AI-assisted recommendations are treated as non-clinical suggestions and undergo human review.
5. Notifications and reports are securely propagated to caregivers in real time.

---

## Tech Stack & Tools Breakdown
**Languages & Frameworks**
- **Python 3.10**: Core language for both backend and AI integrations.
- **Streamlit**: Frontend development framework for rapid UI prototyping.
- **Flask**: API development and middleware for RBAC and encryption.

**Data Storage & Security**
- **PostgreSQL**: Primary relational database with schema migrations support.
- **AES-256 Encryption**: Used for securing sensitive data, including healthcare records.

**Integrations**
- **OpenAI API**: Delivers AI-enhanced care suggestions, logged for provenance and validation.

**Infrastructure**
- **Docker Compose**: Standardized local and production environments.
- **Nginx**: Reverse proxy for secure API routing and network isolation.

---

## Quickstart / Installation
Follow these steps to deploy the Elderly Management System locally:

### Prerequisites
- Install **Docker** and **Docker Compose**.
- Ensure Python 3.10+ and PostgreSQL are set up (if not using Docker).

### Steps
```bash
# 1. Clone the Repository
git clone https://github.com/EF361/elderly-management-system.git
cd elderly-management-system

# 2. Set Environment Variables
cp .env.example .env
# Update .env with PostgreSQL credentials, OpenAI API key, and other secrets.

# 3. Build and Start Services
docker-compose up --build

# 4. Apply Database Migrations
docker exec -it elderly_management_backend bash -c "flask db upgrade"

# 5. Seed Database with Sanitized Test Data
docker exec -it elderly_management_backend bash -c "python scripts/seed_data.py"

# 6. Access the Application
# Open http://localhost:8501 in your browser to access the frontend.

```

---

## Security & Compliance Highlights
- **RBAC Enforcement**: Ensures sensitive operations like resident updates adhere to role-based permissions.
- **Audit Logging**: All sensitive operations are logged with identifiers for traceability.
- **Data Retention & Backup**: Backup jobs configured via Docker volumes; compliant with GDPR-like retention rules.
- **Encryption and Secret Management**: All sensitive fields are encrypted at rest (AES-256), and runtime secrets are injected via environment variables.
- **Threat Model**: Verifies controls for injection attacks, session hijacking, and unauthorized data access.

Links to Evidence & Documentation:
- **RBAC Tests**: [tests/rbac.test.py](tests/rbac.test.py)
- **Schema & Database Migrations**: [migrations/](migrations/)
- **Backup Strategy**: [docs/backup.md](docs/backup.md)
- **Audit Logging**: [docs/audit-log-policy.md](docs/audit-log-policy.md)

---

## Developer Notes
This repository was built and architected by **Alicia Goh (EF361)**, leveraging her expertise in AI-enhanced software engineering for operationally sensitive environments. Alicia's focus on compliance-grade solutions, hardened security, and developer-friendly ergonomics positions this system for scalable growth in both healthcare and eldercare industries.

---

## License
The project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.