from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, progress, quiz, resume, jobs, roadmap, aptitude

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
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
# app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(resume.router)
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(roadmap.router, prefix="/api/roadmap", tags=["Roadmap"])
app.include_router(aptitude.router, prefix="/api/leaderboard", tags=["Leaderboard"])

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


