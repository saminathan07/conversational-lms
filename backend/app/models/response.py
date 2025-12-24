from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base


class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    confidence_score = Column(Float)
    time_taken_seconds = Column(Integer)
    
    feedback = Column(Text)
    difficulty_at_time = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())