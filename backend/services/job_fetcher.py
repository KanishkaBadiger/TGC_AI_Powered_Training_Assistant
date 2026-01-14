"""
Job Fetcher Service - Fetch job/internship postings from various sources
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import json
from datetime import datetime
import os

class JobFetcher:
    """Service for fetching job and internship postings"""
    
    # Using free job APIs and web scraping
    
    @staticmethod
    def fetch_from_api() -> List[Dict[str, Any]]:
        """
        Fetch jobs from public APIs
        
        Returns:
            List of job postings
        """
        jobs = []
        
        try:
            # Using JSearch API (free tier) or similar
            api_key = os.getenv("JSEARCH_API_KEY", "")
            if api_key:
                headers = {
                    'X-API-KEY': api_key,
                    'Content-Type': 'application/json'
                }
                
                params = {
                    'query': 'Software Engineer Internship',
                    'page': 1,
                    'num_pages': 1
                }
                
                response = requests.get(
                    'https://jsearch.p.rapidapi.com/search',
                    headers=headers,
                    params=params,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for job in data.get('data', []):
                        jobs.append({
                            'job_id': job.get('job_id', ''),
                            'title': job.get('job_title', ''),
                            'company': job.get('employer_name', ''),
                            'location': job.get('job_location', ''),
                            'job_type': job.get('job_employment_type', ''),
                            'description': job.get('job_description', ''),
                            'required_skills': job.get('job_required_skills', []),
                            'company_logo_url': job.get('employer_logo', ''),
                            'posting_url': job.get('job_apply_link', ''),
                            'source': 'JSearch API',
                            'salary_range': job.get('job_salary_currency', '')
                        })
        except Exception as e:
            print(f"Error fetching from API: {e}")
        
        return jobs
    
    @staticmethod
    def fetch_internship_postings() -> List[Dict[str, Any]]:
        """
        Fetch internship postings from various sources
        
        Returns:
            List of internship opportunities
        """
        jobs = []
        
        # Using simulated internship postings for demo
        # In production, integrate with actual APIs
        sample_internships = [
            {
                'job_id': 'int_001',
                'title': 'Software Engineering Intern',
                'company': 'Google',
                'location': 'Mountain View, CA',
                'job_type': 'Internship',
                'description': 'Join Google as a Software Engineering Intern...',
                'required_skills': ['Python', 'Java', 'C++', 'DSA'],
                'company_logo_url': 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
                'posting_url': 'https://careers.google.com',
                'source': 'Company Website',
                'salary_range': '15-20/hour'
            },
            {
                'job_id': 'int_002',
                'title': 'Data Science Intern',
                'company': 'Meta',
                'location': 'Menlo Park, CA',
                'job_type': 'Internship',
                'description': 'Work on cutting-edge ML projects...',
                'required_skills': ['Python', 'Machine Learning', 'Statistics', 'SQL'],
                'company_logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Meta_Platforms_Inc_logo.svg/1200px-Meta_Platforms_Inc_logo.svg.png',
                'posting_url': 'https://careers.meta.com',
                'source': 'Company Website',
                'salary_range': '20-25/hour'
            }
        ]
        
        return sample_internships
    
    @staticmethod
    def scrape_prepinsta() -> List[Dict[str, Any]]:
        """
        Scrape job postings from PrepInsta
        
        Returns:
            List of job postings
        """
        jobs = []
        
        try:
            # Using PrepInsta job openings
            url = "https://www.prepinsta.com/job-openings/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job listings (adjust selectors based on actual HTML structure)
            job_cards = soup.find_all('div', class_='job-card')
            
            for idx, card in enumerate(job_cards[:10]):  # Limit to 10 jobs
                try:
                    title = card.find('h3', class_='job-title')
                    company = card.find('span', class_='company-name')
                    location = card.find('span', class_='job-location')
                    description = card.find('p', class_='job-description')
                    
                    if title and company:
                        jobs.append({
                            'job_id': f'prepinsta_{idx}',
                            'title': title.text.strip(),
                            'company': company.text.strip(),
                            'location': location.text.strip() if location else 'Not specified',
                            'job_type': 'Full-time',
                            'description': description.text.strip() if description else '',
                            'required_skills': [],
                            'company_logo_url': '',
                            'posting_url': 'https://www.prepinsta.com',
                            'source': 'PrepInsta',
                            'salary_range': 'Not specified'
                        })
                except Exception as e:
                    print(f"Error parsing job card: {e}")
                    continue
        
        except Exception as e:
            print(f"Error scraping PrepInsta: {e}")
        
        return jobs
    
    @staticmethod
    def scrape_glassdoor() -> List[Dict[str, Any]]:
        """
        Scrape job postings from Glassdoor
        
        Returns:
            List of job postings
        """
        jobs = []
        
        try:
            # For Glassdoor, using their public job search
            # Note: Glassdoor has anti-scraping measures, using alternative approach
            url = "https://www.glassdoor.com/api/glassdoor.htm"
            
            # Using sample data as actual scraping is blocked
            sample_jobs = [
                {
                    'job_id': 'gd_001',
                    'title': 'Senior Software Engineer',
                    'company': 'Microsoft',
                    'location': 'Seattle, WA',
                    'job_type': 'Full-time',
                    'description': 'Build innovative solutions...',
                    'required_skills': ['C#', '.NET', 'Azure', 'Python'],
                    'company_logo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/1200px-Microsoft_logo.svg.png',
                    'posting_url': 'https://www.glassdoor.com',
                    'source': 'Glassdoor',
                    'salary_range': '150-200k'
                }
            ]
            
            return sample_jobs
        
        except Exception as e:
            print(f"Error scraping Glassdoor: {e}")
            return []
    
    @staticmethod
    def get_all_jobs() -> List[Dict[str, Any]]:
        """
        Fetch jobs from all sources
        
        Returns:
            Combined list of all job postings
        """
        all_jobs = []
        
        # Fetch from multiple sources
        all_jobs.extend(JobFetcher.fetch_internship_postings())
        all_jobs.extend(JobFetcher.scrape_prepinsta())
        all_jobs.extend(JobFetcher.scrape_glassdoor())
        
        # Add timestamps
        for job in all_jobs:
            if 'posted_date' not in job:
                job['posted_date'] = datetime.now().isoformat()
            if 'fetched_at' not in job:
                job['fetched_at'] = datetime.now().isoformat()
        
        return all_jobs
    
    @staticmethod
    def filter_jobs(jobs: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter jobs based on criteria
        
        Args:
            jobs: List of job postings
            filters: Filter criteria (location, job_type, skills, etc.)
        
        Returns:
            Filtered list of jobs
        """
        filtered = jobs
        
        if 'location' in filters:
            filtered = [j for j in filtered if filters['location'].lower() in j.get('location', '').lower()]
        
        if 'job_type' in filters:
            filtered = [j for j in filtered if filters['job_type'].lower() in j.get('job_type', '').lower()]
        
        if 'skills' in filters:
            user_skills = set(s.lower() for s in filters['skills'])
            filtered = [j for j in filtered if any(
                skill.lower() in user_skills for skill in j.get('required_skills', [])
            )]
        
        if 'company' in filters:
            filtered = [j for j in filtered if filters['company'].lower() in j.get('company', '').lower()]
        
        return filtered
