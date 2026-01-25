from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from database.database import get_db
from database import models
from backend.models.roadmap_ai import generate_roadmap_plan # Import utility

router = APIRouter(prefix="/api/roadmap", tags=["Roadmap"])

# 1. GENERATE NEW ROADMAP
@router.post("/generate")
def create_roadmap(
    user_id: str, 
    role: str, 
    skill_level: str, 
    roadmap_type: str, 
    end_date: date,
    db: Session = Depends(get_db)
):
    # Calculate duration
    start_date = date.today()
    days_count = (end_date - start_date).days
    
    if days_count < 7:
        raise HTTPException(status_code=400, detail="Timeline too short (min 7 days)")

    # Call AI
    ai_plan = generate_roadmap_plan(role, days_count, skill_level, roadmap_type)
    
    # Save Parent Roadmap
    new_roadmap = models.Roadmap(
        user_id=user_id, role=role, skill_level=skill_level,
        start_date=start_date, end_date=end_date
    )
    db.add(new_roadmap)
    db.commit()
    db.refresh(new_roadmap)
    
    # Save Daily Tasks
    current_date = start_date
    for day_plan in ai_plan:
        task = models.RoadmapTask(
            roadmap_id=new_roadmap.id,
            day_number=day_plan['day'],
            module_name=day_plan['module'],
            topic=day_plan['topic'],
            description=day_plan['description'],
            resources=day_plan['resources'],
            estimated_minutes=day_plan['time_min'],
            date_assigned=current_date,
            status="PENDING"
        )
        db.add(task)
        current_date += timedelta(days=1)
    
    db.commit()
    return {"message": "Roadmap created successfully", "roadmap_id": new_roadmap.id}

# 2. GET TODAY'S STATUS (With Missed Day Intelligence)
@router.get("/dashboard/{user_id}")
def get_dashboard(user_id: str, db: Session = Depends(get_db)):
    today = date.today()
    
    # 1. Fetch Roadmap
    roadmap = db.query(models.Roadmap).filter(
        models.Roadmap.user_id == user_id
    ).order_by(models.Roadmap.id.desc()).first()
    
    if not roadmap:
        return {"status": "no_roadmap"}

    # 2. Logic: Auto-Mark Missed Tasks
    # If a task was due BEFORE today and is still PENDING, mark it MISSED
    overdue_tasks = db.query(models.RoadmapTask).filter(
        models.RoadmapTask.roadmap_id == roadmap.id,
        models.RoadmapTask.date_assigned < today,
        models.RoadmapTask.status == "PENDING"
    ).all()
    
    for task in overdue_tasks:
        task.status = "MISSED"
    db.commit()

    # 3. Fetch ALL tasks for the Calendar
    all_tasks = db.query(models.RoadmapTask).filter(
        models.RoadmapTask.roadmap_id == roadmap.id
    ).all()

    return {
        "status": "active",
        "roadmap_details": {
            "id": roadmap.id,
            "role": roadmap.role,
            "start_date": roadmap.start_date,
            "skill_level": roadmap.skill_level, 
            "is_paused": roadmap.is_paused
        },
        "all_tasks": all_tasks  # <--- NEW: Send all tasks to frontend
    }
# 3. MARK COMPLETE (Gamification Trigger)
@router.post("/complete/{task_id}")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.RoadmapTask).filter(models.RoadmapTask.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
        
    task.status = "COMPLETED"
    
    # Logic to add XP/Points to Leaderboard would go here
    # add_leaderboard_points(user_id, points=10)
    
    db.commit()
    return {"message": "Task Completed! +10 XP"}

# 4. RESCHEDULE (Shift everything forward)
@router.post("/reschedule/{roadmap_id}")
def reschedule_roadmap(roadmap_id: int, db: Session = Depends(get_db)):
    """
    Shifts all PENDING or MISSED tasks to start from TODAY.
    Effectively 'pausing' time for the days missed.
    """
    today = date.today()
    
    # Get all incomplete tasks ordered by day
    incomplete_tasks = db.query(models.RoadmapTask).filter(
        models.RoadmapTask.roadmap_id == roadmap_id,
        models.RoadmapTask.status.in_(["PENDING", "MISSED"])
    ).order_by(models.RoadmapTask.day_number).all()
    
    # Shift dates
    current_date = today
    for task in incomplete_tasks:
        task.date_assigned = current_date
        task.status = "PENDING" # Reset missed status
        current_date += timedelta(days=1)
        
    db.commit()
    return {"message": "Roadmap rescheduled. You're back on track!"}

# 5.Finish early
@router.post("/finish_early/{roadmap_id}")
def finish_early(roadmap_id: int, db: Session = Depends(get_db)):
    """
    Finds the first PENDING task (even if it's tomorrow) and marks it COMPLETED today.
    """
    today = date.today()
    
    # Get the next pending task sorted by day number
    next_task = db.query(models.RoadmapTask).filter(
        models.RoadmapTask.roadmap_id == roadmap_id,
        models.RoadmapTask.status == "PENDING"
    ).order_by(models.RoadmapTask.day_number).first()
    
    if not next_task:
        raise HTTPException(status_code=404, detail="No pending tasks found!")
        
    # Mark it done
    next_task.status = "COMPLETED"
    
    # Optional: If you want to strictly shift dates, logic is complex.
    # For now, we just mark it done. The calendar will turn it Green.
    # If the date was in the future, we effectively 'finished early'.
    
    db.commit()
    return {"message": "Task completed early! Keep up the streak."}

#6. pause and resume
@router.post("/toggle_pause/{roadmap_id}")
def toggle_pause(roadmap_id: int, db: Session = Depends(get_db)):
    roadmap = db.query(models.Roadmap).filter(models.Roadmap.id == roadmap_id).first()
    if not roadmap:
        raise HTTPException(404, "Roadmap not found")
    
    # TOGGLE LOGIC
    if roadmap.is_paused:
        # RESUMING: We must shift dates!
        roadmap.is_paused = False
        
        # 1. Find the first pending task (where we left off)
        first_pending = db.query(models.RoadmapTask).filter(
            models.RoadmapTask.roadmap_id == roadmap.id,
            models.RoadmapTask.status.in_(["PENDING", "MISSED"])
        ).order_by(models.RoadmapTask.day_number).first()
        
        if first_pending:
            # Calculate the shift: Make the first pending task due TODAY
            shift_start_date = first_pending.date_assigned
            today = date.today()
            days_diff = (today - shift_start_date).days
            
            # If days_diff is positive, it means we are late. Shift everything forward.
            if days_diff > 0:
                all_future_tasks = db.query(models.RoadmapTask).filter(
                    models.RoadmapTask.roadmap_id == roadmap.id,
                    models.RoadmapTask.day_number >= first_pending.day_number
                ).all()
                
                for task in all_future_tasks:
                    task.date_assigned += timedelta(days=days_diff)

    else:
        # PAUSING: Just set the flag
        roadmap.is_paused = True
    
    db.commit()
    return {"status": "paused" if roadmap.is_paused else "active"}

#Archive current roadmap
@router.post("/archive/{user_id}")
def archive_current_roadmap(user_id: str, db: Session = Depends(get_db)):
    # Find the active roadmap
    active_map = db.query(models.Roadmap).filter(
        models.Roadmap.user_id == user_id,
        models.Roadmap.is_active == True # You would need to add this column to your model
    ).first()
    
    if active_map:
        active_map.is_active = False
        db.commit()
    return {"message": "Archived"}