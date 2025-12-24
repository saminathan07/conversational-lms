from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.question import Question
from app.models.response import Response
from app.schemas.chat_schema import ChatRequest, ChatResponse, AnswerRequest, AnswerResponse
from app.services.ai_engine import ai_engine
from app.services.adaptive import adaptive_engine
from app.services.feedback import feedback_generator
from app.api.auth import get_current_user
from app.utils.helpers import get_topic_display_name

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle chat message and generate question"""
    
    # Generate question based on user's current difficulty
    question_data = ai_engine.generate_question(
        topic=chat_request.topic,
        difficulty=current_user.current_difficulty
    )
    
    # Save question to database
    new_question = Question(
        user_id=current_user.id,
        topic=chat_request.topic,
        difficulty=current_user.current_difficulty,
        question_text=question_data["question"],
        correct_answer=question_data["answer"],
        explanation=question_data["explanation"]
    )
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    return ChatResponse(
        response=question_data["question"],
        question_id=new_question.id,
        difficulty=current_user.current_difficulty,
        is_question=True,
        topic=get_topic_display_name(chat_request.topic)
    )


@router.post("/answer", response_model=AnswerResponse)
async def submit_answer(
    answer_request: AnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Evaluate user's answer"""
    
    # Get question
    question = db.query(Question).filter(Question.id == answer_request.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Evaluate answer
    is_correct, ai_feedback, confidence = ai_engine.evaluate_answer(
        question=question.question_text,
        correct_answer=question.correct_answer,
        user_answer=answer_request.answer
    )
    
    # Update streak
    new_streak = adaptive_engine.update_streak(current_user.correct_streak, is_correct)
    
    # Adjust difficulty
    new_difficulty = adaptive_engine.adjust_difficulty(
        current_difficulty=current_user.current_difficulty,
        is_correct=is_correct,
        streak=new_streak
    )
    
    # Generate feedback
    feedback = feedback_generator.generate_feedback(
        is_correct=is_correct,
        difficulty=current_user.current_difficulty,
        streak=new_streak,
        explanation=question.explanation
    )
    
    # Save response
    new_response = Response(
        user_id=current_user.id,
        question_id=question.id,
        user_answer=answer_request.answer,
        is_correct=is_correct,
        confidence_score=confidence,
        feedback=feedback,
        difficulty_at_time=current_user.current_difficulty
    )
    
    db.add(new_response)
    
    # Update user stats
    current_user.correct_streak = new_streak
    current_user.current_difficulty = new_difficulty
    current_user.total_questions += 1
    if is_correct:
        current_user.correct_answers += 1
    
    db.commit()
    
    return AnswerResponse(
        is_correct=is_correct,
        feedback=feedback,
        explanation=question.explanation,
        new_difficulty=new_difficulty,
        streak=new_streak
    )