from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import date

from database.database import get_db
from database import models
from models.quiz_ai import generate_quiz_questions

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])

# --- REQUEST MODELS ---
class QuizRequest(BaseModel):
    category: str
    sub_category: str
    difficulty: str
    num_questions: int

class QuizSubmission(BaseModel):
    user_id: int
    category: str
    score: int
    total_questions: int

# --- ROUTES ---

@router.post("/generate")
def generate_quiz(request: QuizRequest):
    questions = generate_quiz_questions(
        request.category, request.sub_category, request.difficulty, request.num_questions
    )
    if not questions:
        raise HTTPException(status_code=500, detail="AI failed to generate quiz.")
    return {"questions": questions}

@router.post("/submit")
def submit_quiz_result(submission: QuizSubmission, db: Session = Depends(get_db)):
    """Saves result and updates User XP/Streak for Leaderboard"""
    
    # 1. Calculate XP (e.g., 10 XP per correct answer)
    xp_gained = submission.score * 10
    
    # 2. Save Quiz History
    new_attempt = models.QuizAttempt(
        user_id=submission.user_id,
        category=submission.category,
        score=submission.score,
        total_questions=submission.total_questions,
        xp_earned=xp_gained
    )
    db.add(new_attempt)
    
    # 3. Update User Total XP (For Leaderboard)
    user_progress = db.query(models.UserProgress).filter(models.UserProgress.user_id == submission.user_id).first()
    if user_progress:
        user_progress.total_xp += xp_gained
    else:
        # Create if missing
        new_progress = models.UserProgress(user_id=submission.user_id, total_xp=xp_gained)
        db.add(new_progress)
        
    # 4. Update Streak (Daily Login Logic)
    streak = db.query(models.Streak).filter(models.Streak.user_id == submission.user_id).first()
    today = date.today()
    
    if streak:
        if streak.last_activity_date != today:
            # If last activity was yesterday, increment. Else reset or keep same.
            # (Simple logic: just increment for any new daily activity)
            streak.current_streak += 1
            streak.last_activity_date = today
    else:
        new_streak = models.Streak(user_id=submission.user_id, current_streak=1, last_activity_date=today)
        db.add(new_streak)

    db.commit()
    return {"message": "Quiz saved!", "xp_earned": xp_gained}