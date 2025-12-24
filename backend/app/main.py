from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import engine, Base

# ✅ IMPORTANT: import models so tables create correctly
from app.models import User, Question, Response, Progress  # noqa: F401

from app.api import auth, chat, progress, analytics

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# ✅ CORS (frontend runs on 8080)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


@app.get("/")
async def root():
    return {
        "message": "Conversational LMS API",
        "version": settings.APP_VERSION,
        "status": "active",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
