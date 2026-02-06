# Evolution of Todo (Hackathon Phase IV Completed)

![Project Status](https://img.shields.io/badge/Status-Completed-green)
![Phase](https://img.shields.io/badge/Phase-IV-blue)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Next.js%20%7C%20PostgreSQL%20%7C%20Docker%20%7C%20K8s-blueviolet)

> A Spec-Driven, AI-Integrated, Cloud-Native Todo Application.

## 🌟 Overview
This project represents the evolution of a simple Todo application into a full-scale, cloud-native system with AI capabilities. It was built following **Spec-Driven Development** principles.

## 🚀 Features

### Phase I & II: Full Stack Web App
- **Frontend**: Next.js 14+ (App Router), Tailwind CSS.
- **Backend**: FastAPI (Python), SQLModel, PostgreSQL.
- **Auth**: Secure Authentication (JWT).
- **Core Features**: CRUD Todos, User Isolation via Auth.

### Phase III: AI Integration 🤖
- **AI Agent**: Integrated Gemini 1.5 Flash via `google-genai` SDK.
- **Natural Language Control**: "Add a task to buy groceries" -> *Action Performed*.
- **Tool Calling**: The integration allows the LLM to directly interact with the database (CRUD operations).
- **Interactive UI**: Dedicated Chat Interface in the Dashboard.

### Phase IV: Cloud-Native Infrastructure ☁️
- **Containerization**: Optimized Dockerfiles for Frontend and Backend.
- **Orchestration**: Kubernetes Helm Charts for scalable deployment.
- **Automation**: One-click deployment script (`deploy_k8s.ps1`) for Minikube.
- **AIOps**: workflows for `kubectl-ai` and `kagent`.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker Desktop
- Minikube & Helm (for Phase IV)

### 1. Environment Setup
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost/todo_db
SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
```

### 2. Run Locally (Dev Mode)

**Backend:**
```bash
# In the root directory
pip install -r backend/requirements.txt
uvicorn backend.main:app --port 8001 --reload
```

**Frontend:**
```bash
# In /frontend directory
npm install
npm run dev
```
Access at: `http://localhost:3000`

### 3. Run on Kubernetes (Minikube)

We have automated the local Kubernetes deployment.

1. **Open PowerShell as Administrator**.
2. Run the deployment script:
   ```powershell
   .\deploy_k8s.ps1
   ```
3. Follow the prompts (enter API Key).

See [`k8s/AI_OPS.md`](k8s/AI_OPS.md) for managing the cluster with AI.

---

## 📂 Project Structure

```
├── backend/            # FastAPI Application
│   ├── main.py         # App Entry & AI Logic
│   ├── models.py       # SQLModel Database Schemas
│   ├── auth.py         # JWT Authentication
│   └── tests/          # Unit Tests
├── frontend/           # Next.js Application
│   ├── app/            # App Router Pages
│   ├── components/     # UI Components (ChatInterface, etc.)
│   └── lib/            # API & Context utilities
├── k8s/                # Kubernetes Infrastructure
│   ├── helm/           # Helm Charts (frontend/backend)
│   └── AI_OPS.md       # AI Operations Guide
├── speckit/            # Specifications & Architecture
│   ├── spec.md         # Phase 1-3 Specs
│   └── phase4_spec.md  # Phase 4 Spec
└── deploy_k8s.ps1      # Deployment Automation Script
```

## 🧪 Testing
Run the backend verification script:
```bash
python test_backend.py
```

## 📜 Deployment Guides
- **Vercel**: See [`DEPLOY_VERCEL.md`](DEPLOY_VERCEL.md)
- **Kubernetes**: See [`k8s/AI_OPS.md`](k8s/AI_OPS.md)

---

**Developed for Hackathon II**
