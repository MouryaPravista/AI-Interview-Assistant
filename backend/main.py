from fastapi import FastAPI, UploadFile, File, Form
from typing import List
import shutil, os
from utils.pdf_parser import extract_text_from_pdf
from utils.ai_engine import recommend_roles, generate_questions, evaluate_responses

app = FastAPI()

@app.post("/analyze-resume")
async def analyze(file: UploadFile = File(...)):
    if not os.path.exists("temp"): os.makedirs("temp")
    path = f"temp/{file.filename}"
    with open(path, "wb") as b: shutil.copyfileobj(file.file, b)
    text = extract_text_from_pdf(path)
    return {"resume_text": text, "recommended_roles": recommend_roles(text)}

@app.post("/get-questions")
async def get_qs(role: str = Form(...), resume_text: str = Form(...), level: str = Form(...)):
    return {"questions": generate_questions(role, resume_text, level)}

@app.post("/evaluate")
async def eval_interview(responses: List[dict]):
    return evaluate_responses(responses)