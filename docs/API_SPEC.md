# API_SPEC.md

## EvalForge API Specification

This document outlines the RESTful API endpoints used by EvalForge to manage evaluations, questions, models, and users.

---

## 🛡️ Authentication

### `POST /api/login`
Authenticate a user and return a JWT token.

**Request Body:**
```json
{
  "username": "admin",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

---

## 📋 Evaluations

### `POST /api/evaluations`
Start a new evaluation run between models using selected question criteria.

**Request Body:**
```json
{
  "model_ids": [1, 2],
  "question_scope": ["Networking", "Cryptography"],
  "question_count": 50,
  "mode": "peer",  // or "parallel"
  "benchmark_id": null
}
```

**Response:**
```json
{
  "evaluation_id": "abc123",
  "status": "started"
}
```

---

### `GET /api/evaluations/{id}`
Retrieve metadata and status for an evaluation.

**Response:**
```json
{
  "evaluation_id": "abc123",
  "status": "completed",
  "start_time": "2025-05-21T12:00:00Z",
  "end_time": "2025-05-21T12:10:00Z"
}
```

---

### `GET /api/evaluations/{id}/results`
Get results and metrics from a completed evaluation.

**Response:**
```json
{
  "models": [
    {
      "id": 1,
      "name": "GPT-4",
      "accuracy": 0.92,
      "scores_by_ku": {
        "Networking": 0.85,
        "Cryptography": 1.0
      }
    }
  ],
  "questions": [
    {
      "id": 10,
      "text": "Which protocol operates at Layer 4?",
      "correct": "TCP",
      "answers": [
        { "model_id": 1, "answer": "TCP", "correct": true }
      ]
    }
  ]
}
```

---

## ❓ Questions

### `GET /api/questions`
Retrieve a list of questions with optional filtering.

**Query Parameters:**
- `ku=Networking`
- `limit=25`

**Response:**
```json
[
  {
    "id": 101,
    "text": "What does the OSI model stand for?",
    "options": ["A", "B", "C", "D"],
    "correct": "A",
    "ku": "Networking"
  }
]
```

---

### `POST /api/questions`
Add a new MCQ to the bank.

**Request Body:**
```json
{
  "text": "What is SSL?",
  "options": ["Secure Socket Layer", "Super Server Link", "System Secure Layer", "Server Socket Layer"],
  "correct": "Secure Socket Layer",
  "ku": "Cryptography"
}
```

---

### `DELETE /api/questions/{id}`
Remove a question from the database.

---

## 🧠 Models

### `GET /api/models`
Retrieve list of configured AI models.

**Response:**
```json
[
  { "id": 1, "name": "GPT-4", "type": "OpenAI", "status": "active" }
]
```

---

### `POST /api/models`
Register a new model.

**Request Body:**
```json
{
  "name": "GPT-4",
  "type": "OpenAI",
  "api_key": "sk-abc123",
  "model_name": "gpt-4"
}
```

---

### `POST /api/models/{id}/test`
Test a model’s connectivity and readiness.

---

## ⚙️ Settings and Metadata

### `GET /api/kus`
Return list of Knowledge Units (KUs) for question tagging.

**Response:**
```json
[
  "Networking",
  "Cryptography",
  "Threat Analysis"
]
```

---

## 🔒 Security

- All endpoints require bearer token authentication unless noted.
- Use HTTPS for all traffic.
- Rate limits and error codes follow standard REST conventions.

---

© EvalForge Project — 2025. All rights reserved.
