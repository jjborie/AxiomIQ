# AGENT_ARCHITECTURE.md

## EvalForge Agent Architecture

EvalForge supports the use of AI agents to automate and orchestrate core functions in the system, particularly for model evaluation, question curation, and scoring analytics. This document outlines agent roles, behaviors, and interaction protocols.

---

## 🧠 Agent Types

### 1. **EvaluationAgent**
- **Purpose:** Orchestrates the evaluation process between models.
- **Responsibilities:**
  - Selects MCQs based on KU/topic criteria.
  - Assigns question sets to each model.
  - Calls ModelInterface to query each model.
  - Scores responses and stores results.

### 2. **ModelAgent**
- **Purpose:** Wrapper for individual AI models (e.g., GPT-4, Claude).
- **Responsibilities:**
  - Accepts question prompts.
  - Returns the selected answer.
  - Applies parsing logic to standardize format.
  - Supports retry and timeout logic.

### 3. **QuestionCurationAgent**
- **Purpose:** Assists in evaluating and improving question bank quality.
- **Responsibilities:**
  - Reviews existing questions for clarity and alignment.
  - Suggests edits or flags ambiguous items.
  - Optionally generates new MCQs for target KUs.

### 4. **AnalyticsAgent**
- **Purpose:** Conducts post-evaluation statistical and qualitative analysis.
- **Responsibilities:**
  - Aggregates performance metrics by KU, model, and difficulty.
  - Runs ANOVA and correlation analyses.
  - Generates summary reports and visualizations.

### 5. **BenchmarkAgent**
- **Purpose:** Runs AI models through external benchmark datasets.
- **Responsibilities:**
  - Executes benchmark tasks (e.g., CyberSecEval 2).
  - Normalizes scoring across benchmarks.
  - Compares benchmark results with EvalForge metrics.

---

## 🤖 Agent Interaction Flow

```
EvaluationAgent
   └─▶ ModelAgent(s)
         └─▶ AI Model
   └─▶ QuestionCurationAgent
   └─▶ AnalyticsAgent
   └─▶ BenchmarkAgent
```

- Agents communicate via internal API calls or task queues (Celery).
- Each agent operates autonomously within assigned task boundaries.

---

## ⚙️ Configuration

Agents are configured in `agents/config.yaml`:

```yaml
agents:
  evaluation:
    timeout: 30
    mode: peer
  model:
    max_retries: 2
    response_format: "letter"
  analytics:
    enable_anova: true
    export_format: "csv"
```

---

## 🔐 Security Considerations

- Agents are sandboxed and only access assigned services.
- ModelAgent enforces output filtering to sanitize unexpected responses.
- All agent actions are logged with trace IDs.

---

## 🧪 Testing Agents

Unit and integration tests exist under `tests/agents/`. Run with:

```bash
pytest tests/agents/
```

---

## 🧭 Future Agents

- **FeedbackAgent**: Gathers user feedback on questions and answers.
- **AdaptiveAgent**: Modifies question difficulty based on past performance.
- **TrainingAgent**: Fine-tunes models using evaluation outcomes.

---

