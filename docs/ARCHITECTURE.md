# ARCHITECTURE.md

## EvalForge System Architecture

EvalForge is a modular, containerized platform designed to evaluate the domain knowledge proficiency of Generative AI models using structured multiple-choice questions (MCQs). The architecture is built for scalability, extensibility, and secure internal use.

---

## 1. High-Level Overview

```
+------------------+       +------------------+       +------------------+
|   React Frontend | <---> | FastAPI Backend  | <---> | PostgreSQL DB    |
+------------------+       +------------------+       +------------------+
                                 |
                                 v
                        +------------------+
                        | Model Adapters   |
                        | (OpenAI, HF, etc)|
                        +------------------+
                                 |
                                 v
                      +----------------------+
                      | External/Local Models|
                      +----------------------+
```

---

## 2. Core Components

### 🧠 Frontend (React)
- UI for model management, evaluations, question bank, and analytics
- Built with React + Material-UI
- Uses Axios/React Query to communicate with backend
- Protected via JWT session/token-based auth

### ⚙️ Backend (FastAPI)
- FastAPI serves as the orchestrator for:
  - Model Evaluation Engine
  - Question Bank Service
  - Benchmark Comparison Engine
- Asynchronous architecture using `asyncio` and `httpx`
- Celery + Redis for task queuing of long-running evaluations

### 🗃️ Database (PostgreSQL)
- Stores questions, evaluations, user credentials, models, and results
- Schema includes:
  - `models`, `questions`, `evaluations`, `answers`, `users`
- Indexed by KU and domain for efficient question retrieval

### 🔌 Model Integration Layer
- Adapters for different LLMs (e.g., OpenAI, HuggingFace, Local Inference APIs)
- Abstracts API formats to a common `ask(question, options)` interface
- Includes retry and error handling logic
- Optional response time tracking

---

## 3. Evaluation Workflow

1. Admin configures models and selects MCQ criteria
2. Backend orchestrator:
   - Selects question set from DB
   - Distributes MCQs across models
   - Sends API requests and receives responses
   - Compares responses to answer key
   - Stores and scores results
3. Frontend polls and visualizes results

---

## 4. Deployment Stack

- **Containerization**: Docker (per service)
- **Orchestration**: Kubernetes (multi-instance, auto-scale)
- **CI/CD**: GitHub Actions
- **Environment Config**: `.env` files or Vault secrets
- **Monitoring**: Prometheus + Grafana (optional)
- **Logging**: ELK stack or lightweight JSON logs

---

## 5. Security

- JWT-based user authentication
- HTTPS enforced with TLS
- Secrets stored encrypted or managed externally
- Minimal permissions for API access
- Audit trail logging on all sensitive actions

---

## 6. Extensibility

- Add new LLMs via plug-and-play adapter
- Add new domain MCQs via CSV or API
- Future-proofed for evaluation of:
  - Code generation models
  - Long-form QA models
  - Domain-specific benchmarks

---

## 7. Planned Enhancements

- WebSocket live updates during evaluation
- Role-based access controls (RBAC)
- User feedback on question quality
- GraphQL support for analytics API

---

© EvalForge Project — 2025. All rights reserved.
