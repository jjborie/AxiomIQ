"""Agent implementations for EvalForge.

This module defines simple agent classes used to orchestrate model evaluation
and related tasks.  The goal is to mirror the architecture described in
``docs/AGENT_ARCHITECTURE.md`` while keeping the implementation lightweight for
this demo project.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


@dataclass
class ModelAgent:
    """Wrapper around an AI model.

    Parameters
    ----------
    model_id: int
        Unique identifier for the model.
    name: str
        Human friendly name.
    max_retries: int
        Number of attempts for the ``ask`` call.
    response_format: str
        Expected answer format ("letter", etc.).
    """

    model_id: int
    name: str
    max_retries: int = 2
    response_format: str = "letter"

    def ask(self, question: str, options: Iterable[str]) -> str:
        """Return an answer to ``question``.

        The demo implementation simply selects the first option.  In a real
        system this would call an external model API.
        """

        # The simplistic policy used for testing.
        return next(iter(options))


@dataclass
class EvaluationAgent:
    """Orchestrates the evaluation process across models."""

    models: List[ModelAgent]
    timeout: int = 30
    mode: str = "peer"

    def evaluate(self, questions: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        """Run an evaluation over ``questions`` using the configured models."""

        model_stats: Dict[int, Dict[str, Any]] = {
            m.model_id: {"correct": 0, "total": 0, "name": m.name}
            for m in self.models
        }
        question_results: List[Dict[str, Any]] = []

        for q in questions:
            q_res = {"id": q["id"], "answers": {}, "correct": q["correct"]}
            for m in self.models:
                answer = m.ask(q["text"], q["options"])
                q_res["answers"][m.model_id] = answer
                model_stats[m.model_id]["total"] += 1
                if answer == q["correct"]:
                    model_stats[m.model_id]["correct"] += 1
            question_results.append(q_res)

        model_results = []
        for mid, stats in model_stats.items():
            total = stats["total"] or 1
            accuracy = stats["correct"] / total
            model_results.append(
                {
                    "id": mid,
                    "name": stats["name"],
                    "correct": stats["correct"],
                    "total": total,
                    "accuracy": accuracy,
                }
            )

        return {"models": model_results, "questions": question_results}


@dataclass
class QuestionCurationAgent:
    """Provides basic question review utilities."""

    def review(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """Return a trivial review result."""
        return {"id": question.get("id"), "status": "ok"}


@dataclass
class AnalyticsAgent:
    """Performs simple analytics on evaluation results."""

    enable_anova: bool = True
    export_format: str = "csv"

    def summary(self, evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
        models = evaluation_result.get("models", [])
        average_accuracy = (
            sum(m["accuracy"] for m in models) / len(models) if models else 0
        )
        return {"model_count": len(models), "average_accuracy": average_accuracy}


@dataclass
class BenchmarkAgent:
    """Runs external benchmarks for a model."""

    def run(self, model: ModelAgent) -> Dict[str, Any]:
        # Placeholder benchmark run producing a random score
        return {"model_id": model.model_id, "benchmark_score": random.random()}


__all__ = [
    "ModelAgent",
    "EvaluationAgent",
    "QuestionCurationAgent",
    "AnalyticsAgent",
    "BenchmarkAgent",
]
