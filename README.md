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
