"""
Roadmap routes for learning path and milestone tracking
"""
from fastapi import APIRouter, HTTPException, Depends
from db.sqlite import get_connection
from services.llm_service import LLMService
from utils.jwt_handler import verify_token
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.post("/generate")
def generate_roadmap(
    current_role: str,
    target_role: str,
    available_hours_per_week: int = 10,
    user=Depends(verify_token)
):
    """Generate personalized learning roadmap"""
    try:
        # Generate roadmap using LLM
        roadmap_data = LLMService.generate_personalized_roadmap(
            current_role=current_role,
            target_role=target_role,
            available_hours_per_week=available_hours_per_week
        )
        
        # Save to database
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO learning_roadmap 
            (user_id, roadmap_name, target_goal, description, modules, created_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                user['user_id'],
                f"{current_role} to {target_role}",
                target_role,
                roadmap_data.get('title', ''),
                json.dumps(roadmap_data.get('modules', [])),
                datetime.now()
            )
        )
        
        roadmap_id = cursor.lastrowid
        
        # Add milestones
        modules = roadmap_data.get('modules', [])
        for idx, module in enumerate(modules):
            start_date = datetime.now() + timedelta(weeks=idx*4)
            end_date = start_date + timedelta(weeks=4)
            
            cursor.execute(
                """INSERT INTO roadmap_milestones 
                (roadmap_id, milestone_name, description, start_date, end_date, status)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    roadmap_id,
                    module.get('module_name', f'Module {idx+1}'),
                    json.dumps(module),
                    start_date.date(),
                    end_date.date(),
                    'pending'
                )
            )
        
        # Update user profile
        cursor.execute(
            "UPDATE user_profiles SET target_role=? WHERE user_id=?",
            (target_role, user['user_id'])
        )
        
        conn.commit()
        conn.close()
        
        return {
            "roadmap_id": roadmap_id,
            "roadmap_name": f"{current_role} to {target_role}",
            "target_goal": target_role,
            "estimated_duration_months": roadmap_data.get('duration_months', 0),
            "modules": roadmap_data.get('modules', []),
            "timeline": roadmap_data.get('timeline', []),
            "resources": roadmap_data.get('resources', {}),
            "message": "Roadmap generated successfully"
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/{roadmap_id}")
def get_roadmap(roadmap_id: int, user=Depends(verify_token)):
    """Get roadmap details"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, roadmap_name, target_goal, description, modules, created_at 
            FROM learning_roadmap WHERE id=? AND user_id=?""",
            (roadmap_id, user['user_id'])
        )
        
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(404, "Roadmap not found")
        
        # Get milestones
        cursor.execute(
            """SELECT id, milestone_name, description, start_date, end_date, status, progress_percentage
            FROM roadmap_milestones WHERE roadmap_id=? ORDER BY start_date""",
            (roadmap_id,)
        )
        
        milestones = []
        for row in cursor.fetchall():
            milestones.append({
                "id": row[0],
                "milestone_name": row[1],
                "description": json.loads(row[2]) if row[2] else {},
                "start_date": row[3],
                "end_date": row[4],
                "status": row[5],
                "progress_percentage": row[6]
            })
        
        conn.close()
        
        return {
            "id": result[0],
            "roadmap_name": result[1],
            "target_goal": result[2],
            "description": result[3],
            "modules": json.loads(result[4]) if result[4] else [],
            "milestones": milestones,
            "created_at": result[5]
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put("/{roadmap_id}/milestone/{milestone_id}")
def update_milestone(
    roadmap_id: int,
    milestone_id: int,
    status: str,
    progress_percentage: int = 0,
    user=Depends(verify_token)
):
    """Update milestone status and progress"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verify ownership
        cursor.execute(
            "SELECT user_id FROM learning_roadmap WHERE id=?",
            (roadmap_id,)
        )
        result = cursor.fetchone()
        
        if not result or result[0] != user['user_id']:
            raise HTTPException(403, "Unauthorized")
        
        cursor.execute(
            """UPDATE roadmap_milestones 
            SET status=?, progress_percentage=? WHERE id=? AND roadmap_id=?""",
            (status, progress_percentage, milestone_id, roadmap_id)
        )
        
        conn.commit()
        conn.close()
        
        return {"message": "Milestone updated successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/user/roadmaps")
def get_user_roadmaps(user=Depends(verify_token)):
    """Get all user's roadmaps"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, roadmap_name, target_goal, created_at 
            FROM learning_roadmap WHERE user_id=? ORDER BY created_at DESC""",
            (user['user_id'],)
        )
        
        roadmaps = []
        for row in cursor.fetchall():
            roadmaps.append({
                "id": row[0],
                "roadmap_name": row[1],
                "target_goal": row[2],
                "created_at": row[3]
            })
        
        conn.close()
        return {"roadmaps": roadmaps}
    except Exception as e:
        raise HTTPException(500, str(e))
