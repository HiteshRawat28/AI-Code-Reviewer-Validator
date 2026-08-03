# AI Code Reviewer

A stunning, intelligent code review tool powered by the Groq API. Paste a code snippet, and get instant, structured, and color-coded feedback on **Bugs**, **Style Violations**, and **Security Vulnerabilities**.

## Live Demo
🚀 **Try it out here:** [https://ai-code-reviewer-validator.vercel.app/](https://ai-code-reviewer-validator.vercel.app/)

## Features
- **Lightning Fast LLM Analysis**: Powered by Groq's high-speed inference (using `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, and `gemma2-9b-it`).
- **Resilient Fallback**: Automatically cascades through models if API quota limits are hit.
- **Strict Pydantic Validation**: LLM outputs are rigorously validated against a JSON schema. If the model hallucinates or provides malformed JSON, the backend automatically issues a strict retry prompt before gracefully erroring out.
- **Premium UI**: A sleek, modern, glassmorphic dark-mode frontend built in React (Vite).
- **Zero Database MVP**: Fully stateless—no user tracking, no code persistence.
- **Production Hardened**: Features IP-based rate limiting and strict CORS policies to prevent abuse and protect LLM quotas.

## Tech Stack
- **Frontend**: React, Vite, Vanilla CSS
- **Backend**: FastAPI, Uvicorn, Pydantic, SlowAPI (Rate Limiting)
- **AI**: Groq Python SDK
- **Deployment**: Vercel (Frontend), Render (Backend)

---

## Local Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Node.js v18+

### 2. Backend Setup
Navigate to the `backend` directory:
```bash
cd backend
```

Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up your Environment Variables:
- Copy `.env.example` to `.env`
- Add your Groq API key:
```env
GROQ_API_KEY="your_actual_api_key_here"
```

Run the backend server on **port 8001**:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### 3. Frontend Setup
Open a **new terminal window** and navigate to the `frontend` directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the Vite development server:
```bash
npm run dev
```

### 4. Usage
- Open your browser and navigate to `http://localhost:5173`.
- Select your programming language from the dropdown.
- Paste a snippet of code (e.g., a function with a bug or a missing docstring).
- Click **Analyze Code** and watch the structured feedback generate!

---

## Architecture Details
This project enforces a strict "Validator" pattern. The LLM is explicitly prompted to respond *only* in JSON format matching a specific schema. The FastAPI backend intercepts this response, parses the JSON, and uses Pydantic to ensure all fields (Bugs, Style Issues, Security Issues, Severities) are exactly correct before passing the trusted data to the frontend.
