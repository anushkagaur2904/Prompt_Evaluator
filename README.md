# Prompt Evaluation & Experimentation System
# Prompt Evaluation & Experimentation System

## Quick Start
Start the backend and frontend locally with these commands:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the frontend at `http://localhost:5173` and backend at `http://localhost:8000`.

## 1. 🎯 Executive Summary
This repository implements a practical prompt evaluation and experimentation system with a FastAPI backend and a React frontend.

The platform evaluates prompt quality using deterministic metrics, compares outputs across models, supports A/B prompt testing, stores prompt versions, and captures user feedback.

## 2. 🧠 What the System Does
The system provides:
* Prompt evaluation with deterministic scoring
* Prompt optimization suggestions
* Multi-model response comparison
* A/B prompt testing
* Prompt history and version tracking
* Feedback capture for prompt results
* Prompt injection detection and regression alerts

## 3. 🚀 Key Features

### 🔹 Deterministic Prompt Metrics
* Keyword relevance matching
* Format validation (bullet / JSON)
* Conciseness checks
* Clarity, specificity, context, instruction, and ambiguity scoring

### 🔹 A/B Prompt Comparison
* Compare Prompt A vs Prompt B
* Side-by-side metric view
* Winner recommendation and regression indicator

### 🔹 Multi-Model Output Comparison
* Compare Groq, Gemini, and HuggingFace outputs
* Latency and score summary
* Best model recommendation

### 🔹 Prompt Versioning & History
* Save prompt versions
* Load previous prompt revisions
* Support regression tracking

### 🔹 Feedback Capture
* Thumbs-up / thumbs-down feedback
* Comment capture for prompt quality
* Stored in the backend for future analysis

### 🔹 Security Guardrails
* Prompt injection detection
* Safe fallback to mock model responses when API keys are missing

## 4. 🧩 Architecture
* **Backend:** FastAPI, deterministic prompt evaluation, MongoDB storage helpers
* **Frontend:** React, Vite, modern UI components
* **Database:** MongoDB (via Motor)
* **DevOps:** Docker support and Jenkins pipeline

## 5. 🔧 Setup Instructions

### Local Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Local Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
Copy the backend example env file and add your API keys:
```bash
cd backend
cp .env.example .env
```
Edit `.env` with your keys:
```env
GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_gemini_key
HUGGINGFACE_API_KEY=your_huggingface_key
```
If API keys are missing, the backend uses safe mock responses.

### Run with Docker Compose
```bash
docker-compose up -d
```

### Build Docker Images
```bash
docker build -t prompt-backend:latest ./backend
docker build -t prompt-frontend:latest ./frontend
```

### Jenkins Pipeline
The repo includes a Jenkinsfile that:
* installs backend and frontend dependencies
* builds Docker images
* runs containers locally for verification
* checks service health on `http://localhost:8000` and `http://localhost:3000`

## 6. 📍 Important Endpoints
* `POST /api/analyze` – prompt evaluation
* `POST /api/optimize` – prompt optimization
* `POST /api/compare` – multi-model comparison
* `POST /api/ab-test` – A/B comparison
* `POST /api/feedback` – submit feedback
* `GET /api/prompt-history` – fetch prompt versions
* `POST /api/prompt-history` – save prompt version
* `POST /api/dataset` – add golden dataset entry

## 7. 🧪 What’s New
* deterministic prompt metrics added
* regression detection on prompt scores
* A/B prompt comparison feature
* prompt version history and save/load support
* user feedback buttons and storage
* updated Docker and Jenkins support for the current repo

## 8. 🧠 Current Status
* ✅ Backend available on `http://localhost:8000`
* ✅ Frontend build passes with Vite
* ✅ New UI components for A/B testing and prompt history
* ✅ Feedback capture is implemented
* ✅ Jenkins pipeline updated for frontend port mapping

## 9. 📌 Next Steps
* Add prompt dataset management UI
* Add regression visualization and trend tracking
* Extend storage with analytics dashboards
* Add more robust unit/integration tests
