# Phase II Technical Plan - Evolution of Todo

Derived from `speckit/spec.md` and `speckit/constitution.md`.

## 1. Backend Plan (FastAPI)
-   **Framework**: FastAPI (High performance, easy REST generation).
-   **Structure**:
    ```
    backend/
      main.py           # Entry point
      database.py       # Neon DB connection & SQLModel config
      models.py         # User and Todo data models
      auth.py           # Better Auth integration (or simplified JWT logic if library unavailable)
      routers/
        todos.py        # CRUD endpoints
        auth.py         # Signin/Signup endpoints
    ```
-   **Dependencies**: `fastapi`, `uvicorn`, `sqlmodel`, `psycopg2-binary` (or `asyncpg`).

## 2. Database Plan (Neon PostgreSQL)
-   **Connection**: Connection string provided via `.env` (User to provide).
-   **ORM**: SQLModel (Combines Pydantic & SQLAlchemy).
-   **Tables**:
    -   `User`: id, email, password_hash
    -   `Todo`: id, user_id, title, status, created_at
-   **Migration**: `sqlmodel.create_all()` on startup for simplicity in this phase.

## 3. Frontend Plan (Next.js)
-   **Framework**: Next.js (App Router).
-   **Structure**:
    ```
    frontend/
      app/
        page.tsx        # Landing / Redirect
        login/          # Login page
        signup/         # Signup page
        dashboard/      # Protected Todo list
      components/
        TodoItem.tsx
        AddTodoForm.tsx
      lib/
        api.ts          # Axios/Fetch wrapper
        auth.context.tsx # React Context for auth state
    ```
-   **Styling**: CSS Modules or Tailwind (if requested, else standard CSS).

## 4. Integration Plan
-   **CORS**: Configure FastAPI `CORSMiddleware` to allow `localhost:3000`.
-   **Authentication**:
    -   Frontend stores token (localStorage/cookie).
    -   Sends token in `Authorization: Bearer <token>` header.
    -   Backend dependency `get_current_user` validates token.
-   **Development**:
    -   Run Backend: `uvicorn backend.main:app --reload`
    -   Run Frontend: `npm run dev`

## 5. Constraints
-   No background workers.
-   No Websockets.
-   Strict Phase II rules.
