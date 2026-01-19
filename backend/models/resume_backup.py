"""
Resume Analyzer Pydantic Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ==================== Upload Resume Stage ====================
class ResumeUploadRequest(BaseModel):
    """Request model for resume upload"""
    file_name: str = Field(..., description="Name of the resume file")
    file_content: str = Field(..., description="Text content extracted from resume")


class ResumeUploadResponse(BaseModel):
    """Response model for resume upload"""
    resume_id: int
    message: str
    file_name: str
    uploaded_at: datetime


# ==================== Role Matching Stage ====================
class RoleMatchingRequest(BaseModel):
    """Request model for role matching analysis"""
    resume_id: int = Field(..., description="ID of the uploaded resume")
    job_description: str = Field(..., description="Job description text")
    target_role: str = Field(..., description="Target job role")


class RoleMatchingResponse(BaseModel):
    """Response model for role matching"""
    resume_id: int
    match_percentage: int = Field(..., ge=0, le=100, description="Percentage match 0-100")
    target_role: str
    matching_skills: List[str]
    mismatching_skills: List[str]
    overall_assessment: str


# ==================== Resume Score Stage ====================
class ScoreBreakdown(BaseModel):
    """Breakdown of resume scores by category"""
    technical_skills: int = Field(..., ge=0, le=100, description="Technical skills score")
    experience: int = Field(..., ge=0, le=100, description="Experience score")
    education: int = Field(..., ge=0, le=100, description="Education score")
    achievements: int = Field(..., ge=0, le=100, description="Achievements score")


class ResumeScoreRequest(BaseModel):
    """Request model for ATS-style resume scoring"""
    resume_id: int = Field(..., description="ID of the uploaded resume")
    job_description: Optional[str] = Field(None, description="Job description for context")


class ResumeScoreResponse(BaseModel):
    """Response model for ATS resume scoring"""
    resume_id: int
    ats_score: int = Field(..., ge=0, le=100, description="Overall ATS score 0-100")
    score_breakdown: ScoreBreakdown
    strengths: List[str]
    weaknesses: List[str]
    ats_keywords_found: List[str]
    improvement_suggestions: List[str]


# ==================== Skill Gap Stage ====================
class SkillGapRequest(BaseModel):
    """Request model for skill gap analysis"""
    resume_id: int = Field(..., description="ID of the uploaded resume")
    job_description: Optional[str] = Field(None, description="Job description for comparison")
    target_role: Optional[str] = Field(None, description="Target role for comparison")


class SkillGapResponse(BaseModel):
    """Response model for skill gap analysis"""
    resume_id: int
    current_skills: List[str]
    required_skills: List[str]
    missing_skills: List[str]
    skill_gap_count: int
    gap_percentage: float = Field(..., ge=0, le=100, description="Percentage of skills missing")
    priority_missing_skills: List[str]


# ==================== Upskilling Stage ====================
class LearningResource(BaseModel):
    """A learning resource recommendation"""
    title: str = Field(..., description="Title of the resource")
    type: str = Field(..., description="Type: book, course, platform, project")
    platform: Optional[str] = Field(None, description="Platform (Coursera, Udemy, etc.)")
    duration_weeks: Optional[int] = Field(None, description="Estimated duration in weeks")
    difficulty: str = Field(..., description="Difficulty level: beginner, intermediate, advanced")
    url: Optional[str] = Field(None, description="URL to the resource")
    reason: str = Field(..., description="Why this resource is recommended")


class UpskillRecommendation(BaseModel):
    """Upskilling recommendation for a skill"""
    skill: str = Field(..., description="Skill to learn")
    priority: str = Field(..., description="Priority: high, medium, low")
    estimated_time_weeks: int = Field(..., ge=1, description="Estimated learning time in weeks")
    learning_resources: List[LearningResource]
    learning_path_steps: List[str]


class UpskillingRequest(BaseModel):
    """Request model for upskilling recommendations"""
    resume_id: int = Field(..., description="ID of the uploaded resume")
    missing_skills: List[str] = Field(..., description="List of missing skills")
    available_hours_per_week: int = Field(default=10, ge=1, le=168, description="Hours available per week")


class UpskillingResponse(BaseModel):
    """Response model for upskilling recommendations"""
    resume_id: int
    total_recommendations: int
    estimated_total_weeks: int
    upskilling_recommendations: List[UpskillRecommendation]
    priority_roadmap: List[str]


# ==================== Interview Prep Stage ====================
class InterviewQuestion(BaseModel):
    """An interview question with preparation tips"""
    question: str = Field(..., description="The interview question")
    question_type: str = Field(..., description="Type: behavioral, technical, situational")
    difficulty: str = Field(..., description="Difficulty: easy, medium, hard")
    answer_tips: List[str]
    sample_answer: Optional[str] = Field(None, description="Sample answer structure")
    key_points_to_cover: List[str]
    related_skill: Optional[str] = Field(None, description="Related skill from resume")


class InterviewPrepRequest(BaseModel):
    """Request model for interview preparation"""
    resume_id: int = Field(..., description="ID of the uploaded resume")
    job_description: str = Field(..., description="Job description for context")
    target_role: str = Field(..., description="Target job role")
    num_questions: int = Field(default=5, ge=3, le=10, description="Number of questions to generate")


class InterviewPrepResponse(BaseModel):
    """Response model for interview preparation"""
    resume_id: int
    target_role: str
    num_questions: int
    interview_questions: List[InterviewQuestion]
    preparation_tips: List[str]
    common_questions_for_role: List[str]
    follow_up_resources: List[str]


# ==================== Complete Analysis (Combined) ====================
class CompleteResumeAnalysisRequest(BaseModel):
    """Request model for complete resume analysis"""
    resume_id: int = Field(..., description="ID of the uploaded resume")
    job_description: str = Field(..., description="Job description for all analyses")
    target_role: str = Field(..., description="Target job role")
    available_hours_per_week: int = Field(default=10, ge=1, le=168)
    num_interview_questions: int = Field(default=5, ge=3, le=10)


class CompleteResumeAnalysisResponse(BaseModel):
    """Response model containing all analysis stages"""
    resume_id: int
    role_matching: RoleMatchingResponse
    resume_score: ResumeScoreResponse
    skill_gap: SkillGapResponse
    upskilling: UpskillingResponse
    interview_prep: InterviewPrepResponse
    analysis_timestamp: datetime


# ==================== Resume Storage Model ====================
class ResumeStorageModel(BaseModel):
    """Model for storing resume data"""
    id: Optional[int] = None
    user_id: int
    file_name: str
    file_content: str
    uploaded_at: datetime
    analyzed_at: Optional[datetime] = None
    match_percentage: Optional[int] = None
    ats_score: Optional[int] = None
    job_description_analyzed: Optional[str] = None
    analysis_results: Optional[Dict[str, Any]] = None


class ResumeAnalysisMetadata(BaseModel):
    """Metadata for stored analyses"""
    resume_id: int
    user_id: int
    job_description: str
    target_role: str
    analysis_stage: str  # "role_matching", "scoring", "skill_gap", "upskilling", "interview"
    results: Dict[str, Any]
    created_at: datetime
