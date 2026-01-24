# Phase II Specification - Evolution of Todo

**Phase II Goal**: Implement all 5 Basic Level Todo features as a full-stack web application.

## 1. Requirements

### Backend Requirements (Python/FastAPI)
1.  **RESTful API Endpoints**:
    -   Create a todo
    -   Retrieve all todos (for the current user)
    -   Update a todo
    -   Delete a todo
    -   Toggle todo complete/incomplete
2.  **Persistence**:
    -   Store data in Neon Serverless PostgreSQL.
3.  **Authentication & Data Isolation**:
    -   Associate data with authenticated users.
    -   Users can only access *their own* todos.
4.  **Format**: JSON for requests and responses.

### Authentication Requirements (Better Auth)
1.  **User Signup**: Ability to create a new account.
2.  **User Signin**: Ability to log in.
3.  **Authorization**: Protect API execution (Authenticated users only).
4.  **Simplicity**: No complex roles or permissions.

### Frontend Requirements (Next.js)
1.  **Web Application**: Built with Next.js (React).
2.  **Pages**:
    -   Sign Up Page
    -   Sign In Page
    -   Dashboard (List of todos)
3.  **Features**:
    -   Add Todo Form
    -   Edit Todo capability
    -   Delete Todo button
    -   Toggle Complete/Incomplete status
4.  **Responsive UI**: Optimized for desktop and mobile.

## 2. Data Model

### User
-   `id`: UUID/Integer (Primary Key)
-   `email`: String (Unique)
-   `password_hash`: String

### Todo
-   `id`: UUID/Integer (Primary Key)
-   `user_id`: Foreign Key to User
-   `title`: String (Required)
-   `status`: Enum/String ("Incomplete", "Complete") - Default: "Incomplete"
-   `created_at`: Datetime

## 3. Acceptance Criteria
1.  User can sign up and sign in.
2.  Backend API protects routes (returns 401 for unauthenticated requests).
3.  User creates a todo -> Data persists in Neon DB.
4.  User sees ONLY their own todos on the dashboard.
5.  User can update, delete, and toggle completion of a todo.
6.  Frontend is responsive and provides feedback (loading states/errors).

## 4. Non-Functional Constraints
-   No Al agents (yet).
-   No background jobs or real-time sockets.
-   No complex analytics.
