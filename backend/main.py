from datetime import datetime
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

from . import config
from .database import SessionLocal, engine
from . import models as db_models

db_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="AxiomIQ Backend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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
# In memory "database" for evaluations only
# ---------------------------------------------------------------------------
_evaluations: Dict[str, Evaluation] = {}
_evaluation_results: Dict[str, EvaluationResult] = {}
_kus = ["Networking", "Cryptography", "Threat Analysis"]


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
@app.post("/auth/login", response_model=Token)
def login(data: LoginRequest):
    if not config.verify_credentials(data.username, data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    return Token(access_token=config.ACCESS_TOKEN)


# ---------------------------------------------------------------------------
# Questions endpoints
# ---------------------------------------------------------------------------
@app.get("/questions", response_model=List[Question])
def list_questions(
    ku: Optional[str] = None,
    limit: int = 100,
    token: str = Depends(require_token),
    db: SessionLocal = Depends(get_db),
):
    query = db.query(db_models.Question)
    if ku:
        query = query.filter(db_models.Question.ku == ku)
    records = query.limit(limit).all()
    return [Question(id=q.id, text=q.text, options=q.options, correct=q.correct, ku=q.ku) for q in records]


@app.post("/questions", response_model=Question)
def create_question(
    data: QuestionCreate,
    token: str = Depends(require_token),
    db: SessionLocal = Depends(get_db),
):
    record = db_models.Question(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return Question(id=record.id, text=record.text, options=record.options, correct=record.correct, ku=record.ku)


@app.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    token: str = Depends(require_token),
    db: SessionLocal = Depends(get_db),
):
    record = db.query(db_models.Question).get(question_id)
    if not record:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(record)
    db.commit()
    return {"status": "deleted"}


# ---------------------------------------------------------------------------
# Models endpoints
# ---------------------------------------------------------------------------
@app.get("/models", response_model=List[Model])
def list_models(token: str = Depends(require_token), db: SessionLocal = Depends(get_db)):
    records = db.query(db_models.Model).all()
    return [Model(id=m.id, name=m.name, type=m.type, status=m.status, api_key=m.api_key, model_name=m.model_name) for m in records]


@app.post("/models", response_model=Model)
def create_model(
    data: ModelCreate,
    token: str = Depends(require_token),
    db: SessionLocal = Depends(get_db),
):
    record = db_models.Model(status="active", **data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return Model(id=record.id, name=record.name, type=record.type, status=record.status, api_key=record.api_key, model_name=record.model_name)


@app.post("/models/{model_id}/test")
def test_model(
    model_id: int,
    token: str = Depends(require_token),
    db: SessionLocal = Depends(get_db),
):
    record = db.query(db_models.Model).get(model_id)
    if not record:
        raise HTTPException(status_code=404, detail="Model not found")
    # Dummy success response
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Evaluation endpoints
# ---------------------------------------------------------------------------
@app.post("/evaluations", response_model=Evaluation)
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


@app.get("/evaluations/{evaluation_id}/status", response_model=Evaluation)
def get_evaluation_status(evaluation_id: str, token: str = Depends(require_token)):
    if evaluation_id not in _evaluations:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return _evaluations[evaluation_id]


@app.get("/evaluations/{evaluation_id}", response_model=EvaluationResult)
def get_evaluation_results(evaluation_id: str, token: str = Depends(require_token)):
    if evaluation_id not in _evaluation_results:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return _evaluation_results[evaluation_id]


# ---------------------------------------------------------------------------
# Misc endpoints
# ---------------------------------------------------------------------------
@app.get("/kus", response_model=List[str])
def list_kus(token: str = Depends(require_token)):
    return _kus


