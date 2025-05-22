from backend.agents import (
    ModelAgent,
    EvaluationAgent,
    QuestionCurationAgent,
    AnalyticsAgent,
    BenchmarkAgent,
)


def test_model_agent_answer():
    agent = ModelAgent(model_id=1, name="m1")
    answer = agent.ask("Q?", ["A", "B"])
    assert answer == "A"


def test_evaluation_agent():
    m = ModelAgent(model_id=1, name="m1")
    q = {"id": 1, "text": "Q?", "options": ["A", "B"], "correct": "A"}
    eval_agent = EvaluationAgent([m])
    result = eval_agent.evaluate([q])
    assert result["models"][0]["correct"] == 1
    assert result["questions"][0]["answers"][1] == "A"


def test_question_curation_agent():
    agent = QuestionCurationAgent()
    review = agent.review({"id": 1, "text": "Q"})
    assert review["status"] == "ok"


def test_analytics_agent_summary():
    analytics = AnalyticsAgent()
    summary = analytics.summary({
        "models": [{"accuracy": 1.0}, {"accuracy": 0.5}]
    })
    assert summary["model_count"] == 2
    assert summary["average_accuracy"] == 0.75


def test_benchmark_agent():
    benchmark = BenchmarkAgent()
    m = ModelAgent(model_id=1, name="m1")
    result = benchmark.run(m)
    assert result["model_id"] == 1
