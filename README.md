# AxiomIQ

This repository provides a minimal demonstration of a backend API and a small
HTML frontend.  The API is implemented with FastAPI and stores data in memory.

## Endpoints

* `POST /auth/login` – obtain an access token
* `POST /questions` – create a question
* `POST /models` – create a model
* `GET /models` – list models
* `POST /evaluations` – start an evaluation
* `GET /evaluations/{id}` – fetch evaluation results
* `GET /evaluations/{id}/status` – fetch evaluation status

The frontend (`frontend/index.html`) contains a few basic forms that exercise
these endpoints using JavaScript `fetch` calls.

## Running with Docker Compose

```bash
docker-compose -f docker/docker-compose.yml up --build
```

This builds and starts the backend on port `8000` and the frontend on port `3000`.

## Running on Kubernetes

1. **Build the container images**

   ```bash
   docker build -t axiomiq-backend:latest -f docker/Dockerfile.api .
   docker build -t axiomiq-frontend:latest -f docker/Dockerfile.ui .
   ```

   If using Minikube or kind, load the images into your cluster:

   ```bash
   minikube image load axiomiq-backend:latest
   minikube image load axiomiq-frontend:latest
   # or for kind:
   # kind load docker-image axiomiq-backend:latest
   # kind load docker-image axiomiq-frontend:latest
   ```

2. **Deploy the manifests**

   ```bash
   kubectl apply -f k8s/
   ```

3. **Access the services**

   The services expose `NodePort`s so you can reach them at the address of any
   cluster node:

   * Backend – port **30080**
   * Frontend – port **30081**

   If your environment does not allow NodePorts you can still port-forward:

   ```bash
   kubectl port-forward svc/backend 8000:8000
   kubectl port-forward svc/frontend 3000:80
   ```

   With either method, open `http://localhost:3000` in your browser and the API
   is reachable on `http://localhost:8000`.
