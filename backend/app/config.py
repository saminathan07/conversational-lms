from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Conversational LMS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days

    # ✅ Database (LOCAL dev – SQLite)
    # 👉 PostgreSQL later use pannalaam
    DATABASE_URL: str = "sqlite:///./lms.db"

    # AI
    ANTHROPIC_API_KEY: Optional[str] = None

    # ✅ CORS (frontend 8080)
    CORS_ORIGINS: List[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
