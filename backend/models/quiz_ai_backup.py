from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class QuizQuestion(BaseModel):
    id: Optional[int] = None
    category: str
    subcategory: str
    question_text: str
    question_type: str  # mcq, descriptive, code
    difficulty_level: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str
    tags: Optional[List[str]] = None

class QuizAttempt(BaseModel):
    id: Optional[int] = None
    user_id: int
    question_id: int
    user_answer: str
    is_correct: bool
    time_taken_seconds: int
    attempted_at: datetime

class QuizSession(BaseModel):
    id: Optional[int] = None
    user_id: int
    quiz_type: str
    total_questions: int
    questions_answered: int
    correct_answers: int
    score: float
    duration_seconds: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str = "in_progress"

class QuizRequest(BaseModel):
    category: str
    subcategory: str
    difficulty: str = "medium"
    num_questions: int = 5
    question_type: str = "mcq"

class QuizSubmission(BaseModel):
    session_id: int
    question_id: int
    answer: str
    time_taken_seconds: int

class QuizResponse(BaseModel):
    session_id: int
    total_questions: int
    correct_answers: int
    score: float
    accuracy: float
    duration_minutes: int
    results: List[Dict[str, Any]]

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    options: List[str]
    difficulty_level: str
