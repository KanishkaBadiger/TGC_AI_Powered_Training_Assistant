# backend/utils/roadmap_ai.py
import json
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_roadmap_plan(role, days, skill_level, roadmap_type):
    # We strictly enforce JSON structure with specific fields for links
    system_prompt = f"""
    You are a strictly structured senior technical mentor. Create a detailed {days}-day study roadmap for a {skill_level} {role}.
    Focus Area: {roadmap_type}.
    
    CRITICAL OUTPUT RULES:
    1. Output MUST be valid JSON only. No markdown formatting.
    2. "resources" must be an ARRAY of objects with "title" and "url".
    3. For DSA topics, YOU MUST provide a matching LeetCode or GeeksForGeeks problem link.
    4. For Theory, provide a high-quality article (Medium/Dev.to) or documentation link.
    
    JSON FORMAT:
    {{
      "roadmap": [
        {{
            "day": 1,
            "module": "Arrays",
            "topic": "Kadane's Algorithm",
            "description": "Understand the logic behind maximum subarray sum. Solve 1 easy and 1 medium problem.",
            "resources": [
                {{"title": "Read: Kadane's Algo Explanation", "url": "https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/"}},
                {{"title": "Practice: Maximum Subarray (LeetCode)", "url": "https://leetcode.com/problems/maximum-subarray/"}}
            ],
            "time_min": 90
        }}
      ]
    }}
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.3
        )
        data = json.loads(completion.choices[0].message.content)
        return data.get("roadmap", [])
    except Exception as e:
        print(f"AI Error: {e}")
        return []