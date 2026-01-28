import sys
import os
from dotenv import load_dotenv
load_dotenv()

# 1. Add the parent directory (Project Root) to sys.path
# This allows python to "see" the database folder sitting outside
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from routes import auth, progress, quiz, resume, jobs, roadmap, aptitude, leaderboard

app = FastAPI(
    title="AI Powered Training Assistant API",
    description="Backend API for AI-powered training and skill development",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(quiz.router)
app.include_router(resume.router)
app.include_router(jobs.router,tags=["Jobs"])
app.include_router(roadmap.router)
app.include_router(aptitude.router, prefix="/api/leaderboard", tags=["Leaderboard"])
app.include_router(leaderboard.router, tags=["Leaderboard"])


@app.get("/")
def home():
    return {
        "status": "AI Training Assistant Backend Running",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health": "ok"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}


