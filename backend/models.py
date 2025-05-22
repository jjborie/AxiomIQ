from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.types import JSON
from .database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    options = Column(JSON)
    correct = Column(String, nullable=False)
    ku = Column(String, nullable=False)

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    api_key = Column(String)
    model_name = Column(String)
