"""
Resume Analyzer Service - Extract and analyze resume information
"""
from typing import Dict, Any, List
import re
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from llm_service import LLMService
from vector_service import VectorService

class ResumeAnalyzer:
    """Service for analyzing resumes and extracting information"""
    
    @staticmethod
    def parse_resume(resume_text: str) -> Dict[str, Any]:
        """
        Parse resume and extract structured information
        
        Args:
            resume_text: Raw resume text
        
        Returns:
            Structured resume data
        """
        # Use LLM to analyze resume
        analysis = LLMService.analyze_resume(resume_text)
        
        if not analysis:
            # Fallback to rule-based parsing
            analysis = ResumeAnalyzer._rule_based_parse(resume_text)
        
        return analysis
    
    @staticmethod
    def _rule_based_parse(resume_text: str) -> Dict[str, Any]:
        """
        Rule-based resume parsing as fallback
        
        Args:
            resume_text: Raw resume text
        
        Returns:
            Parsed resume data
        """
        
        # Extract skills using common patterns
        skills = ResumeAnalyzer._extract_skills(resume_text)
        
        # Extract education
        education = ResumeAnalyzer._extract_education(resume_text)
        
        # Extract experience years
        experience_years = ResumeAnalyzer._extract_experience_years(resume_text)
        
        return {
            "skills": skills,
            "experience_years": experience_years,
            "education": education,
            "certifications": ResumeAnalyzer._extract_certifications(resume_text),
            "projects": [],
            "languages": ResumeAnalyzer._extract_languages(resume_text),
            "summary": resume_text[:500]  # First 500 chars as summary
        }
    
    @staticmethod
    def _extract_skills(resume_text: str) -> List[str]:
        """Extract skills from resume text"""
        
        common_skills = [
            'Python', 'Java', 'C++', 'JavaScript', 'TypeScript', 'C#', 'Go', 'Rust', 'PHP', 'Ruby',
            'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Elasticsearch',
            'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring', 'Express',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform',
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn',
            'Data Analysis', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn',
            'Git', 'GitHub', 'GitLab', 'Jira', 'Confluence',
            'REST API', 'GraphQL', 'Microservices', 'SOLID', 'Design Patterns',
            'Agile', 'Scrum', 'Kanban',
            'HTML', 'CSS', 'Bootstrap', 'Tailwind',
            'Linux', 'Windows', 'macOS',
            'Problem Solving', 'Leadership', 'Communication', 'Team Collaboration'
        ]
        
        found_skills = []
        resume_lower = resume_text.lower()
        
        for skill in common_skills:
            if skill.lower() in resume_lower:
                found_skills.append(skill)
        
        return found_skills
    
    @staticmethod
    def _extract_education(resume_text: str) -> List[Dict[str, str]]:
        """Extract education details"""
        
        education_patterns = [
            r'(?:B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|Ph\.?D\.?|B\.?Tech|M\.?Tech|MBA|BCA|MCA)\s+(?:in|of|from)?\s+([A-Za-z\s]+)',
            r'(?:Bachelor|Master|PhD|Diploma)\s+(?:in|of)?\s+([A-Za-z\s]+)',
        ]
        
        education = []
        for pattern in education_patterns:
            matches = re.finditer(pattern, resume_text, re.IGNORECASE)
            for match in matches:
                if match.group(0) not in [e.get('degree', '') for e in education]:
                    education.append({
                        'degree': match.group(0),
                        'field': match.group(1) if len(match.groups()) > 0 else ''
                    })
        
        return education
    
    @staticmethod
    def _extract_experience_years(resume_text: str) -> int:
        """Extract years of experience"""
        
        # Look for patterns like "5 years", "5+ years", "5-7 years"
        patterns = [
            r'(\d+)\s*\+?\s*years?\s+(?:of\s+)?experience',
            r'(?:experience|experience:)\s*(\d+)\s*\+?\s*years?',
        ]
        
        years = []
        for pattern in patterns:
            matches = re.finditer(pattern, resume_text, re.IGNORECASE)
            for match in matches:
                try:
                    years.append(int(match.group(1)))
                except:
                    pass
        
        return max(years) if years else 0
    
    @staticmethod
    def _extract_certifications(resume_text: str) -> List[str]:
        """Extract certifications"""
        
        certifications = []
        cert_keywords = [
            'AWS', 'Azure', 'GCP', 'Kubernetes', 'Docker',
            'AWS Solutions Architect', 'AWS Developer', 'AWS SysOps',
            'Azure Administrator', 'Azure Developer', 'Azure Solutions Architect',
            'Certified Scrum Master', 'Certified Scrum Product Owner',
            'CISSP', 'CEH', 'OSCP',
            'PMP', 'PRINCE2',
            'Oracle', 'Microsoft', 'CompTIA', 'Cisco'
        ]
        
        for cert in cert_keywords:
            if cert.lower() in resume_text.lower():
                certifications.append(cert)
        
        return certifications
    
    @staticmethod
    def _extract_languages(resume_text: str) -> List[str]:
        """Extract programming languages and natural languages"""
        
        languages = set()
        
        # Programming languages
        prog_langs = ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'Go', 'Rust', 'PHP', 'Ruby', 'Swift', 'Kotlin']
        for lang in prog_langs:
            if lang in resume_text:
                languages.add(lang)
        
        # Natural languages
        nat_langs = ['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Hindi']
        for lang in nat_langs:
            if lang in resume_text:
                languages.add(lang)
        
        return list(languages)
    
    @staticmethod
    def analyze_skill_gaps(
        current_skills: List[str],
        target_role: str,
        user_id: int = None
    ) -> Dict[str, Any]:
        """
        Analyze skill gaps for a target role
        
        Args:
            current_skills: List of current skills
            target_role: Target job role
            user_id: User ID for saving analysis
        
        Returns:
            Skill gap analysis
        """
        
        analysis = LLMService.find_skill_gaps(current_skills, target_role)
        
        if not analysis:
            analysis = {
                "required_skills": [],
                "missing_skills": [],
                "skill_match_percentage": 0,
                "priority_skills": [],
                "learning_resources": [],
                "estimated_learning_time_weeks": 0,
                "recommendations": []
            }
        
        # Add match percentage calculation
        if analysis.get('required_skills'):
            matching_skills = set(current_skills) & set(analysis['required_skills'])
            analysis['skill_match_percentage'] = (len(matching_skills) / len(analysis['required_skills'])) * 100
            analysis['missing_skills'] = [s for s in analysis['required_skills'] if s not in current_skills]
        
        return analysis
    
    @staticmethod
    def generate_skill_development_plan(
        current_skills: List[str],
        target_skills: List[str],
        available_hours_per_week: int = 10
    ) -> Dict[str, Any]:
        """
        Generate a skill development plan
        
        Args:
            current_skills: Current skills
            target_skills: Skills to develop
            available_hours_per_week: Hours available for learning
        
        Returns:
            Development plan with timeline
        """
        
        missing_skills = [s for s in target_skills if s not in current_skills]
        
        if not missing_skills:
            return {
                "status": "complete",
                "message": "You already have all required skills!",
                "timeline": []
            }
        
        # Estimate learning time (rough estimate)
        skill_difficulty = {
            'easy': 2,      # weeks
            'medium': 4,    # weeks
            'hard': 8       # weeks
        }
        
        plan = {
            "total_skills_to_learn": len(missing_skills),
            "estimated_total_weeks": 0,
            "weekly_hours_required": available_hours_per_week,
            "skills_plan": [],
            "timeline": []
        }
        
        # Group skills by difficulty
        easy_skills = missing_skills[:len(missing_skills)//3]
        medium_skills = missing_skills[len(missing_skills)//3:2*len(missing_skills)//3]
        hard_skills = missing_skills[2*len(missing_skills)//3:]
        
        week = 1
        for skill in easy_skills:
            plan['skills_plan'].append({
                'skill': skill,
                'difficulty': 'easy',
                'weeks': skill_difficulty['easy'],
                'start_week': week,
                'end_week': week + skill_difficulty['easy'] - 1,
                'resources': [f"Learn {skill} online", "Practice projects"]
            })
            week += skill_difficulty['easy']
        
        for skill in medium_skills:
            plan['skills_plan'].append({
                'skill': skill,
                'difficulty': 'medium',
                'weeks': skill_difficulty['medium'],
                'start_week': week,
                'end_week': week + skill_difficulty['medium'] - 1,
                'resources': [f"Advanced {skill} course", "Real-world projects"]
            })
            week += skill_difficulty['medium']
        
        for skill in hard_skills:
            plan['skills_plan'].append({
                'skill': skill,
                'difficulty': 'hard',
                'weeks': skill_difficulty['hard'],
                'start_week': week,
                'end_week': week + skill_difficulty['hard'] - 1,
                'resources': [f"Master {skill}", "Build portfolio projects"]
            })
            week += skill_difficulty['hard']
        
        plan['estimated_total_weeks'] = week - 1
        
        return plan
