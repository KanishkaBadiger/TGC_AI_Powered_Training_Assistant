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
