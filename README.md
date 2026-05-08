# Prompt Evaluation & Experimentation System

A full-stack AI Prompt Evaluation and Experimentation platform with DevOps integration using FastAPI, React/Vite, MongoDB, Docker, Jenkins, and SonarQube.

---

# 📌 Project Overview

This repository implements a practical Prompt Evaluation and Experimentation System designed to evaluate, compare, optimize, and track prompts using deterministic metrics and multi-model analysis.

The project also integrates modern DevOps practices including:
- Continuous Integration (CI)
- Static Code Analysis
- Containerization
- Multi-container Deployment

---

# 🎯 Executive Summary

The platform evaluates prompt quality using deterministic scoring metrics, compares outputs across models, supports A/B prompt testing, stores prompt versions, and captures user feedback.

It provides an end-to-end workflow for prompt engineering experimentation and quality monitoring.

---

# 🧠 What the System Does

The system provides:

- Prompt evaluation with deterministic scoring
- Prompt optimization suggestions
- Multi-model response comparison
- A/B prompt testing
- Prompt history and version tracking
- Feedback capture for prompt results
- Prompt injection detection
- Regression alerts for prompt quality changes

---

# 🚀 Key Features

## 🔹 Deterministic Prompt Metrics

- Keyword relevance matching
- Format validation (Bullet / JSON)
- Conciseness checks
- Clarity scoring
- Specificity scoring
- Context scoring
- Instruction scoring
- Ambiguity scoring

---

## 🔹 A/B Prompt Comparison

- Compare Prompt A vs Prompt B
- Side-by-side metric comparison
- Winner recommendation
- Regression detection

---

## 🔹 Multi-Model Output Comparison

Supports comparison between:
- Groq
- Gemini
- HuggingFace

Includes:
- Latency comparison
- Response quality scoring
- Best model recommendation

---

## 🔹 Prompt Versioning & History

- Save prompt versions
- Load previous prompt revisions
- Track prompt improvements
- Support regression monitoring

---

## 🔹 Feedback Capture

- Thumbs-up / thumbs-down feedback
- User comments for prompt quality
- Backend storage for analysis

---

## 🔹 Security Guardrails

- Prompt injection detection
- Safe fallback to mock model responses when API keys are unavailable

---

# 🧩 System Architecture

## Backend
- FastAPI
- Deterministic prompt evaluation engine
- MongoDB integration using Motor

## Frontend
- React
- Vite
- Modern UI components
- Nginx production deployment

## Database
- MongoDB

## DevOps Stack
- Docker
- Docker Compose
- Jenkins
- SonarQube
- GitHub

---

# 📂 Project Structure

```bash
Prompt_Evaluator/
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   └── ...
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── ...
│
├── docker-compose.yml
├── Jenkinsfile
└── README.md

⚙️ Local Setup Instructions

Backend Setup
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8000
Frontend Setup

Open another terminal:

cd frontend

npm install

npm run dev

🌐 Local URLs

Frontend
http://localhost:5173

Backend
http://localhost:8000

Swagger API Docs
http://localhost:8000/docs

🔐 Environment Variables

Copy the backend example environment file:

cd backend

cp .env.example .env

Add your API keys:

GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_gemini_key
HUGGINGFACE_API_KEY=your_huggingface_key

If API keys are missing, the backend automatically uses safe mock responses.

🐳 Docker Setup

Backend Docker

The backend is containerized using:

Python 3.9 Slim
FastAPI
Uvicorn
Frontend Docker

The frontend uses:

Multi-stage Docker builds
Node.js for build stage
Nginx for production deployment

🐳 Docker Compose Setup

Docker Compose orchestrates:

Backend container
Frontend container
MongoDB container

Run Entire Application
docker compose up --build

Stop Containers
docker compose down

🐳 Build Docker Images Manually

Backend
docker build -t prompt-backend:latest ./backend

Frontend
docker build -t prompt-frontend:latest ./frontend

🔄 Jenkins CI Pipeline

The repository includes a Jenkins pipeline for Continuous Integration.
Pipeline Stages
Checkout source code from GitHub
Backend validation
Frontend build
SonarQube static code analysis

📊 SonarQube Integration

SonarQube is integrated for:
Code quality analysis
Bug detection
Vulnerability detection
Code smell detection
Maintainability analysis

🌐 DevOps Service URLs

Jenkins Dashboard
http://localhost:8080

SonarQube Dashboard
http://localhost:9000

📍 Important API Endpoints

Method	Endpoint	Description
POST	/api/analyze	Prompt evaluation
POST	/api/optimize	Prompt optimization
POST	/api/compare	Multi-model comparison
POST	/api/ab-test	A/B prompt testing
POST	/api/feedback	Submit user feedback
GET	/api/prompt-history	Fetch prompt versions
POST	/api/prompt-history	Save prompt version
POST	/api/dataset	Add golden dataset entry

📈 DevOps Workflow

GitHub
   ↓
Jenkins CI Pipeline
   ↓
Backend Validation
   ↓
Frontend Build
   ↓
SonarQube Analysis
   ↓
Docker Compose Deployment

🧪 What's New

Deterministic prompt metrics added
Regression detection support
A/B prompt testing feature
Prompt version history support
User feedback capture
Docker containerization
Docker Compose deployment
Jenkins CI pipeline integration
SonarQube static analysis integration
Nginx frontend deployment

🧠 Current Status

✅ Backend available on http://localhost:8000
✅ Frontend available on http://localhost:3000
✅ Docker Compose deployment working
✅ MongoDB integration working
✅ Jenkins pipeline configured
✅ SonarQube analysis configured
✅ Frontend production build working with Nginx
✅ Prompt history and feedback system implemented

📚 Learning Outcomes

This project demonstrates:

Full-stack application development
Prompt engineering experimentation
CI/CD pipeline implementation
Docker containerization
Multi-container orchestration
Static code analysis
DevOps workflow integration

📌 Future Improvements

Prompt dataset management dashboard
Regression trend visualization
Analytics dashboards
Unit and integration testing
Automated deployment pipeline
Kubernetes integration
Monitoring and logging tools
Cloud deployment support

