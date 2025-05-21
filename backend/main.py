from datetime import datetime
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

from . import config

app = FastAPI(title="AxiomIQ Backend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class Question(BaseModel):
    id: int
    text: str
    options: List[str]
    correct: str
    ku: str


class QuestionCreate(BaseModel):
    text: str
    options: List[str]
    correct: str
    ku: str


class Model(BaseModel):
    id: int
    name: str
    type: str
    status: str
    api_key: Optional[str] = None
    model_name: Optional[str] = None


class ModelCreate(BaseModel):
    name: str
    type: str
    api_key: Optional[str] = None
    model_name: Optional[str] = None


class EvaluationCreate(BaseModel):
    model_ids: List[int] = Field(default_factory=list)
    question_scope: List[str] = Field(default_factory=list)
    question_count: int
    mode: str
    benchmark_id: Optional[int] = None


class Evaluation(BaseModel):
    evaluation_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None


class EvaluationResult(BaseModel):
    models: List[Dict]
    questions: List[Dict]


# ---------------------------------------------------------------------------
# In memory "database"
# ---------------------------------------------------------------------------
_questions: Dict[int, Question] = {}
_models: Dict[int, Model] = {}
_evaluations: Dict[str, Evaluation] = {}
_evaluation_results: Dict[str, EvaluationResult] = {}
_kus = ["Networking", "Cryptography", "Threat Analysis"]

_question_id = 1
_model_id = 1


# ---------------------------------------------------------------------------
# Utility / dependencies
# ---------------------------------------------------------------------------

def require_token(token: str = Depends(oauth2_scheme)):
    if token != config.ACCESS_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# ---------------------------------------------------------------------------
# Basic routes
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "AxiomIQ backend"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
@app.post("/api/login", response_model=Token)
def login(data: LoginRequest):
    if not config.verify_credentials(data.username, data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    return Token(access_token=config.ACCESS_TOKEN)


# ---------------------------------------------------------------------------
# Questions endpoints
# ---------------------------------------------------------------------------
@app.get("/api/questions", response_model=List[Question])
def list_questions(ku: Optional[str] = None, limit: int = 100, token: str = Depends(require_token)):
    questions = list(_questions.values())
    if ku:
        questions = [q for q in questions if q.ku == ku]
    return questions[:limit]


@app.post("/api/questions", response_model=Question)
def create_question(data: QuestionCreate, token: str = Depends(require_token)):
    global _question_id
    question = Question(id=_question_id, **data.dict())
    _questions[_question_id] = question
    _question_id += 1
    return question


@app.delete("/api/questions/{question_id}")
def delete_question(question_id: int, token: str = Depends(require_token)):
    if question_id not in _questions:
        raise HTTPException(status_code=404, detail="Question not found")
    del _questions[question_id]
    return {"status": "deleted"}


# ---------------------------------------------------------------------------
# Models endpoints
# ---------------------------------------------------------------------------
@app.get("/api/models", response_model=List[Model])
def list_models(token: str = Depends(require_token)):
    return list(_models.values())


@app.post("/api/models", response_model=Model)
def create_model(data: ModelCreate, token: str = Depends(require_token)):
    global _model_id
    model = Model(id=_model_id, status="active", **data.dict())
    _models[_model_id] = model
    _model_id += 1
    return model


@app.post("/api/models/{model_id}/test")
def test_model(model_id: int, token: str = Depends(require_token)):
    if model_id not in _models:
        raise HTTPException(status_code=404, detail="Model not found")
    # Dummy success response
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Evaluation endpoints
# ---------------------------------------------------------------------------
@app.post("/api/evaluations", response_model=Evaluation)
def create_evaluation(data: EvaluationCreate, token: str = Depends(require_token)):
    eval_id = f"ev{len(_evaluations)+1}"
    evaluation = Evaluation(
        evaluation_id=eval_id,
        status="started",
        start_time=datetime.utcnow(),
    )
    _evaluations[eval_id] = evaluation
    # Dummy evaluation result placeholder
    _evaluation_results[eval_id] = EvaluationResult(models=[], questions=[])
    return evaluation


@app.get("/api/evaluations/{evaluation_id}", response_model=Evaluation)
def get_evaluation(evaluation_id: str, token: str = Depends(require_token)):
    if evaluation_id not in _evaluations:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return _evaluations[evaluation_id]


@app.get("/api/evaluations/{evaluation_id}/results", response_model=EvaluationResult)
def get_evaluation_results(evaluation_id: str, token: str = Depends(require_token)):
    if evaluation_id not in _evaluation_results:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return _evaluation_results[evaluation_id]


# ---------------------------------------------------------------------------
# Misc endpoints
# ---------------------------------------------------------------------------
@app.get("/api/kus", response_model=List[str])
def list_kus(token: str = Depends(require_token)):
    return _kus


