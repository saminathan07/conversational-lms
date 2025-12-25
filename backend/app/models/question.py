from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.db.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    topic = Column(String, index=True)
    difficulty = Column(Float, default=1.0)

    question_text = Column(Text, nullable=False)
    correct_answer = Column(Text)
    explanation = Column(Text)

    # MCQ Options stored as JSON: [{"id": 1, "text": "Option A"}, ...]
    options = Column(JSON, nullable=True)
    correct_option_id = Column(Integer, nullable=True)  # ID of correct option

    # ❌ DO NOT use "metadata"
    extra_data = Column(JSON)  # ✅ renamed

    created_at = Column(DateTime(timezone=True), server_default=func.now())
