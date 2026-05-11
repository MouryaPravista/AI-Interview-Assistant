import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def recommend_roles(resume_text):
    """Suggests 3 job roles based on the resume."""
    prompt = f"Resume: {resume_text}\nBased on this resume, suggest exactly 3 professional job roles. Return ONLY a JSON list of strings: ['Role1', 'Role2', 'Role3']"
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text.replace("```json", "").replace("```", "").strip())
    except:
        return ["Software Engineer", "Data Analyst", "Product Manager"]

def generate_leveled_questions(role, resume_text):
    """Generates 9 questions divided by difficulty."""
    prompt = f"""
    Role: {role}
    Resume: {resume_text}
    Task: Generate 9 interview questions. 
    - 3 Easy (Fundamentals/Syntax)
    - 3 Medium (Scenario/Problem Solving)
    - 3 Hard (System Design/Deep Technical)
    
    Return ONLY a JSON object:
    {{
        "easy": [{{ "question": "..." }}, {{ "question": "..." }}, {{ "question": "..." }}],
        "medium": [{{ "question": "..." }}, {{ "question": "..." }}, {{ "question": "..." }}],
        "hard": [{{ "question": "..." }}, {{ "question": "..." }}, {{ "question": "..." }}]
    }}
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except:
        return {"easy": [], "medium": [], "hard": []}

def evaluate_responses(responses):
    """Grades all 9 answers with strict JSON formatting."""
    prompt = f"""
    You are a strict technical interviewer. Evaluate these responses: {responses}
    
    Return ONLY a JSON object with these EXACT keys:
    {{
        "overall_score": "X/10",
        "feedback": "A short summary of performance",
        "details": [
            {{
                "question": "the question text",
                "score": 5,
                "feedback": "why this score"
            }}
        ]
    }}
    """
    try:
        response = model.generate_content(prompt)
        # Remove any markdown backticks the AI might add
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        # If it fails, we return a "Safe" dictionary so the app doesn't crash
        return {
            "overall_score": "N/A", 
            "feedback": f"Parsing Error: {str(e)}", 
            "details": []
        }