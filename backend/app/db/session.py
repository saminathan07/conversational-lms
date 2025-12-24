from app.db.database import SessionLocal


def get_session():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()