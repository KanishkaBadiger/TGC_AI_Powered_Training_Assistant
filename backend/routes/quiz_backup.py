"""
Quiz routes for managing quiz generation and attempts
"""
from fastapi import APIRouter, HTTPException, Depends
from models.quiz import (
    QuizRequest, QuizSubmission, QuizSession, QuizResponse, 
    QuizQuestion, QuestionResponse
)
from db.sqlite import get_connection
from services.llm_service import LLMService
from utils.jwt_handler import verify_token
from datetime import datetime
import json

router = APIRouter()

@router.post("/generate")
def generate_quiz(request: QuizRequest, user=Depends(verify_token)):
    """Generate a new quiz based on category and difficulty"""
    try:
        # Generate questions using LLM
        questions = LLMService.generate_quiz_questions(
            category=request.category,
            subcategory=request.subcategory,
            difficulty=request.difficulty,
            num_questions=request.num_questions,
            question_type=request.question_type
        )
        
        if not questions:
            raise HTTPException(500, "Failed to generate quiz questions")
        
        # Save questions to database
        conn = get_connection()
        cursor = conn.cursor()
        
        question_ids = []
        for q in questions:
            cursor.execute(
                """INSERT INTO quiz_questions 
                (category, subcategory, question_text, question_type, difficulty_level, 
                options, correct_answer, explanation, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    request.category,
                    request.subcategory,
                    q.get('question', ''),
                    request.question_type,
                    request.difficulty,
                    json.dumps(q.get('options', [])),
                    q.get('correct_answer', ''),
                    q.get('explanation', ''),
                    json.dumps([request.category, request.subcategory])
                )
            )
            question_ids.append(cursor.lastrowid)
        
        # Create quiz session
        cursor.execute(
            """INSERT INTO quiz_sessions 
            (user_id, quiz_type, total_questions, questions_answered, correct_answers, 
            score, duration_seconds, started_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user['user_id'],
                f"{request.category}_{request.subcategory}",
                request.num_questions,
                0,
                0,
                0.0,
                0,
                datetime.now(),
                "in_progress"
            )
        )
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "session_id": session_id,
            "total_questions": request.num_questions,
            "questions": [
                {
                    "id": qid,
                    "question_text": q.get('question', ''),
                    "options": q.get('options', []),
                    "difficulty_level": request.difficulty
                }
                for qid, q in zip(question_ids, questions)
            ]
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/submit-answer")
def submit_answer(submission: QuizSubmission, user=Depends(verify_token)):
    """Submit an answer to a quiz question"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get the correct answer
        cursor.execute(
            "SELECT correct_answer FROM quiz_questions WHERE id=?",
            (submission.question_id,)
        )
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(404, "Question not found")
        
        correct_answer = result[0]
        is_correct = submission.answer.strip().lower() == correct_answer.strip().lower()
        
        # Record the attempt
        cursor.execute(
            """INSERT INTO quiz_attempts 
            (user_id, question_id, user_answer, is_correct, time_taken_seconds, attempted_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                user['user_id'],
                submission.question_id,
                submission.answer,
                is_correct,
                submission.time_taken_seconds,
                datetime.now()
            )
        )
        
        # Update session
        if is_correct:
            cursor.execute(
                """UPDATE quiz_sessions 
                SET correct_answers = correct_answers + 1, questions_answered = questions_answered + 1
                WHERE id=?""",
                (submission.session_id,)
            )
        else:
            cursor.execute(
                """UPDATE quiz_sessions 
                SET questions_answered = questions_answered + 1
                WHERE id=?""",
                (submission.session_id,)
            )
        
        conn.commit()
        conn.close()
        
        return {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "message": "Answer submitted successfully"
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/submit-session")
def submit_session(session_id: int, user=Depends(verify_token)):
    """Complete a quiz session and calculate score"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get session details
        cursor.execute(
            "SELECT user_id, total_questions, correct_answers FROM quiz_sessions WHERE id=?",
            (session_id,)
        )
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(404, "Session not found")
        
        user_id, total_questions, correct_answers = result
        
        if user_id != user['user_id']:
            raise HTTPException(403, "Unauthorized")
        
        # Calculate score
        score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Update session
        cursor.execute(
            """UPDATE quiz_sessions 
            SET score = ?, status = 'completed', completed_at = ?
            WHERE id=?""",
            (score, datetime.now(), session_id)
        )
        
        # Update user progress
        cursor.execute(
            """UPDATE user_progress 
            SET total_quizzes_attempted = total_quizzes_attempted + 1,
                total_correct_answers = total_correct_answers + ?,
                average_score = (average_score * total_quizzes_attempted + ?) / (total_quizzes_attempted + 1),
                last_activity_date = ?
            WHERE user_id=?""",
            (correct_answers, score, datetime.now().date(), user_id)
        )
        
        # Update streak
        cursor.execute(
            """SELECT last_activity_date FROM streaks WHERE user_id=?""",
            (user_id,)
        )
        last_activity = cursor.fetchone()
        
        if last_activity and last_activity[0]:
            # Check if activity is consecutive
            from datetime import date, timedelta
            today = date.today()
            if date.fromisoformat(str(last_activity[0])) == today - timedelta(days=1):
                # Consecutive day, increase streak
                cursor.execute(
                    """UPDATE streaks 
                    SET current_streak = current_streak + 1, last_activity_date = ?
                    WHERE user_id=?""",
                    (today, user_id)
                )
            elif date.fromisoformat(str(last_activity[0])) != today:
                # Not consecutive, reset streak
                cursor.execute(
                    """UPDATE streaks 
                    SET current_streak = 1, last_activity_date = ?
                    WHERE user_id=?""",
                    (today, user_id)
                )
        else:
            cursor.execute(
                """UPDATE streaks 
                SET current_streak = 1, last_activity_date = ?
                WHERE user_id=?""",
                (datetime.now().date(), user_id)
            )
        
        conn.commit()
        
        # Get results
        cursor.execute(
            """SELECT user_answer, is_correct FROM quiz_attempts 
            WHERE user_id=? AND question_id IN (
                SELECT id FROM quiz_questions WHERE id IN (
                    SELECT question_id FROM quiz_attempts WHERE user_id=? AND attempted_at > ?
                )
            )""",
            (user_id, user_id, (datetime.now().timestamp() - 3600))
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return {
            "session_id": session_id,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "score": score,
            "accuracy": (correct_answers / total_questions * 100) if total_questions > 0 else 0,
            "message": "Quiz submitted successfully"
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/history")
def get_quiz_history(user=Depends(verify_token)):
    """Get user's quiz history"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, quiz_type, total_questions, correct_answers, score, 
            duration_seconds, completed_at FROM quiz_sessions 
            WHERE user_id=? AND status='completed' ORDER BY completed_at DESC LIMIT 20""",
            (user['user_id'],)
        )
        
        history = []
        for row in cursor.fetchall():
            history.append({
                "session_id": row[0],
                "quiz_type": row[1],
                "total_questions": row[2],
                "correct_answers": row[3],
                "score": row[4],
                "duration_minutes": row[5] // 60 if row[5] else 0,
                "completed_at": row[6]
            })
        
        conn.close()
        return history
    except Exception as e:
        raise HTTPException(500, str(e))
