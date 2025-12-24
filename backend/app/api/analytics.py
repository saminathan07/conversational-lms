from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict

from app.db.database import get_db
from app.models.user import User
from app.models.response import Response
from app.models.question import Question
from app.api.auth import get_current_user
from app.services.scoring import scoring_system

router = APIRouter()


@router.get("/performance")
async def get_performance_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed performance analytics"""
    
    responses = db.query(Response).filter(
        Response.user_id == current_user.id
    ).all()
    
    if not responses:
        return {
            "message": "No data yet. Start answering questions!",
            "total_questions": 0,
            "accuracy": 0.0,
            "average_difficulty": 0.0,
            "strongest_topics": [],
            "weakest_topics": []
        }
    
    # Convert to dict for analysis
    response_data = []
    for r in responses:
        question = db.query(Question).filter(Question.id == r.question_id).first()
        response_data.append({
            "is_correct": r.is_correct,
            "difficulty": r.difficulty_at_time,
            "topic": question.topic if question else "unknown"
        })
    
    analysis = scoring_system.analyze_performance(response_data)
    
    return analysis


@router.get("/history")
async def get_answer_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent answer history"""
    
    responses = db.query(Response).filter(
        Response.user_id == current_user.id
    ).order_by(Response.created_at.desc()).limit(limit).all()
    
    history = []
    for r in responses:
        question = db.query(Question).filter(Question.id == r.question_id).first()
        history.append({
            "question": question.question_text if question else "N/A",
            "user_answer": r.user_answer,
            "is_correct": r.is_correct,
            "difficulty": r.difficulty_at_time,
            "created_at": r.created_at.isoformat()
        })
    
    return history