"""
Resume routes for analyzing resumes and identifying skill gaps
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Body
from db.sqlite import get_connection
from services.resume_analyzer import ResumeAnalyzer
from services.llm_service import LLMService
from services.vector_service import VectorService
from utils.jwt_handler import verify_token
from models.resume import (
    ResumeUploadResponse,
    RoleMatchingResponse,
    ResumeScoreResponse,
    ScoreBreakdown,
    SkillGapResponse,
    UpskillingResponse,
    InterviewPrepResponse,
    CompleteResumeAnalysisResponse,
    CompleteResumeAnalysisRequest
)
from datetime import datetime
import json
import PyPDF2
from io import BytesIO

router = APIRouter()

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        raise HTTPException(400, "Failed to extract text from PDF")

def extract_text_from_file(file_content: bytes, file_name: str) -> str:
    """Extract text from resume file (PDF or TXT)"""
    if file_name.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_content)
    else:
        # Assume TXT file
        return file_content.decode('utf-8')


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...), user=Depends(verify_token)):
    """Upload and extract resume text
    
    Supports PDF and TXT files. Returns resume_id for use in analysis endpoints.
    """
    try:
        # Read file content
        content = await file.read()
        
        # Extract text from file (PDF or TXT)
        resume_text = extract_text_from_file(content, file.filename)
        
        if not resume_text.strip():
            raise HTTPException(400, "Resume file is empty or cannot be read")
        
        # Save to database
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO resumes 
            (user_id, file_path, file_name, content, uploaded_at)
            VALUES (?, ?, ?, ?, ?)""",
            (
                user['user_id'],
                f"resumes/{user['user_id']}/{file.filename}",
                file.filename,
                resume_text,
                datetime.now()
            )
        )
        
        resume_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return ResumeUploadResponse(
            resume_id=resume_id,
            message="Resume uploaded successfully",
            file_name=file.filename,
            uploaded_at=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error uploading resume: {str(e)}")


@router.post("/role-matching")
async def analyze_role_matching(
    resume_id: int = Body(...),
    job_description: str = Body(...),
    target_role: str = Body(...),
    user=Depends(verify_token)
) -> RoleMatchingResponse:
    """Analyze how well resume matches job description
    
    Compares resume against job description and returns match percentage.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get resume
        cursor.execute(
            "SELECT content FROM resumes WHERE id=? AND user_id=?",
            (resume_id, user['user_id'])
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(404, "Resume not found")
        
        resume_text = result[0]
        
        # Analyze role matching
        analysis = LLMService.analyze_role_matching(
            resume_text=resume_text,
            job_description=job_description,
            target_role=target_role
        )
        
        return RoleMatchingResponse(
            resume_id=resume_id,
            match_percentage=analysis.get('match_percentage', 0),
            target_role=target_role,
            matching_skills=analysis.get('matching_skills', []),
            mismatching_skills=analysis.get('mismatching_skills', []),
            overall_assessment=analysis.get('overall_assessment', '')
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error in role matching analysis: {str(e)}")


@router.post("/resume-score")
async def analyze_resume_score(
    resume_id: int = Body(...),
    job_description: str = Body(None),
    user=Depends(verify_token)
) -> ResumeScoreResponse:
    """Generate ATS-style resume score
    
    Evaluates resume across Technical Skills, Experience, Education, and Achievements.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get resume
        cursor.execute(
            "SELECT content FROM resumes WHERE id=? AND user_id=?",
            (resume_id, user['user_id'])
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(404, "Resume not found")
        
        resume_text = result[0]
        
        # Analyze ATS score
        analysis = LLMService.analyze_ats_score(
            resume_text=resume_text,
            job_description=job_description
        )
        
        return ResumeScoreResponse(
            resume_id=resume_id,
            ats_score=analysis.get('ats_score', 0),
            score_breakdown=ScoreBreakdown(**analysis.get('score_breakdown', {})),
            strengths=analysis.get('strengths', []),
            weaknesses=analysis.get('weaknesses', []),
            ats_keywords_found=analysis.get('ats_keywords_found', []),
            improvement_suggestions=analysis.get('improvement_suggestions', [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error in resume scoring: {str(e)}")


@router.post("/skill-gap")
async def analyze_skill_gap(
    resume_id: int = Body(...),
    job_description: str = Body(...),
    target_role: str = Body(...),
    user=Depends(verify_token)
) -> SkillGapResponse:
    """Analyze skill gaps between resume and job requirements
    
    Identifies missing skills and gap percentage.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get resume
        cursor.execute(
            "SELECT content FROM resumes WHERE id=? AND user_id=?",
            (resume_id, user['user_id'])
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(404, "Resume not found")
        
        resume_text = result[0]
        
        # Analyze skill gaps
        analysis = LLMService.analyze_skill_gap_comprehensive(
            resume_text=resume_text,
            job_description=job_description,
            target_role=target_role
        )
        
        return SkillGapResponse(
            resume_id=resume_id,
            current_skills=analysis.get('current_skills', []),
            required_skills=analysis.get('required_skills', []),
            missing_skills=analysis.get('missing_skills', []),
            skill_gap_count=analysis.get('skill_gap_count', 0),
            gap_percentage=analysis.get('gap_percentage', 0),
            priority_missing_skills=analysis.get('priority_missing_skills', [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error in skill gap analysis: {str(e)}")


@router.post("/upskilling-recommendations")
async def get_upskilling_recommendations(
    resume_id: int = Body(...),
    missing_skills: list = Body(...),
    available_hours_per_week: int = Body(default=10),
    user=Depends(verify_token)
) -> UpskillingResponse:
    """Get upskilling recommendations with learning paths
    
    Generates courses, books, and projects for skill development.
    """
    try:
        if not missing_skills:
            raise HTTPException(400, "Missing skills list is required")
        
        if not (1 <= available_hours_per_week <= 168):
            raise HTTPException(400, "Available hours per week must be between 1 and 168")
        
        # Generate upskilling recommendations
        analysis = LLMService.generate_upskilling_recommendations(
            missing_skills=missing_skills,
            available_hours_per_week=available_hours_per_week
        )
        
        return UpskillingResponse(
            resume_id=resume_id,
            total_recommendations=analysis.get('total_recommendations', 0),
            estimated_total_weeks=analysis.get('estimated_total_weeks', 0),
            upskilling_recommendations=analysis.get('upskilling_recommendations', []),
            priority_roadmap=analysis.get('priority_roadmap', [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error generating upskilling recommendations: {str(e)}")


@router.post("/interview-questions")
async def generate_interview_questions(
    resume_id: int = Body(...),
    job_description: str = Body(...),
    target_role: str = Body(...),
    num_questions: int = Body(default=5),
    user=Depends(verify_token)
) -> InterviewPrepResponse:
    """Generate custom interview questions
    
    Creates behavioral, technical, and situational questions based on resume and role.
    """
    try:
        if not (3 <= num_questions <= 10):
            raise HTTPException(400, "Number of questions must be between 3 and 10")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get resume
        cursor.execute(
            "SELECT content FROM resumes WHERE id=? AND user_id=?",
            (resume_id, user['user_id'])
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(404, "Resume not found")
        
        resume_text = result[0]
        
        # Generate interview questions
        analysis = LLMService.generate_interview_questions(
            resume_text=resume_text,
            job_description=job_description,
            target_role=target_role,
            num_questions=num_questions
        )
        
        return InterviewPrepResponse(
            resume_id=resume_id,
            target_role=target_role,
            num_questions=num_questions,
            interview_questions=analysis.get('interview_questions', []),
            preparation_tips=analysis.get('preparation_tips', []),
            common_questions_for_role=analysis.get('common_questions_for_role', []),
            follow_up_resources=analysis.get('follow_up_resources', [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error generating interview questions: {str(e)}")


@router.post("/complete-analysis")
async def complete_resume_analysis(
    request: CompleteResumeAnalysisRequest,
    user=Depends(verify_token)
) -> CompleteResumeAnalysisResponse:
    """Complete resume analysis covering all 6 stages
    
    Performs role matching, scoring, skill gap, upskilling, and interview prep in one call.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get resume
        cursor.execute(
            "SELECT content FROM resumes WHERE id=? AND user_id=?",
            (request.resume_id, user['user_id'])
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(404, "Resume not found")
        
        resume_text = result[0]
        
        # 1. Role Matching Analysis
        role_match = LLMService.analyze_role_matching(
            resume_text=resume_text,
            job_description=request.job_description,
            target_role=request.target_role
        )
        
        # 2. ATS Score
        score_analysis = LLMService.analyze_ats_score(
            resume_text=resume_text,
            job_description=request.job_description
        )
        
        # 3. Skill Gap Analysis
        skill_gap = LLMService.analyze_skill_gap_comprehensive(
            resume_text=resume_text,
            job_description=request.job_description,
            target_role=request.target_role
        )
        
        # 4. Upskilling Recommendations
        missing_skills = skill_gap.get('missing_skills', [])
        upskilling = LLMService.generate_upskilling_recommendations(
            missing_skills=missing_skills,
            available_hours_per_week=request.available_hours_per_week
        )
        
        # 5. Interview Prep
        interview_prep = LLMService.generate_interview_questions(
            resume_text=resume_text,
            job_description=request.job_description,
            target_role=request.target_role,
            num_questions=request.num_interview_questions
        )
        
        return CompleteResumeAnalysisResponse(
            resume_id=request.resume_id,
            role_matching=RoleMatchingResponse(
                resume_id=request.resume_id,
                match_percentage=role_match.get('match_percentage', 0),
                target_role=request.target_role,
                matching_skills=role_match.get('matching_skills', []),
                mismatching_skills=role_match.get('mismatching_skills', []),
                overall_assessment=role_match.get('overall_assessment', '')
            ),
            resume_score=ResumeScoreResponse(
                resume_id=request.resume_id,
                ats_score=score_analysis.get('ats_score', 0),
                score_breakdown=ScoreBreakdown(**score_analysis.get('score_breakdown', {})),
                strengths=score_analysis.get('strengths', []),
                weaknesses=score_analysis.get('weaknesses', []),
                ats_keywords_found=score_analysis.get('ats_keywords_found', []),
                improvement_suggestions=score_analysis.get('improvement_suggestions', [])
            ),
            skill_gap=SkillGapResponse(
                resume_id=request.resume_id,
                current_skills=skill_gap.get('current_skills', []),
                required_skills=skill_gap.get('required_skills', []),
                missing_skills=missing_skills,
                skill_gap_count=skill_gap.get('skill_gap_count', 0),
                gap_percentage=skill_gap.get('gap_percentage', 0),
                priority_missing_skills=skill_gap.get('priority_missing_skills', [])
            ),
            upskilling=UpskillingResponse(
                resume_id=request.resume_id,
                total_recommendations=upskilling.get('total_recommendations', 0),
                estimated_total_weeks=upskilling.get('estimated_total_weeks', 0),
                upskilling_recommendations=upskilling.get('upskilling_recommendations', []),
                priority_roadmap=upskilling.get('priority_roadmap', [])
            ),
            interview_prep=InterviewPrepResponse(
                resume_id=request.resume_id,
                target_role=request.target_role,
                num_questions=request.num_interview_questions,
                interview_questions=interview_prep.get('interview_questions', []),
                preparation_tips=interview_prep.get('preparation_tips', []),
                common_questions_for_role=interview_prep.get('common_questions_for_role', []),
                follow_up_resources=interview_prep.get('follow_up_resources', [])
            ),
            analysis_timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error in complete analysis: {str(e)}")


@router.get("/analysis/{resume_id}")
def get_resume_analysis(resume_id: int, user=Depends(verify_token)):
    """Get stored resume data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT file_name, content, uploaded_at FROM resumes WHERE id=? AND user_id=?""",
            (resume_id, user['user_id'])
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(404, "Resume not found")
        
        return {
            "resume_id": resume_id,
            "file_name": result[0],
            "content": result[1],
            "uploaded_at": result[2]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error retrieving resume: {str(e)}")


@router.get("/list")
def list_user_resumes(user=Depends(verify_token)):
    """List all resumes uploaded by the user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT id, file_name, uploaded_at FROM resumes WHERE user_id=? ORDER BY uploaded_at DESC""",
            (user['user_id'],)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        resumes = [
            {
                "resume_id": row[0],
                "file_name": row[1],
                "uploaded_at": row[2]
            }
            for row in results
        ]
        
        return {"resumes": resumes}
    except Exception as e:
        raise HTTPException(500, f"Error listing resumes: {str(e)}")


@router.post("/role-suggestions")
async def get_role_suggestions(job_description: str = Body(...)):
    """Generate role suggestions based on job description
    
    Returns list of suitable target roles extracted from job description.
    """
    try:
        prompt = f"""Based on this job description, suggest 5-8 appropriate target role titles for a candidate.
        
JOB DESCRIPTION:
{job_description}

Extract and suggest specific role titles that match this job description. Consider variations and related positions.

Return ONLY valid JSON (no markdown, no extra text):
{{
    "suggested_roles": ["role1", "role2", "role3", "role4", "role5"]
}}"""
        
        import json
        message = LLMService.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
        )
        
        response_text = message.choices[0].message.content.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()
        
        result = json.loads(response_text)
        return {"suggested_roles": result.get("suggested_roles", [])}
    except Exception as e:
        print(f"Error generating role suggestions: {e}")
        return {"suggested_roles": []}


