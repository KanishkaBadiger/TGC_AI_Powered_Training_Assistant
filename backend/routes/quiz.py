from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import os
import requests
import json
import re

# ✅ Define Router
router = APIRouter(prefix="/api/quiz", tags=["Quiz"])

# ------------------ MODELS ------------------
class QuizGenerateRequest(BaseModel):
    user_id: int
    domain: str           # <--- ✅ Matches your Frontend now
    category: str
    num_questions: int
    difficulty: str

class QuizSubmitRequest(BaseModel):
    user_id: int
    answers: Dict[str, str]

# ------------------ IN-MEMORY STORE ------------------
QUIZ_STORE = {}

# ------------------ GROQ CONFIG ------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# ------------------ GROQ HELPER ------------------
def generate_quiz_with_groq(domain, category, difficulty, num_questions):
    if not GROQ_API_KEY:
        # Fallback for testing if key is missing
        print("⚠️ API Key missing. Returning mock data.")
        return [
            {
                "id": "q1",
                "question": "Mock Question: API Key Missing",
                "options": ["Option A", "Option B"],
                "correct_answer": "Option A",
                "explanation": "Add GROQ_API_KEY to .env"
            }
        ]

    prompt = f"""
    Generate {num_questions} {difficulty} level {category} questions on {domain}.

    RULES:
    - Return ONLY valid JSON
    - No markdown, no text outside JSON

    FORMAT:
    {{
      "questions": [
        {{
          "question": "",
          "options": ["", "", "", ""],
          "correct_answer": "",
          "explanation": ""
        }}
      ]
    }}
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=25
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Groq API Error: {response.text}")

        content = response.json()["choices"][0]["message"]["content"]
        content = re.sub(r"```json|```", "", content).strip()
        
        data = json.loads(content)
        
        quiz = []
        for i, q in enumerate(data["questions"]):
            quiz.append({
                "id": f"q{i+1}",
                "question": q["question"],
                "options": q["options"],
                "correct_answer": q["correct_answer"],
                "explanation": q["explanation"]
            })

        return quiz

    except Exception as e:
        print(f"Error generating quiz: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate quiz")

# ------------------ ROUTES ------------------

@router.post("/generate")
def generate_quiz(data: QuizGenerateRequest):
    # Call the helper
    quiz = generate_quiz_with_groq(
        data.domain,
        data.category,
        data.difficulty,
        data.num_questions
    )

    # Save to memory
    QUIZ_STORE[data.user_id] = quiz

    # Return list directly (Teammate's format)
    return [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        for q in quiz
    ]

@router.post("/submit")
def submit_quiz(data: QuizSubmitRequest):
    if data.user_id not in QUIZ_STORE:
        # Fallback if server restarted
        return {"error": "Quiz session not found. Please regenerate."}

    quiz = QUIZ_STORE[data.user_id]
    results = []

    for q in quiz:
        user_answer = data.answers.get(q["id"])

        results.append({
            "question_id": q["id"],
            "question_text": q["question"],
            "your_answer": user_answer,
            "correct_answer": q["correct_answer"],
            "is_correct": user_answer == q["correct_answer"],
            "explanation": q["explanation"]
        })

    return results