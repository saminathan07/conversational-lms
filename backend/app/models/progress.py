from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base


class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    topic = Column(String, index=True)
    difficulty_level = Column(Float)
    accuracy = Column(Float)
    questions_completed = Column(Integer, default=0)
    
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())