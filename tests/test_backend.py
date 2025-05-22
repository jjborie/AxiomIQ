import pytest
from fastapi import HTTPException

from backend import main, config


@pytest.fixture(autouse=True)
def reset_state():
    from backend import database, models

    models.Base.metadata.drop_all(bind=database.engine)
    models.Base.metadata.create_all(bind=database.engine)
    main._evaluations.clear()
    main._evaluation_results.clear()
    yield
    models.Base.metadata.drop_all(bind=database.engine)
    models.Base.metadata.create_all(bind=database.engine)
    main._evaluations.clear()
    main._evaluation_results.clear()


def test_login_success():
    data = main.LoginRequest(username=config.DEFAULT_USERNAME, password=config.DEFAULT_PASSWORD)
    token = main.login(data)
    assert token.access_token == config.ACCESS_TOKEN
    assert token.token_type == "bearer"


def test_login_failure():
    data = main.LoginRequest(username="bad", password="creds")
    with pytest.raises(HTTPException) as exc:
        main.login(data)
    assert exc.value.status_code == 401


def test_question_lifecycle():
    qdata = main.QuestionCreate(text="Sample?", options=["yes", "no"], correct="yes", ku="Networking")
    question = main.create_question(qdata, token=config.ACCESS_TOKEN)
    assert question.id == 1

    questions = main.list_questions(token=config.ACCESS_TOKEN)
    assert len(questions) == 1
    assert questions[0].text == "Sample?"

    resp = main.delete_question(question.id, token=config.ACCESS_TOKEN)
    assert resp["status"] == "deleted"
    questions = main.list_questions(token=config.ACCESS_TOKEN)
    assert len(questions) == 0

    with pytest.raises(HTTPException) as exc:
        main.delete_question(999, token=config.ACCESS_TOKEN)
    assert exc.value.status_code == 404


def test_model_lifecycle():
    mdata = main.ModelCreate(name="m1", type="local")
    model = main.create_model(mdata, token=config.ACCESS_TOKEN)
    assert model.id == 1

    models = main.list_models(token=config.ACCESS_TOKEN)
    assert len(models) == 1
    assert models[0].name == "m1"

    resp = main.test_model(model.id, token=config.ACCESS_TOKEN)
    assert resp["status"] == "ok"

    with pytest.raises(HTTPException) as exc:
        main.test_model(999, token=config.ACCESS_TOKEN)
    assert exc.value.status_code == 404


def test_evaluation_flow():
    qdata = main.QuestionCreate(text="Q?", options=["A", "B"], correct="A", ku="Networking")
    main.create_question(qdata, token=config.ACCESS_TOKEN)
    mdata = main.ModelCreate(name="m1", type="local")
    main.create_model(mdata, token=config.ACCESS_TOKEN)

    data = main.EvaluationCreate(model_ids=[1], question_scope=["Networking"], question_count=1, mode="auto")
    evaluation = main.create_evaluation(data, token=config.ACCESS_TOKEN)
    assert evaluation.evaluation_id == "ev1"

    fetched = main.get_evaluation_status(evaluation.evaluation_id, token=config.ACCESS_TOKEN)
    assert fetched.evaluation_id == evaluation.evaluation_id

    results = main.get_evaluation_results(evaluation.evaluation_id, token=config.ACCESS_TOKEN)
    assert results.models[0]["id"] == 1
    assert len(results.questions) == 1


    with pytest.raises(HTTPException) as exc:
        main.get_evaluation_status("missing", token=config.ACCESS_TOKEN)
    assert exc.value.status_code == 404

    with pytest.raises(HTTPException) as exc:
        main.get_evaluation_results("missing", token=config.ACCESS_TOKEN)
    assert exc.value.status_code == 404


def test_list_kus():
    kus = main.list_kus(token=config.ACCESS_TOKEN)
    assert kus == main._kus
