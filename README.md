# AI Interview Assistant 🤖

An intelligent, full-stack interview preparation platform that uses **LLMs (Gemini 2.5 Flash)** to simulate realistic technical interviews based on a user's unique resume and target job role.

## 🚀 Key Features
- **Dynamic Resume Analysis:** Extracts technical skills and experience from PDF resumes using `PyPDF2`.
- **Intelligent Role Recommendation:** Suggests career paths based on the candidate's background.
- **Multi-Level Interviewing:** Generates targeted questions across three difficulty levels (Easy, Medium, Hard).
- **Automated AI Evaluation:** Provides instant scoring (0-10), constructive feedback, and "Ideal Answers" for every response.
- **Cost-Optimized Engineering:** Targeted question generation to minimize token usage and API latency.

## 🛠️ Technical Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Streamlit
- **AI Engine:** Google Gemini 2.5 Flash API
- **NLP & Parsing:** PyPDF2, Prompt Engineering
- **Environment Management:** Conda / Dotenv

## 📂 Project Structure
```text
├── backend/        # FastAPI REST API
├── frontend/       # Streamlit User Interface
├── utils/          # AI Engine & PDF Parsing logic
├── temp/           # Temporary storage for resume processing
├── .env            # Private API Keys (Hidden)
└── requirements.txt # Project dependencies
