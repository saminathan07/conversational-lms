from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import random
import uuid
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.question import Question
from app.models.response import Response
from app.schemas.quiz_schema import (
    QuizStartRequest, QuizSessionStart, QuizQuestion, QuizOption,
    QuizAnswerSubmit, QuizAnswerResult, QuizSessionComplete
)
from app.api.auth import get_current_user
from app.services.adaptive import adaptive_engine
from app.services.feedback import feedback_generator
from app.services.ai_engine import ai_engine

router = APIRouter()

# Store active quiz sessions: {session_id: {user_id, topic, questions, current_index, start_time, answers}}
active_sessions = {}


@router.post("/start", response_model=QuizSessionStart)
async def start_quiz(
    quiz_request: QuizStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new quiz session"""
    
    # Get questions for the topic
    questions = db.query(Question).filter(
        Question.topic == quiz_request.topic
    ).order_by(func.random()).limit(quiz_request.number_of_questions).all()
    
    if len(questions) < quiz_request.number_of_questions:
        # Not enough questions in DB, generate new ones
        needed = quiz_request.number_of_questions - len(questions)
        for _ in range(needed):
            question_data = ai_engine.generate_mcq_question(
                topic=quiz_request.topic,
                difficulty=current_user.current_difficulty
            )
            
            # Save question to database
            new_question = Question(
                user_id=current_user.id,
                topic=quiz_request.topic,
                difficulty=current_user.current_difficulty,
                question_text=question_data["question"],
                correct_answer=question_data["answer"],
                correct_option_id=question_data["correct_option_id"],
                explanation=question_data["explanation"],
                options=question_data["options"]
            )
            db.add(new_question)
            db.commit()
            db.refresh(new_question)
            questions.append(new_question)
    
    # Create session
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {
        "user_id": current_user.id,
        "topic": quiz_request.topic,
        "questions": [q.id for q in questions],
        "current_index": 0,
        "start_time": datetime.now(),
        "answers": [],
        "scores": 0
    }
    
    # Format first question
    first_question = questions[0]
    quiz_question = QuizQuestion(
        question_id=first_question.id,
        question_text=first_question.question_text,
        options=[QuizOption(id=opt["id"], text=opt["text"]) for opt in first_question.options],
        topic=quiz_request.topic,
        difficulty=current_user.current_difficulty,
        question_number=1,
        total_questions=len(questions)
    )
    
    return QuizSessionStart(
        session_id=session_id,
        topic=quiz_request.topic,
        difficulty_level=current_user.current_difficulty,
        first_question=quiz_question,
        total_questions=len(questions)
    )


@router.post("/answer", response_model=QuizAnswerResult)
async def submit_quiz_answer(
    answer: QuizAnswerSubmit,
    session_id: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit answer to a quiz question"""
    
    # Validate session
    if session_id not in active_sessions:
        raise HTTPException(status_code=400, detail="Invalid quiz session")
    
    session = active_sessions[session_id]
    if session["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized for this session")
    
    # Get question
    question = db.query(Question).filter(
        Question.id == answer.question_id
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if answer is correct
    is_correct = answer.selected_option_id == question.correct_option_id
    
    # Update streak and difficulty
    new_streak = adaptive_engine.update_streak(current_user.correct_streak, is_correct)
    new_difficulty = adaptive_engine.adjust_difficulty(
        current_difficulty=current_user.current_difficulty,
        is_correct=is_correct,
        streak=new_streak
    )
    
    # Points
    points_earned = 10 if is_correct else 0
    session["scores"] += points_earned
    
    # Save response
    new_response = Response(
        user_id=current_user.id,
        question_id=question.id,
        user_answer=str(answer.selected_option_id),
        is_correct=is_correct,
        feedback=f"{'Correct!' if is_correct else 'Incorrect!'}",
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
    db.refresh(current_user)
    
    # Record answer in session
    session["answers"].append({
        "question_id": question.id,
        "selected_option_id": answer.selected_option_id,
        "is_correct": is_correct,
        "points": points_earned
    })
    session["current_index"] += 1
    
    # Prepare next question if available
    next_question = None
    quiz_complete = session["current_index"] >= len(session["questions"])
    
    if not quiz_complete:
        next_q = db.query(Question).filter(
            Question.id == session["questions"][session["current_index"]]
        ).first()
        
        if next_q:
            next_question = QuizQuestion(
                question_id=next_q.id,
                question_text=next_q.question_text,
                options=[QuizOption(id=opt["id"], text=opt["text"]) for opt in next_q.options],
                topic=session["topic"],
                difficulty=current_user.current_difficulty,
                question_number=session["current_index"] + 1,
                total_questions=len(session["questions"])
            )
    
    return QuizAnswerResult(
        question_id=question.id,
        is_correct=is_correct,
        correct_option_id=question.correct_option_id,
        explanation=question.explanation,
        points_earned=points_earned,
        current_score=session["scores"],
        current_streak=new_streak,
        new_difficulty=new_difficulty,
        next_question=next_question,
        quiz_complete=quiz_complete
    )


@router.post("/complete", response_model=QuizSessionComplete)
async def complete_quiz(
    session_id: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete quiz session and get results"""
    
    if session_id not in active_sessions:
        raise HTTPException(status_code=400, detail="Invalid quiz session")
    
    session = active_sessions[session_id]
    if session["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized for this session")
    
    # Calculate stats
    correct_count = sum(1 for a in session["answers"] if a["is_correct"])
    incorrect_count = len(session["answers"]) - correct_count
    percentage = (correct_count / len(session["answers"]) * 100) if session["answers"] else 0
    
    time_taken = int((datetime.now() - session["start_time"]).total_seconds())
    
    # Clean up session
    del active_sessions[session_id]
    
    return QuizSessionComplete(
        session_id=session_id,
        topic=session["topic"],
        total_questions=len(session["answers"]),
        correct_answers=correct_count,
        incorrect_answers=incorrect_count,
        score_percentage=percentage,
        time_taken_seconds=time_taken,
        final_difficulty=current_user.current_difficulty,
        questions_data=session["answers"]
    )


@router.get("/topics")
async def get_available_topics():
    """Get list of available topics for quiz"""
    topics = [
        {"id": "python_basics", "name": "🐍 Python Basics", "description": "Learn Python fundamentals"},
        {"id": "web_security", "name": "🌐 Web Security", "description": "Secure web development"},
        {"id": "networking", "name": "📡 Networking", "description": "Network fundamentals"},
        {"id": "linux_security", "name": "🐧 Linux Security", "description": "Linux hardening & security"},
        {"id": "cryptography", "name": "🔐 Cryptography", "description": "Encryption & hashing"},
        {"id": "incident_response", "name": "🚨 Incident Response", "description": "Handling security incidents"},
    ]
    return {"topics": topics}
