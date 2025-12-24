from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    topic: Optional[str] = "general"


class ChatResponse(BaseModel):
    response: str
    question_id: Optional[int] = None
    difficulty: float
    is_question: bool
    topic: str


class AnswerRequest(BaseModel):
    question_id: int
    answer: str


class AnswerResponse(BaseModel):
    is_correct: bool
    feedback: str
    explanation: str
    new_difficulty: float
    streak: int