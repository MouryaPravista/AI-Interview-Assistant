import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def clean_json(text):
    """Safely extracts JSON from AI response."""
    try:
        start = text.find('[') if text.find('[') < text.find('{') and text.find('[') != -1 else text.find('{')
        end = text.rfind(']') + 1 if text.rfind(']') > text.rfind('}') else text.rfind('}') + 1
        return json.loads(text[start:end])
    except: return None

def recommend_roles(resume_text):
    prompt = f"Resume: {resume_text}\nSuggest 3 job roles. Return ONLY a JSON list: ['Role1', 'Role2', 'Role3']"
    res = model.generate_content(prompt)
    return clean_json(res.text) or ["Software Engineer", "Data Analyst", "AI Developer"]

def generate_questions(role, resume_text, level):
    """Generates 5 professional, diverse interview questions."""
    prompt = f"""
    You are a Senior Hiring Manager for {role}. 
    Difficulty: {level}. Candidate Resume: {resume_text}
    
    Task: Generate 5 distinct interview questions. 
    1. Resume Project Deep-dive.
    2. Real-world Industry Tooling/Standards.
    3. Technical Scenario (Problem Solving).
    4. Behavioral/Teamwork question.
    5. Scalability/Optimization (Harder concept).
    
    Return ONLY a JSON list of objects: [{{"question": "..."}}]
    """
    res = model.generate_content(prompt)
    data = clean_json(res.text)
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], str):
        data = [{"question": q} for q in data]
    return data[:5] if data else [{"question": "Describe your technical background."}]

def evaluate_responses(responses):
    prompt = f"Act as a strict Interviewer. Evaluate these 5 responses: {responses}. Return ONLY JSON: {{'overall_score': 'X/10', 'feedback': 'summary', 'details': [{{'question': '...', 'score': 0-10, 'feedback': '...'}}]}}"
    res = model.generate_content(prompt)
    return clean_json(res.text) or {"overall_score": "N/A", "feedback": "Evaluation failed", "details": []}