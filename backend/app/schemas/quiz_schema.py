from pydantic import BaseModel, Field
from typing import List, Optional


class QuizOption(BaseModel):
    """Single MCQ option"""
    id: int
    text: str


class QuizQuestion(BaseModel):
    """Quiz question with MCQ options"""
    question_id: int
    question_text: str
    options: List[QuizOption]
    topic: str
    difficulty: float
    question_number: int
    total_questions: Optional[int] = None


class QuizStartRequest(BaseModel):
    """Request to start a quiz"""
    topic: str
    number_of_questions: int = Field(default=10, ge=1, le=50)


class QuizAnswerSubmit(BaseModel):
    """Submit answer for a quiz question"""
    question_id: int
    selected_option_id: int


class QuizAnswerResult(BaseModel):
    """Result of submitted answer"""
    question_id: int
    is_correct: bool
    correct_option_id: int
    explanation: str
    points_earned: int
    current_score: int
    current_streak: int
    new_difficulty: float
    next_question: Optional[QuizQuestion] = None
    quiz_complete: bool = False


class QuizSessionStart(BaseModel):
    """Quiz session details"""
    session_id: str
    topic: str
    difficulty_level: float
    first_question: QuizQuestion
    total_questions: int


class QuizSessionComplete(BaseModel):
    """Final quiz results"""
    session_id: str
    topic: str
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    score_percentage: float
    time_taken_seconds: int
    final_difficulty: float
    questions_data: List[dict]
