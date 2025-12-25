from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    topic: Optional[str] = "general"


class ChatResponse(BaseModel):
    response: str
    question_id: Optional[int] = None
    difficulty: Optional[float] = None
    is_question: bool
    topic: str = "general"


class AnswerRequest(BaseModel):
    question_id: int
    answer: str = Field(min_length=1)


class AnswerResponse(BaseModel):
    is_correct: bool
    feedback: str
    explanation: str
    new_difficulty: float
    streak: int
