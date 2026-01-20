# backend/routes/jobs.py
from fastapi import APIRouter, HTTPException
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/jobs", tags=["Job Search"])
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

@router.get("/search")
def search_jobs(query: str, location: str = "India"):
    """
    Searches for live job listings using Google Search API (Serper).
    """
    if not SERPER_API_KEY:
        raise HTTPException(status_code=500, detail="Serper API Key missing in backend .env")

    url = "https://google.serper.dev/search"
    
    # We explicitly add "jobs" to the query to force job results
    # e.g. "Python Intern jobs in Pune"
    search_term = f"{query} jobs in {location}"
    
    payload = json.dumps({
        "q": search_term,
        "num": 15,       # Number of results
        "tbs": "qdr:w"   # "qdr:w" filters for jobs posted in the Past Week (Fresh data!)
    })
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()
        
        # Parse the results. Serper usually gives 'organic' results for this.
        jobs_list = []
        
        # Check if Serper found organic results
        if "organic" in data:
            for item in data["organic"]:
                jobs_list.append({
                    "title": item.get("title", "Job Opportunity"),
                    "company": item.get("source", "Unknown Company"), # 'source' usually holds the website name
                    "link": item.get("link", "#"),
                    "snippet": item.get("snippet", "Click to see details."),
                    "date": item.get("date", "Recently posted")
                })
                
        return {"count": len(jobs_list), "jobs": jobs_list}

    except Exception as e:
        print(f"Job Search Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))