from fastapi import FastAPI, UploadFile, File, Form
import shutil, os, json
from utils.pdf_parser import extract_text_from_pdf
from utils.ai_engine import recommend_roles, generate_leveled_questions, evaluate_responses

app = FastAPI()

@app.post("/analyze-resume")
async def analyze(file: UploadFile = File(...)):
    if not os.path.exists("temp"): os.makedirs("temp")
    path = f"temp/{file.filename}"
    with open(path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
    
    text = extract_text_from_pdf(path)
    roles = recommend_roles(text)
    return {"resume_text": text, "recommended_roles": roles}

@app.post("/get-questions")
async def get_qs(role: str = Form(...), resume_text: str = Form(...)):
    questions = generate_leveled_questions(role, resume_text)
    return {"questions": questions}

@app.post("/evaluate")
async def eval_interview(responses: list):
    return evaluate_responses(responses)