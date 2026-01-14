from fastapi import APIRouter, Depends, HTTPException
from db.sqlite import get_connection
from utils.jwt_handler import verify_token
from datetime import datetime, date, timedelta

router = APIRouter()

@router.get("/")
def get_progress(user=Depends(verify_token)):
    """Get user progress and statistics"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get progress data
        cursor.execute(
            """SELECT total_quizzes_attempted, total_correct_answers, average_score, 
            current_streak, max_streak, level, total_study_hours
            FROM user_progress WHERE user_id=?""",
            (user['user_id'],)
        )
        
        progress_data = cursor.fetchone()
        
        if not progress_data:
            # Initialize if not exists
            cursor.execute(
                "INSERT INTO user_progress (user_id) VALUES (?)",
                (user['user_id'],)
            )
            conn.commit()
            progress_data = (0, 0, 0, 0, 0, 'Beginner', 0)
        
        # Get streak info
        cursor.execute(
            "SELECT current_streak, max_streak, last_activity_date FROM streaks WHERE user_id=?",
            (user['user_id'],)
        )
        
        streak_data = cursor.fetchone()
        
        if not streak_data:
            cursor.execute(
                "INSERT INTO streaks (user_id) VALUES (?)",
                (user['user_id'],)
            )
            conn.commit()
            streak_data = (0, 0, None)
        
        # Get leaderboard rank
        cursor.execute(
            "SELECT rank, total_points FROM leaderboard WHERE user_id=?",
            (user['user_id'],)
        )
        
        leaderboard_data = cursor.fetchone()
        
        conn.close()
        
        return {
            "email": user['email'],
            "total_quizzes_attempted": progress_data[0],
            "total_correct_answers": progress_data[1],
            "average_score": progress_data[2],
            "current_streak": streak_data[0] if streak_data else 0,
            "max_streak": streak_data[1] if streak_data else 0,
            "last_activity_date": streak_data[2] if streak_data else None,
            "level": progress_data[5],
            "total_study_hours": progress_data[6],
            "leaderboard_rank": leaderboard_data[0] if leaderboard_data else None,
            "total_points": leaderboard_data[1] if leaderboard_data else 0
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/statistics")
def get_statistics(user=Depends(verify_token)):
    """Get detailed user statistics"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get quiz statistics
        cursor.execute(
            """SELECT COUNT(*), AVG(score), MAX(score), MIN(score)
            FROM quiz_sessions WHERE user_id=? AND status='completed'""",
            (user['user_id'],)
        )
        
        quiz_stats = cursor.fetchone()
        
        # Get category-wise performance
        cursor.execute(
            """SELECT category, COUNT(*) as attempts, AVG(CASE WHEN is_correct THEN 1 ELSE 0 END) as accuracy
            FROM quiz_attempts qa
            JOIN quiz_questions qq ON qa.question_id = qq.id
            WHERE qa.user_id=? GROUP BY qq.category""",
            (user['user_id'],)
        )
        
        category_performance = []
        for row in cursor.fetchall():
            category_performance.append({
                "category": row[0],
                "attempts": row[1],
                "accuracy": row[2]
            })
        
        # Get daily activity
        cursor.execute(
            """SELECT DATE(attempted_at), COUNT(*) 
            FROM quiz_attempts WHERE user_id=? AND attempted_at > datetime('now', '-30 days')
            GROUP BY DATE(attempted_at) ORDER BY DATE(attempted_at)""",
            (user['user_id'],)
        )
        
        daily_activity = {}
        for row in cursor.fetchall():
            daily_activity[row[0]] = row[1]
        
        conn.close()
        
        return {
            "quiz_statistics": {
                "total_quizzes": quiz_stats[0] if quiz_stats else 0,
                "average_score": quiz_stats[1] if quiz_stats else 0,
                "highest_score": quiz_stats[2] if quiz_stats else 0,
                "lowest_score": quiz_stats[3] if quiz_stats else 0
            },
            "category_performance": category_performance,
            "daily_activity_last_30_days": daily_activity
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/streak")
def get_streak_info(user=Depends(verify_token)):
    """Get detailed streak information"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT current_streak, max_streak, last_activity_date, streak_start_date FROM streaks WHERE user_id=?",
            (user['user_id'],)
        )
        
        streak_data = cursor.fetchone()
        conn.close()
        
        if not streak_data:
            return {
                "current_streak": 0,
                "max_streak": 0,
                "last_activity_date": None,
                "days_until_streak_lost": None
            }
        
        current_streak, max_streak, last_activity, streak_start = streak_data
        
        # Calculate days until streak is lost
        if last_activity:
            last_date = datetime.strptime(str(last_activity), '%Y-%m-%d').date()
            days_until_lost = (last_date + timedelta(days=1) - date.today()).days
        else:
            days_until_lost = None
        
        return {
            "current_streak": current_streak,
            "max_streak": max_streak,
            "last_activity_date": last_activity,
            "streak_start_date": streak_start,
            "days_until_streak_lost": days_until_lost
        }
    except Exception as e:
        raise HTTPException(500, str(e))

