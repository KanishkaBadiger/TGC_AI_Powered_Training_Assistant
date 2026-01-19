from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from groq import Groq
import os
import json
import uuid
from typing import Dict
from dotenv import load_dotenv
load_dotenv()

# Import your models and utils
from models.resume import (
    RoleMatchingRequest, RoleMatchingResponse,
    ResumeScoreRequest, ResumeScoreResponse,
    SkillGapRequest, SkillGapResponse,
    UpskillingRequest, UpskillingResponse,
    InterviewPrepRequest, InterviewPrepResponse
)
from utils.resume_helper import extract_text_from_file

# Initialize Router and Groq
router = APIRouter(prefix="/api/resume", tags=["Resume Analysis"])

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- TEMPORARY STORAGE (Replace with your DB logic) ---
# Format: { "resume_id_123": "Full text of resume..." }
RESUME_STORAGE: Dict[str, str] = {}

def get_resume_text(resume_id: str):
    """Helper to fetch resume text. Replace with DB call later."""
    if resume_id not in RESUME_STORAGE:
        raise HTTPException(status_code=404, detail="Resume not found")
    return RESUME_STORAGE[resume_id]

# --- 1. UPLOAD RESUME ---
@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text_from_file(file)
    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from file")
    
    # Generate a unique ID and store text
    resume_id = str(uuid.uuid4())
    RESUME_STORAGE[resume_id] = text
    
    return {"resume_id": resume_id, "resume_text": text}

# --- 2. ROLE MATCHING ---
@router.post("/role-matching", response_model=RoleMatchingResponse)
async def role_matching(request: RoleMatchingRequest):
    resume_text = get_resume_text(request.resume_id)
    
    prompt = f"""
    Analyze the resume against the target role and JD.
    Resume: {resume_text[:4000]}
    Role: {request.target_role}
    JD: {request.job_description[:2000]}
    
    Return JSON:
    {{
        "match_percentage": <int>,
        "overall_assessment": "<short summary>",
        "target_role": "{request.target_role}",
        "matching_skills": [<list of matching skills>],
        "mismatching_skills": [<list of missing or weak skills>]
    }}
    """
    
    response = get_groq_response(prompt)
    return response

# --- 3. RESUME SCORE ---
@router.post("/resume-score", response_model=ResumeScoreResponse)
async def resume_score(request: ResumeScoreRequest):
    resume_text = get_resume_text(request.resume_id)
    
    prompt = f"""
    Act as an ATS. Score this resume based on the JD.
    Resume: {resume_text[:4000]}
    JD: {request.job_description[:2000]}
    
    Return JSON:
    {{
        "ats_score": <int 0-100>,
        "score_breakdown": {{
            "technical_skills": <int>,
            "experience": <int>,
            "education": <int>,
            "achievements": <int>
        }},
        "strengths": [<list>],
        "weaknesses": [<list>],
        "ats_keywords_found": [<list>],
        "improvement_suggestions": [<list>]
    }}
    """
    response = get_groq_response(prompt)
    return response

# --- 4. SKILL GAP ---
@router.post("/skill-gap", response_model=SkillGapResponse)
async def skill_gap(request: SkillGapRequest):
    resume_text = get_resume_text(request.resume_id)
    
    prompt = f"""
    Perform a strict Skill Gap Analysis.
    Resume: {resume_text[:4000]}
    Role: {request.target_role}
    JD: {request.job_description[:2000]}
    
    Return JSON:
    {{
        "current_skills": [<skills found in resume>],
        "required_skills": [<skills found in JD>],
        "gap_percentage": <int>,
        "missing_skills": [<skills in JD but not in resume>],
        "priority_missing_skills": [<top 5 critical missing skills>],
        "priority_roadmap": [<ordered list of what to learn first>]
    }}
    """
    response = get_groq_response(prompt)
    return response

# --- 5. UPSKILLING ---
@router.post("/upskilling-recommendations", response_model=UpskillingResponse)
async def upskilling(request: UpskillingRequest):
    # This doesn't strictly need resume text if missing_skills are provided
    skills_to_learn = ", ".join(request.missing_skills)
    
    prompt = f"""
    Create a learning plan for these missing skills: {skills_to_learn}.
    User has {request.available_hours_per_week} hours/week.
    
    Return JSON:
    {{
        "total_recommendations": <int count of skills>,
        "estimated_total_weeks": <int total weeks to learn all>,
        "upskilling_recommendations": [
            {{
                "skill": "<skill name>",
                "estimated_time_weeks": <int>,
                "priority": "High/Medium/Low",
                "learning_path_steps": ["Step 1", "Step 2"],
                "learning_resources": ["Book X", "Course Y"]
            }}
        ],
        "priority_roadmap": ["Week 1-2: Skill A", "Week 3: Skill B"]
    }}
    """
    response = get_groq_response(prompt)
    return response

# --- 6. INTERVIEW PREP ---
@router.post("/interview-questions", response_model=InterviewPrepResponse)
async def interview_prep(request: InterviewPrepRequest):
    resume_text = get_resume_text(request.resume_id)
    
    prompt = f"""
    Generate {request.num_questions} interview questions for a {request.target_role}.
    Based on Resume: {resume_text[:3000]}
    And JD: {request.job_description[:2000]}
    
    Return JSON:
    {{
        "interview_questions": [
            {{
                "question": "<question text>",
                "question_type": "Technical/Behavioral/Situational",
                "difficulty": "Easy/Medium/Hard",
                "related_skill": "<skill name>",
                "answer_tips": ["Tip 1", "Tip 2"],
                "sample_answer": "<short sample>",
                "key_points_to_cover": ["Point A", "Point B"]
            }}
        ],
        "preparation_tips": ["General tip 1", "General tip 2"],
        "common_questions_for_role": ["Common Q1", "Common Q2"]
    }}
    """
    response = get_groq_response(prompt)
    return response

# --- HELPER FOR GROQ ---
def get_groq_response(prompt_text: str):
    """Sends prompt to Groq and parses JSON"""
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a specialized AI Resume Assistant. Output ONLY valid JSON."},
                {"role": "user", "content": prompt_text}
            ],
            # model="llama3-70b-8192",
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Groq Error: {e}")
        raise HTTPException(status_code=500, detail=f"AI Processing Failed: {str(e)}")
