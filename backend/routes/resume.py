"""
Resume routes for analyzing resumes and identifying skill gaps
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from db.sqlite import get_connection
from services.resume_analyzer import ResumeAnalyzer
from services.vector_service import VectorService
from utils.jwt_handler import verify_token
from datetime import datetime
import json

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), user=Depends(verify_token)):
    """Upload and analyze resume"""
    try:
        # Read file content
        content = await file.read()
        resume_text = content.decode('utf-8')
        
        # Analyze resume
        analysis = ResumeAnalyzer.parse_resume(resume_text)
        
        # Save to database
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO resumes 
            (user_id, file_path, file_name, content, skills_extracted, experience_years, 
            education_details, uploaded_at, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user['user_id'],
                f"resumes/{user['user_id']}/{file.filename}",
                file.filename,
                resume_text,
                json.dumps(analysis.get('skills', [])),
                analysis.get('experience_years', 0),
                json.dumps(analysis.get('education', [])),
                datetime.now(),
                datetime.now()
            )
        )
        
        resume_id = cursor.lastrowid
        conn.commit()
        
        # Add to vector database for similarity search
        VectorService.add_resume_embeddings(user['user_id'], resume_text)
        
        # Update user profile with extracted skills
        cursor.execute(
            """UPDATE user_profiles 
            SET education=?, experience_years=?, skills=?
            WHERE user_id=?""",
            (
                json.dumps(analysis.get('education', [])),
                analysis.get('experience_years', 0),
                json.dumps(analysis.get('skills', [])),
                user['user_id']
            )
        )
        
        conn.commit()
        conn.close()
        
        return {
            "resume_id": resume_id,
            "message": "Resume uploaded and analyzed successfully",
            "analysis": {
                "skills": analysis.get('skills', []),
                "experience_years": analysis.get('experience_years', 0),
                "education": analysis.get('education', []),
                "certifications": analysis.get('certifications', []),
                "languages": analysis.get('languages', [])
            }
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/analysis/{resume_id}")
def get_resume_analysis(resume_id: int, user=Depends(verify_token)):
    """Get detailed resume analysis"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT skills_extracted, experience_years, education_details, analyzed_at 
            FROM resumes WHERE id=? AND user_id=?""",
            (resume_id, user['user_id'])
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(404, "Resume not found")
        
        return {
            "resume_id": resume_id,
            "skills": json.loads(result[0]) if result[0] else [],
            "experience_years": result[1],
            "education": json.loads(result[2]) if result[2] else [],
            "analyzed_at": result[3]
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/skill-gap")
def analyze_skill_gap(target_role: str, user=Depends(verify_token)):
    """Analyze skill gaps for target role"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get user's current skills
        cursor.execute(
            "SELECT skills FROM user_profiles WHERE user_id=?",
            (user['user_id'],)
        )
        result = cursor.fetchone()
        current_skills = json.loads(result[0]) if result and result[0] else []
        
        # Analyze skill gaps
        gap_analysis = ResumeAnalyzer.analyze_skill_gaps(
            current_skills=current_skills,
            target_role=target_role,
            user_id=user['user_id']
        )
        
        # Save analysis to database
        cursor.execute(
            """INSERT INTO skill_gaps 
            (user_id, target_role, required_skills, current_skills, missing_skills, 
            skill_proficiency_gap, recommendations, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user['user_id'],
                target_role,
                json.dumps(gap_analysis.get('required_skills', [])),
                json.dumps(current_skills),
                json.dumps(gap_analysis.get('missing_skills', [])),
                json.dumps(gap_analysis.get('skill_match_percentage', 0)),
                json.dumps(gap_analysis.get('recommendations', [])),
                datetime.now()
            )
        )
        
        conn.commit()
        conn.close()
        
        return {
            "target_role": target_role,
            "current_skills": current_skills,
            "required_skills": gap_analysis.get('required_skills', []),
            "missing_skills": gap_analysis.get('missing_skills', []),
            "skill_match_percentage": gap_analysis.get('skill_match_percentage', 0),
            "priority_skills": gap_analysis.get('priority_skills', []),
            "estimated_learning_time_weeks": gap_analysis.get('estimated_learning_time_weeks', 0),
            "recommendations": gap_analysis.get('recommendations', [])
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/skill-development-plan")
def get_skill_development_plan(target_role: str, user=Depends(verify_token)):
    """Get detailed skill development plan"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get user's current skills
        cursor.execute(
            "SELECT skills FROM user_profiles WHERE user_id=?",
            (user['user_id'],)
        )
        result = cursor.fetchone()
        current_skills = json.loads(result[0]) if result and result[0] else []
        
        # Get required skills for target role
        cursor.execute(
            "SELECT required_skills FROM skill_gaps WHERE user_id=? AND target_role=? ORDER BY created_at DESC LIMIT 1",
            (user['user_id'], target_role)
        )
        gap_result = cursor.fetchone()
        target_skills = json.loads(gap_result[0]) if gap_result and gap_result[0] else []
        
        conn.close()
        
        # Generate development plan
        plan = ResumeAnalyzer.generate_skill_development_plan(
            current_skills=current_skills,
            target_skills=target_skills,
            available_hours_per_week=10
        )
        
        return {
            "target_role": target_role,
            "plan": plan
        }
    except Exception as e:
        raise HTTPException(500, str(e))
