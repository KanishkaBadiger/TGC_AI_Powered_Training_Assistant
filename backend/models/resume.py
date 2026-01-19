from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- Request Schemas (What the frontend sends) ---

class RoleMatchingRequest(BaseModel):
    resume_id: str
    job_description: str
    target_role: str

class ResumeScoreRequest(BaseModel):
    resume_id: str
    job_description: str

class SkillGapRequest(BaseModel):
    resume_id: str
    job_description: str
    target_role: str

class UpskillingRequest(BaseModel):
    resume_id: str
    missing_skills: List[str]
    available_hours_per_week: int

class InterviewPrepRequest(BaseModel):
    resume_id: str
    job_description: str
    target_role: str
    num_questions: int = 5

# --- Response Schemas (What the frontend expects) ---

class RoleMatchingResponse(BaseModel):
    match_percentage: int
    overall_assessment: str
    target_role: str
    matching_skills: List[str]
    mismatching_skills: List[str]

class ResumeScoreResponse(BaseModel):
    ats_score: int
    score_breakdown: Dict[str, int]  # {'technical_skills': 80, 'experience': 70...}
    strengths: List[str]
    weaknesses: List[str]
    ats_keywords_found: List[str]
    improvement_suggestions: List[str]

class SkillGapResponse(BaseModel):
    current_skills: List[str]
    required_skills: List[str]
    gap_percentage: int
    missing_skills: List[str]
    priority_missing_skills: List[str]
    priority_roadmap: Optional[List[str]] = []

class UpskillingResponse(BaseModel):
    total_recommendations: int
    estimated_total_weeks: int
    upskilling_recommendations: List[Dict[str, Any]]
    priority_roadmap: List[str]

class InterviewPrepResponse(BaseModel):
    interview_questions: List[Dict[str, Any]]
    preparation_tips: List[str]
    common_questions_for_role: List[str]