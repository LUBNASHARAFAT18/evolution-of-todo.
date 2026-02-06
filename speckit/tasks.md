# Phase II Implementation Tasks

Derived from `speckit/plan.md`.

## Backend (FastAPI + Neon + Auth)
- [x] **TASK-B01**: Initialize `backend` directory and virtual environment structure.
- [x] **TASK-B02**: Install dependencies (`fastapi`, `uvicorn`, `sqlmodel`, `passlib`, `python-jose`, `python-multipart`).
- [x] **TASK-B03**: Implement `backend/database.py` with SQLModel and Neon DB connection.
- [x] **TASK-B04**: Implement `backend/models.py` defining `User` and `Todo` tables.
- [x] **TASK-B05**: Implement `backend/auth.py` (Password hashing, JWT token generation, `get_current_user` dependency).
- [x] **TASK-B06**: Implement `backend/routers/auth.py` (Signup `POST /auth/signup`, Login `POST /auth/token`).
- [x] **TASK-B07**: Implement `backend/routers/todos.py` (CRUD: Create, Read, Update, Delete, Toggle).
- [x] **TASK-B08**: Implement `backend/main.py` entry point (CORS setup, include routers).

## Frontend (Next.js)
- [x] **TASK-F01**: Initialize `frontend` directory using `create-next-app`.
- [x] **TASK-F02**: Setup API client helper (`lib/api.ts`) with Authorization header injection.
- [x] **TASK-F03**: Create Auth Context (`lib/auth.context.tsx`) to manage user session.
- [x] **TASK-F04**: Implement Sign Up Page (`app/signup/page.tsx`).
- [x] **TASK-F05**: Implement Sign In Page (`app/login/page.tsx`).
- [x] **TASK-F06**: Implement Dashboard Page (`app/dashboard/page.tsx`) with Todo List.
- [x] **TASK-F07**: Create `AddTodoForm` component.
- [x] **TASK-F08**: Create `TodoItem` component with Edit/Delete/Toggle actions.
- [x] **TASK-F09**: Implement route protection (Redirect to /login if unauthenticated).

- [x] Perform complete E2E flow: Signup -> Login -> Add Todo -> View -> Logout.

## Phase III Implementation Tasks
- [x] **TASK-A01**: Setup MCP Server project structure.
- [x] **TASK-A02**: Implement `add_task` tool.
- [x] **TASK-A03**: Implement `list_tasks` tool.
- [x] **TASK-A04**: Implement `complete_task` tool.
- [x] **TASK-A05**: Implement `delete_task` tool.
- [x] **TASK-A06**: Implement `update_task` tool.
- [x] **TASK-A07**: Define Antigravity Agent YAML/JSON spec.
- [ ] **TASK-A08**: Verify E2E flow via Chatbot interface.
