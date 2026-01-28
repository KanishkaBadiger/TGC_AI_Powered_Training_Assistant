from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date, timedelta
from database.database import get_db
from database import models
from models.quiz_ai import generate_quiz_questions

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])

# --- DATA MODELS ---
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

# --- GENERATE ROUTE ---
@router.post("/generate")
def generate_quiz(req: QuizRequest):
    questions = generate_quiz_questions(req.category, req.sub_category, req.difficulty, req.num_questions)
    if not questions:
        raise HTTPException(status_code=500, detail="Failed to generate questions")
    return {"questions": questions}

# --- SUBMIT ROUTE (Connects to Leaderboard) ---
@router.post("/submit")
def submit_quiz_result(sub: QuizSubmission, db: Session = Depends(get_db)):
    print(f"📝 Processing Submission for User {sub.user_id}: Score {sub.score}")
    
    # 1. Calculate XP (10 pts per correct answer)
    xp_earned = sub.score * 10
    
    # 2. Save the Attempt History
    new_attempt = models.QuizAttempt(
        user_id=sub.user_id,
        category=sub.category,
        score=sub.score,
        total_questions=sub.total_questions,
        xp_earned=xp_earned
    )
    db.add(new_attempt)
    
    # 3. UPDATE LEADERBOARD (UserProgress Table)
    progress = db.query(models.UserProgress).filter(models.UserProgress.user_id == sub.user_id).first()
    
    if not progress:
        # Create new entry if first time
        progress = models.UserProgress(user_id=sub.user_id, total_xp=0)
        db.add(progress)
    
    # Add XP
    progress.total_xp += xp_earned
    
    # 4. UPDATE STREAK
    today = date.today()
    streak = db.query(models.Streak).filter(models.Streak.user_id == sub.user_id).first()
    
    if not streak:
        streak = models.Streak(user_id=sub.user_id, current_streak=1, last_activity_date=today)
        db.add(streak)
    else:
        if streak.last_activity_date != today:
            # If logged activity yesterday, increment. Else reset to 1.
            if streak.last_activity_date == today - timedelta(days=1):
                streak.current_streak += 1
            else:
                streak.current_streak = 1 # Streak broken
            streak.last_activity_date = today

    db.commit()
    print(f"✅ Saved! Total XP: {progress.total_xp}")
    return {"message": "Leaderboard updated", "xp": xp_earned}