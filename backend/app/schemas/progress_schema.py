
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class ProgressSummary(BaseModel):
    user_id: int
    total_questions: int
    correct_answers: int
    accuracy: float
    current_difficulty: float
    current_streak: int
    topics_covered: List[str]
    
    class Config:
        from_attributes = True


class TopicProgress(BaseModel):
    topic: str
    difficulty_level: float
    accuracy: float
    questions_completed: int
    strengths: Optional[Dict] = None
    weaknesses: Optional[Dict] = None
    last_activity: datetime
    
    class Config:
        from_attributes = True