"""
Leaderboard routes for ranking and achievements
"""
from fastapi import APIRouter, Depends, HTTPException
from db.sqlite import get_connection
from utils.jwt_handler import verify_token
from datetime import datetime

router = APIRouter()

@router.get("/global")
def get_global_leaderboard(limit: int = 50):
    """Get global leaderboard"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT l.rank, u.username, u.avatar_url, l.total_points, 
            l.quizzes_completed, l.accuracy, l.streak_count, l.last_updated
            FROM leaderboard l
            JOIN users u ON l.user_id = u.id
            ORDER BY l.total_points DESC LIMIT ?""",
            (limit,)
        )
        
        leaderboard = []
        for idx, row in enumerate(cursor.fetchall(), 1):
            leaderboard.append({
                "rank": idx,
                "username": row[1],
                "avatar_url": row[2],
                "total_points": row[3],
                "quizzes_completed": row[4],
                "accuracy": row[5],
                "streak_count": row[6],
                "last_updated": row[7]
            })
        
        conn.close()
        return {"leaderboard": leaderboard}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/user-rank")
def get_user_rank(user=Depends(verify_token)):
    """Get user's rank and position"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT rank, total_points, quizzes_completed, accuracy, streak_count
            FROM leaderboard WHERE user_id=?""",
            (user['user_id'],)
        )
        
        result = cursor.fetchone()
        
        if not result:
            # Initialize leaderboard entry
            cursor.execute(
                "INSERT INTO leaderboard (user_id, rank) VALUES (?, ?)",
                (user['user_id'], 999999)
            )
            conn.commit()
            return {
                "rank": 999999,
                "total_points": 0,
                "quizzes_completed": 0,
                "accuracy": 0,
                "streak_count": 0
            }
        
        # Get total users for percentile
        cursor.execute("SELECT COUNT(*) FROM leaderboard")
        total_users = cursor.fetchone()[0]
        
        conn.close()
        
        percentile = (result[0] / total_users) * 100 if total_users > 0 else 0
        
        return {
            "rank": result[0],
            "total_points": result[1],
            "quizzes_completed": result[2],
            "accuracy": result[3],
            "streak_count": result[4],
            "percentile": percentile,
            "total_users": total_users
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/category-leaders/{category}")
def get_category_leaders(category: str, limit: int = 10):
    """Get top performers in a specific category"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # This would need a more complex query to track category-wise scores
        # For now, returning based on overall leaderboard
        cursor.execute(
            """SELECT u.username, COUNT(*) as questions_attempted, 
            AVG(CASE WHEN qa.is_correct THEN 1 ELSE 0 END) as accuracy
            FROM quiz_attempts qa
            JOIN quiz_questions qq ON qa.question_id = qq.id
            JOIN users u ON qa.user_id = u.id
            WHERE qq.category = ?
            GROUP BY u.id
            ORDER BY accuracy DESC, questions_attempted DESC
            LIMIT ?""",
            (category, limit)
        )
        
        leaders = []
        for idx, row in enumerate(cursor.fetchall(), 1):
            leaders.append({
                "rank": idx,
                "username": row[0],
                "questions_attempted": row[1],
                "accuracy": row[2]
            })
        
        conn.close()
        return {"category": category, "leaders": leaders}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/weekly")
def get_weekly_leaderboard():
    """Get weekly leaderboard based on recent activity"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get top performers from last 7 days
        cursor.execute(
            """SELECT u.username, u.avatar_url, COUNT(DISTINCT qa.id) as attempts,
            AVG(CASE WHEN qa.is_correct THEN 1 ELSE 0 END) as accuracy
            FROM quiz_attempts qa
            JOIN users u ON qa.user_id = u.id
            WHERE qa.attempted_at > datetime('now', '-7 days')
            GROUP BY u.id
            ORDER BY accuracy DESC, attempts DESC
            LIMIT 50""",
        )
        
        leaderboard = []
        for idx, row in enumerate(cursor.fetchall(), 1):
            leaderboard.append({
                "rank": idx,
                "username": row[0],
                "avatar_url": row[1],
                "attempts": row[2],
                "accuracy": row[3]
            })
        
        conn.close()
        return {"period": "weekly", "leaderboard": leaderboard}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put("/update-points")
def update_leaderboard_points(user_id: int, points_earned: int, user=Depends(verify_token)):
    """Update leaderboard points (admin/system use)"""
    try:
        if user['user_id'] != user_id:
            raise HTTPException(403, "Unauthorized")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """UPDATE leaderboard 
            SET total_points = total_points + ?
            WHERE user_id=?""",
            (points_earned, user_id)
        )
        
        # Recalculate ranks
        cursor.execute(
            """SELECT user_id FROM leaderboard ORDER BY total_points DESC"""
        )
        
        rank = 1
        for row in cursor.fetchall():
            cursor.execute(
                "UPDATE leaderboard SET rank = ? WHERE user_id = ?",
                (rank, row[0])
            )
            rank += 1
        
        conn.commit()
        conn.close()
        
        return {"message": "Points updated successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))
