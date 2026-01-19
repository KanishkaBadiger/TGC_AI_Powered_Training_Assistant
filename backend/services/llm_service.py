"""
LLM Service using Groq API and Ollama for AI-powered features
"""
import os
import json
from groq import Groq
from typing import Optional, Dict, Any, List

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

class LLMService:
    """Service for interacting with LLM models via Groq"""
    
    @staticmethod
    def generate_quiz_questions(
        category: str,
        subcategory: str,
        difficulty: str = "medium",
        num_questions: int = 5,
        question_type: str = "mcq"
    ) -> List[Dict[str, Any]]:
        """
        Generate quiz questions using LLM
        
        Args:
            category: Category of questions (aptitude, technical, core)
            subcategory: Specific topic within category
            difficulty: Difficulty level (easy, medium, hard)
            num_questions: Number of questions to generate
            question_type: Type of question (mcq, descriptive, code)
        
        Returns:
            List of generated questions with options and answers
        """
        
        prompt = f"""Generate {num_questions} {question_type} questions for {category} - {subcategory} at {difficulty} difficulty level.
        
For MCQ questions, format each question as JSON:
{{
    "question": "Question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Explanation of why this is correct",
    "difficulty": "{difficulty}",
    "category": "{category}",
    "subcategory": "{subcategory}"
}}

Generate ONLY valid JSON array, no additional text."""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            
            response_text = message.choices[0].message.content
            # Parse JSON response
            questions = json.loads(response_text)
            return questions if isinstance(questions, list) else [questions]
        except Exception as e:
            print(f"Error generating questions: {e}")
            return []
    
    @staticmethod
    def analyze_resume(resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume content and extract skills, experience, education
        
        Args:
            resume_text: Raw resume text content
        
        Returns:
            Dictionary with extracted information
        """
        
        prompt = f"""Analyze this resume and extract the following information in JSON format:
{{
    "skills": [],
    "experience_years": 0,
    "education": [],
    "certifications": [],
    "projects": [],
    "languages": [],
    "summary": ""
}}

Resume:
{resume_text}

Return ONLY the JSON response, no additional text."""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000,
            )
            
            response_text = message.choices[0].message.content
            analysis = json.loads(response_text)
            return analysis
        except Exception as e:
            print(f"Error analyzing resume: {e}")
            return {}
    
    @staticmethod
    def find_skill_gaps(current_skills: List[str], target_role: str) -> Dict[str, Any]:
        """
        Identify skill gaps for a target role
        
        Args:
            current_skills: List of current skills
            target_role: Target job position
        
        Returns:
            Dictionary with skill gap analysis and recommendations
        """
        
        prompt = f"""Given these current skills: {', '.join(current_skills)}
        
And a target role: {target_role}

Provide a JSON response with:
{{
    "required_skills": [],
    "missing_skills": [],
    "skill_match_percentage": 0,
    "priority_skills": [],
    "learning_resources": [],
    "estimated_learning_time_weeks": 0,
    "recommendations": []
}}

Return ONLY the JSON response."""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000,
            )
            
            response_text = message.choices[0].message.content
            analysis = json.loads(response_text)
            return analysis
        except Exception as e:
            print(f"Error analyzing skill gaps: {e}")
            return {}
    
    @staticmethod
    def generate_personalized_roadmap(
        current_role: str,
        target_role: str,
        available_hours_per_week: int
    ) -> Dict[str, Any]:
        """
        Generate a personalized learning roadmap
        
        Args:
            current_role: Current job role
            target_role: Target job role
            available_hours_per_week: Hours available for learning per week
        
        Returns:
            Structured roadmap with milestones
        """
        
        prompt = f"""Create a detailed learning roadmap in JSON format for transitioning from {current_role} to {target_role} with {available_hours_per_week} hours per week.

{{
    "title": "Roadmap Title",
    "duration_months": 0,
    "modules": [
        {{
            "module_name": "",
            "duration_weeks": 0,
            "topics": [],
            "resources": [],
            "milestone": ""
        }}
    ],
    "timeline": [
        {{
            "month": 1,
            "goals": [],
            "milestones": []
        }}
    ],
    "resources": {{
        "courses": [],
        "books": [],
        "projects": [],
        "practice_platforms": []
    }}
}}

Return ONLY the JSON response."""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000,
            )
            
            response_text = message.choices[0].message.content
            roadmap = json.loads(response_text)
            return roadmap
        except Exception as e:
            print(f"Error generating roadmap: {e}")
            return {}
    
    @staticmethod
    def generate_explanation(topic: str, explanation_level: str = "intermediate") -> str:
        """
        Generate detailed explanation for a topic
        
        Args:
            topic: Topic to explain
            explanation_level: beginner, intermediate, advanced
        
        Returns:
            Detailed explanation text
        """
        
        prompt = f"""Provide a {explanation_level} level explanation of: {topic}
Include:
- Key concepts
- Examples
- Common mistakes
- Tips for learning

Keep it concise but comprehensive."""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            
            return message.choices[0].message.content
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return ""
    
    # ==================== COMPREHENSIVE RESUME ANALYSIS ====================
    
    @staticmethod
    def analyze_role_matching(resume_text: str, job_description: str, target_role: str) -> Dict[str, Any]:
        """
        Analyze how well resume matches a job description
        
        Args:
            resume_text: Full resume text
            job_description: Job description text
            target_role: Target role name
        
        Returns:
            Role matching analysis with percentage and skills
        """
        
        prompt = f"""You are an expert recruiter analyzing a SPECIFIC candidate's resume.

CRITICAL - ANTI-HALLUCINATION RULES:
1. ONLY list skills that are WORD-FOR-WORD or DIRECTLY MENTIONED in the resume below.
2. Do NOT infer or assume any skills. Do NOT add similar or related skills.
3. Do NOT mention anything the candidate MIGHT know - ONLY what they explicitly stated.
4. Cross-reference: For each skill listed, it must appear verbatim in the resume text.
5. If a skill is not explicitly mentioned, it goes in MISSING skills.

RESUME TEXT:
---
{resume_text}
---

JOB DESCRIPTION:
---
{job_description}
---

TARGET ROLE: {target_role}

ANALYSIS TASK:
1. Extract ALL technical skills mentioned in the resume
2. Extract ALL required skills from the job description
3. Compare: Which resume skills match job requirements?
4. Which job requirements are MISSING from resume?
5. Calculate match % as: (matching skills count / total required skills) * 100

STRICT OUTPUT FORMAT - JSON ONLY:
{{
    "match_percentage": <integer 0-100>,
    "matching_skills": ["skill1 from resume", "skill2 from resume"],
    "mismatching_skills": ["required skill not in resume", "another missing skill"],
    "overall_assessment": "One sentence based on actual resume content only"
}}

Remember: ONLY include skills that appear in the resume. Be conservative and precise."""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000,
            )
            
            response_text = message.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            return analysis
        except Exception as e:
            print(f"Error in role matching analysis: {e}")
            return {
                "match_percentage": 0,
                "matching_skills": [],
                "mismatching_skills": [],
                "overall_assessment": "Error in analysis"
            }
    
    @staticmethod
    def analyze_ats_score(resume_text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate ATS-style resume score with category breakdowns
        
        Args:
            resume_text: Full resume text
            job_description: Optional job description for context
        
        Returns:
            ATS score with breakdown by categories
        """
        
        jd_context = f"\n\nJOB DESCRIPTION (for context):\n{job_description}" if job_description else ""
        
        prompt = f"""You are an ATS (Applicant Tracking System) analyzer. Score this SPECIFIC resume based ONLY on what is explicitly written.

CRITICAL - ANTI-HALLUCINATION RULES:
1. ONLY count skills, experience, and achievements that are clearly WRITTEN in the resume.
2. Do NOT infer or assume qualifications. Do NOT add similar/related skills.
3. Do NOT reward what the candidate MIGHT have - ONLY what they state.
4. For each item in strengths/keywords, cite where it appears in the resume.
5. Be CONSERVATIVE in scoring - better to underrate than overrate.
        
RESUME TEXT:
---
{resume_text}
---
{jd_context}

SCORING INSTRUCTIONS:
1. Technical Skills: Points only for skills explicitly mentioned (Python, Java, etc.)
2. Experience: Points based on years and stated roles/achievements
3. Education: Points only for degrees/certifications explicitly listed
4. Achievements: Points only for quantified/measurable results stated in resume

OUTPUT FORMAT - JSON ONLY:
{{
    "ats_score": <conservative overall score 0-100>,
    "score_breakdown": {{
        "technical_skills": <0-100 based on skills listed>,
        "experience": <0-100 based on years and roles>,
        "education": <0-100 based on degrees listed>,
        "achievements": <0-100 based on quantified results>
    }},
    "strengths": ["strength1 with evidence from resume", "strength2 from resume"],
    "weaknesses": ["gap1 not mentioned in resume", "gap2 not mentioned in resume"],
    "ats_keywords_found": ["keyword1 found verbatim in resume", "keyword2 found"],
    "improvement_suggestions": ["specific gap to address based on missing items"]
}}

REMEMBER: Score conservatively based on actual resume content only."""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500,
            )
            
            response_text = message.choices[0].message.content.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            return analysis
        except Exception as e:
            print(f"Error in ATS score analysis: {e}")
            return {
                "ats_score": 0,
                "score_breakdown": {
                    "technical_skills": 0,
                    "experience": 0,
                    "education": 0,
                    "achievements": 0
                },
                "strengths": [],
                "weaknesses": [],
                "ats_keywords_found": [],
                "improvement_suggestions": []
            }
    
    @staticmethod
    def analyze_skill_gap_comprehensive(
        resume_text: str,
        job_description: str,
        target_role: str
    ) -> Dict[str, Any]:
        """
        Comprehensive skill gap analysis
        
        Args:
            resume_text: Full resume text
            job_description: Job description text
            target_role: Target role
        
        Returns:
            Detailed skill gap analysis
        """
        
        prompt = f"""You are a career development expert. Analyze skill gaps between THIS SPECIFIC RESUME and job requirements.

CRITICAL - ANTI-HALLUCINATION RULES:
1. current_skills: ONLY skills explicitly written in the resume below. NO inference.
2. required_skills: Extract ONLY from the job description provided.
3. missing_skills: Calculated as required skills NOT in current resume skills.
4. Do NOT add inferred skills. Do NOT assume hidden qualifications.
5. For each skill, verify it appears verbatim in the resume or job description.
        
RESUME TEXT:
---
{resume_text}
---

JOB DESCRIPTION:
---
{job_description}
---

TARGET ROLE: {target_role}

ANALYSIS STEPS:
1. Extract all technical skills explicitly mentioned in the resume
2. Extract all technical skills required in the job description
3. Calculate missing skills = required skills NOT in current resume
4. Rank missing skills by importance based on job description

OUTPUT FORMAT - JSON ONLY:
{{
    "current_skills": ["skill1 verbatim from resume", "skill2 from resume"],
    "required_skills": ["req_skill1 verbatim from JD", "req_skill2 from JD"],
    "missing_skills": ["gap1 required but not in resume", "gap2 required but missing"],
    "skill_gap_count": <number of gaps>,
    "gap_percentage": <(missing_skills/required_skills)*100>,
    "priority_missing_skills": ["most critical to learn", "next priority", "optional"]
}}

IMPORTANT: Do NOT fabricate skills. Be factual and conservative."""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1200,
            )
            
            response_text = message.choices[0].message.content.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            return analysis
        except Exception as e:
            print(f"Error in skill gap analysis: {e}")
            return {
                "current_skills": [],
                "required_skills": [],
                "missing_skills": [],
                "skill_gap_count": 0,
                "gap_percentage": 0,
                "priority_missing_skills": []
            }
    
    @staticmethod
    def generate_upskilling_recommendations(
        missing_skills: List[str],
        available_hours_per_week: int = 10
    ) -> Dict[str, Any]:
        """
        Generate detailed upskilling recommendations with learning paths
        
        Args:
            missing_skills: List of skills to learn
            available_hours_per_week: Hours available for learning per week
        
        Returns:
            Upskilling recommendations with resources
        """
        
        skills_str = ", ".join(missing_skills)
        
        prompt = f"""You are an educational advisor. Create learning path recommendations for THESE SPECIFIC skills: {skills_str}
        
IMPORTANT INSTRUCTIONS:
- ONLY create recommendations for the skills listed above. Do NOT add other skills.
- Focus on real, practical learning resources.
- Estimates should be realistic based on available hours: {available_hours_per_week} hours/week
- Prioritize based on difficulty and prerequisites.
- Verify resources are real and accessible.

The learner has {available_hours_per_week} hours per week available.

For each skill listed above, provide realistic learning resources and timeline:

Return ONLY valid JSON (no markdown, no extra text):
{{
    "total_recommendations": <number of skills listed above>,
    "estimated_total_weeks": <realistic estimate based on {available_hours_per_week}h/week>,
    "upskilling_recommendations": [
        {{
            "skill": "skill_name (from list above)",
            "priority": "high|medium|low",
            "estimated_time_weeks": <realistic weeks needed>,
            "learning_resources": [
                {{
                    "title": "real resource title",
                    "type": "book|course|platform|project",
                    "platform": "Coursera|Udemy|LinkedIn|etc",
                    "duration_weeks": <weeks to complete>,
                    "difficulty": "beginner|intermediate|advanced",
                    "url": "https://real.url.here",
                    "reason": "why this helps learn the skill"
                }}
            ],
            "learning_path_steps": ["step1", "step2", "step3"]
        }}
    ],
    "priority_roadmap": ["skill1 prerequisites -> skill1", "skill2 -> skill3"]
}}"""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=3000,
            )
            
            response_text = message.choices[0].message.content.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            return analysis
        except Exception as e:
            print(f"Error generating upskilling recommendations: {e}")
            return {
                "total_recommendations": 0,
                "estimated_total_weeks": 0,
                "upskilling_recommendations": [],
                "priority_roadmap": []
            }
    
    @staticmethod
    def generate_interview_questions(
        resume_text: str,
        job_description: str,
        target_role: str,
        num_questions: int = 5
    ) -> Dict[str, Any]:
        """
        Generate custom interview questions based on resume and job description
        
        Args:
            resume_text: Full resume text
            job_description: Job description text
            target_role: Target role
            num_questions: Number of questions to generate (3-10)
        
        Returns:
            Interview questions with preparation tips
        """
        
        prompt = f"""You are an expert interviewer. Generate interview questions tailored to THIS SPECIFIC CANDIDATE.

CRITICAL - ANTI-HALLUCINATION RULES:
1. ONLY ask questions answerable from the resume provided below.
2. Reference SPECIFIC projects, technologies, or experiences they actually mention.
3. Do NOT assume skills or experience not explicitly stated in their resume.
4. Do NOT ask about industries/technologies they haven't mentioned.
5. Sample answers must be answerable from their actual background.
6. Tips must help them leverage their genuine experience, NOT fabricated skills.

RESUME TEXT:
---
{resume_text}
---

JOB DESCRIPTION:
---
{job_description}
---

TARGET ROLE: {target_role}

QUESTION GENERATION:
Generate {num_questions} interview questions tailored to this candidate's actual background.
- Mix: behavioral (past projects), technical (job requirements), situational (role scenarios)
- Each question must reference something in their resume
- Sample answers must use only their actual experience
- Tips must help them highlight real strengths

OUTPUT FORMAT - JSON ONLY:
{{
    "interview_questions": [
        {{
            "question": "specific question referencing their actual background",
            "question_type": "behavioral|technical|situational",
            "difficulty": "easy|medium|hard",
            "answer_tips": ["tip specific to their resume", "how to use their experience"],
            "sample_answer": "answer structure using only their stated experience",
            "key_points_to_cover": ["point1 they actually have", "point2 job requires"],
            "related_skill": "skill_they_mentioned_in_resume"
        }}
    ],
    "preparation_tips": ["tip based on their resume", "role-specific preparation"],
    "common_questions_for_role": ["q1 typical for {target_role}", "q2 typical for role"],
    "follow_up_resources": ["resource1", "resource2"]
}}

REMEMBER: All questions and tips must be grounded in their actual resume content."""

        try:
            message = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=3000,
            )
            
            response_text = message.choices[0].message.content.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            return analysis
        except Exception as e:
            print(f"Error generating interview questions: {e}")
            return {
                "interview_questions": [],
                "preparation_tips": [],
                "common_questions_for_role": [],
                "follow_up_resources": []
            }
