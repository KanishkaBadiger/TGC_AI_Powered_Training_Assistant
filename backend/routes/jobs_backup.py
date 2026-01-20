"""
Jobs routes for fetching and managing job/internship postings
"""
from fastapi import APIRouter, HTTPException, Depends
from db.sqlite import get_connection
from services.job_fetcher import JobFetcher
from services.vector_service import VectorService
from utils.jwt_handler import verify_token
from datetime import datetime
import json

router = APIRouter()

@router.get("/fetch")
def fetch_jobs(user=Depends(verify_token)):
    """Fetch latest job and internship postings"""
    try:
        jobs = JobFetcher.get_all_jobs()
        
        # Save to database
        conn = get_connection()
        cursor = conn.cursor()
        
        for job in jobs:
            # Check if job already exists
            cursor.execute(
                "SELECT id FROM job_postings WHERE job_id=?",
                (job.get('job_id'),)
            )
            
            if not cursor.fetchone():
                cursor.execute(
                    """INSERT INTO job_postings 
                    (job_id, title, company, location, job_type, description, 
                    required_skills, company_logo_url, posting_url, source, posted_date, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        job.get('job_id'),
                        job.get('title'),
                        job.get('company'),
                        job.get('location'),
                        job.get('job_type'),
                        job.get('description'),
                        json.dumps(job.get('required_skills', [])),
                        job.get('company_logo_url'),
                        job.get('posting_url'),
                        job.get('source'),
                        datetime.now(),
                        datetime.now()
                    )
                )
                
                # Add to vector database
                VectorService.add_job_embeddings(
                    job.get('job_id'),
                    job.get('description', ''),
                    json.dumps(job.get('required_skills', []))
                )
        
        conn.commit()
        conn.close()
        
        return {
            "total_jobs": len(jobs),
            "jobs": jobs,
            "message": "Jobs fetched successfully"
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/search")
def search_jobs(
    keyword: str = "",
    location: str = "",
    job_type: str = "",
    user=Depends(verify_token)
):
    """Search jobs with filters"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM job_postings WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND (title LIKE ? OR description LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        
        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")
        
        if job_type:
            query += " AND job_type LIKE ?"
            params.append(f"%{job_type}%")
        
        query += " ORDER BY posted_date DESC LIMIT 20"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        jobs = []
        for row in results:
            jobs.append({
                "id": row[0],
                "job_id": row[1],
                "title": row[2],
                "company": row[3],
                "location": row[4],
                "job_type": row[5],
                "description": row[6],
                "required_skills": json.loads(row[7]) if row[7] else [],
                "company_logo_url": row[8],
                "posting_url": row[9],
                "source": row[10]
            })
        
        return {
            "total_jobs": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/recommended")
def get_recommended_jobs(user=Depends(verify_token)):
    """Get job recommendations based on user skills"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get user's skills
        cursor.execute(
            "SELECT skills FROM user_profiles WHERE user_id=?",
            (user['user_id'],)
        )
        result = cursor.fetchone()
        user_skills = json.loads(result[0]) if result and result[0] else []
        
        conn.close()
        
        if not user_skills:
            return {"jobs": [], "message": "No skills found. Please analyze your resume first."}
        
        # Find matching jobs using vector search
        user_skills_str = ", ".join(user_skills)
        matching_jobs = VectorService.find_matching_jobs(user_skills_str, n_results=10)
        
        return {
            "recommended_jobs": len(matching_jobs),
            "jobs": matching_jobs
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/save")
def save_job(job_id: str, user=Depends(verify_token)):
    """Save a job posting for later"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if job exists
        cursor.execute(
            "SELECT id FROM job_postings WHERE job_id=?",
            (job_id,)
        )
        job_result = cursor.fetchone()
        
        if not job_result:
            raise HTTPException(404, "Job not found")
        
        # Check if already saved
        cursor.execute(
            "SELECT id FROM job_notifications WHERE user_id=? AND job_id=?",
            (user['user_id'], job_id)
        )
        
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO job_notifications (user_id, job_id, is_saved) VALUES (?, ?, ?)",
                (user['user_id'], job_id, True)
            )
            conn.commit()
        
        conn.close()
        return {"message": "Job saved successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/saved")
def get_saved_jobs(user=Depends(verify_token)):
    """Get user's saved jobs"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT jp.id, jp.job_id, jp.title, jp.company, jp.location, jp.job_type, 
            jp.description, jp.required_skills, jp.company_logo_url, jp.posting_url
            FROM job_postings jp
            JOIN job_notifications jn ON jp.job_id = jn.job_id
            WHERE jn.user_id=? AND jn.is_saved=1
            ORDER BY jn.created_at DESC""",
            (user['user_id'],)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        jobs = []
        for row in results:
            jobs.append({
                "id": row[0],
                "job_id": row[1],
                "title": row[2],
                "company": row[3],
                "location": row[4],
                "job_type": row[5],
                "description": row[6],
                "required_skills": json.loads(row[7]) if row[7] else [],
                "company_logo_url": row[8],
                "posting_url": row[9]
            })
        
        return {
            "total_saved": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        raise HTTPException(500, str(e))
