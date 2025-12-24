from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.user import User
from app.models.response import Response
from app.models.question import Question
from app.schemas.progress_schema import ProgressSummary, TopicProgress
from app.api.auth import get_current_user
from app.utils.helpers import calculate_accuracy

router = APIRouter()


@router.get("/summary", response_model=ProgressSummary)
async def get_progress_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's overall progress summary"""

    # Total questions answered
    total_attempts = (
        db.query(func.count(Response.id))
        .filter(Response.user_id == current_user.id)
        .scalar()
    )

    # Correct answers
    correct_answers = (
        db.query(func.count(Response.id))
        .filter(
            Response.user_id == current_user.id,
            Response.is_correct == True
        )
        .scalar()
    )

    accuracy = calculate_accuracy(correct_answers, total_attempts)

    # Topics user has interacted with
    topics = (
        db.query(Question.topic)
        .join(Response, Response.question_id == Question.id)
        .filter(Response.user_id == current_user.id)
        .distinct()
        .all()
    )

    return {
        "total_questions": total_attempts,
        "correct_answers": correct_answers,
        "accuracy": accuracy,
        "topics": [t[0] for t in topics],
    }
