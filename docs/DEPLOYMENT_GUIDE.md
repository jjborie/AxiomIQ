# DEPLOYMENT_GUIDE.md

## EvalForge Deployment Guide

This guide walks you through deploying the EvalForge AI model evaluation platform using Docker and Kubernetes.

---

## 🧰 Requirements

- Docker (v20+)
- Docker Compose (v2+)
- Kubernetes (minikube or cloud cluster)
- kubectl CLI
- Python 3.9+
- Node.js v18+ and npm
- GitHub (for CI/CD)

---

## 🗂️ Repository Structure

```
evalforge/
├── backend/             # FastAPI application
├── frontend/            # React SPA
├── model_adapters/      # AI model interfaces
├── database/            # Migrations and seed data
├── docker/              # Dockerfiles and compose setup
├── k8s/                 # Kubernetes manifests
└── .env                 # Environment variables
```

---

## 🔧 Environment Configuration

Create a `.env` file at the project root:

```bash
POSTGRES_DB=evalforge
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
SECRET_KEY=your-super-secret-key
OPENAI_API_KEY=sk-abc123
```

---

## 🐳 Local Docker Deployment

1. **Build and start containers:**

```bash
docker-compose up --build
```

2. **Access services:**

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/docs`
- Postgres DB: `localhost:5432`

---

## ☸️ Kubernetes Deployment (Optional)

1. **Configure Secrets:**

```bash
kubectl create secret generic evalforge-secrets \
  --from-literal=POSTGRES_PASSWORD=secret \
  --from-literal=SECRET_KEY=your-super-secret-key \
  --from-literal=OPENAI_API_KEY=sk-abc123
```

2. **Deploy resources:**

```bash
kubectl apply -f k8s/
```

3. **Verify:**

```bash
kubectl get pods
kubectl get svc
```

4. **Port Forward (for local testing):**

```bash
kubectl port-forward svc/frontend 3000:80
kubectl port-forward svc/backend 8000:8000
```

---

## 🔁 Database Initialization

If using Docker Compose, the DB will auto-init. For Kubernetes:

```bash
kubectl exec -it <backend-pod> -- bash
alembic upgrade head  # or equivalent migration tool
```

---

## 🚀 CI/CD with GitHub Actions

Sample `.github/workflows/deploy.yml`:

```yaml
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker images
        run: docker build -t evalforge-backend ./backend
```

---

## 🔒 Security Checklist

- Use HTTPS (reverse proxy or ingress controller)
- Rotate secrets regularly
- Restrict access to model APIs
- Enable audit logging

---

## 📦 Scaling & Monitoring

- Use Kubernetes Horizontal Pod Autoscaler (HPA)
- Integrate Prometheus + Grafana for metrics
- Use centralized logging (e.g. Loki, ELK)

---

## 📬 Support

For questions, please open an issue or contact the maintainers.

---

© EvalForge Project — 2025. All rights reserved.
