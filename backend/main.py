from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List

from backend.database import create_db_and_tables, get_session
from backend.models import User, UserCreate, Todo, TodoCreate, TodoUpdate, Token
from backend.auth import get_password_hash, verify_password, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Client will be initialized inside handler

app = FastAPI(title="Evolution of Todo (Phase II)")

# CORS Middleware (Allow Frontend)
# CORS Middleware (Allow Frontend)
origins = [
    "*", # Allow all origins for Vercel (Preview & Prod)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"status": "Evolution of Todo Backend is Running", "phase": 4, "infrastructure": "Kubernetes"}

# --- Auth Routes ---

@app.post("/auth/signup", response_model=Token)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_data.email)).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_pw)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Auto-login after signup
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Todo Routes ---

@app.post("/todos/", response_model=Todo)
def create_todo(todo_data: TodoCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        priority=todo_data.priority,
        user_id=current_user.id
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo

@app.get("/todos/", response_model=List[Todo])
def read_todos(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()

@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.priority is not None:
        todo.priority = todo_update.priority
    if todo_update.status is not None:
        todo.status = todo_update.status
        
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    session.delete(todo)
    session.commit()
    return {"ok": True}

# --- Chat Agent (Phase III - Gemini Integration) ---

def get_chat_tools(current_user: User, session: Session):
    """Define tools for Gemini to interact with the database."""
    
    def add_todo_tool(title: str, description: str = None, priority: str = "Medium"):
        """Add a new task to the todo list with optional description and priority (Low, Medium, High)."""
        new_todo = Todo(title=title, description=description, priority=priority, user_id=current_user.id)
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)
        return f"Success: Task '{title}' added with {priority} priority."

    def list_todos_tool():
        """List all tasks for the current user."""
        todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
        if not todos:
            return "No tasks found."
        return "\n".join([f"- [{t.id}] {t.title} ({t.status})" for t in todos])

    def complete_todo_tool(todo_id: int):
        """Mark a task as complete using its ID."""
        todo = session.get(Todo, todo_id)
        if not todo or todo.user_id != current_user.id:
            return f"Error: Task {todo_id} not found."
        todo.status = "Complete"
        session.add(todo)
        session.commit()
        return f"Success: Task '{todo.title}' marked as complete."

    def delete_todo_tool(todo_id: int):
        """Delete a task using its ID."""
        todo = session.get(Todo, todo_id)
        if not todo or todo.user_id != current_user.id:
            return f"Error: Task {todo_id} not found."
        title = todo.title
        session.delete(todo)
        session.commit()
        return f"Success: Task '{title}' deleted."

    def update_todo_tool(todo_id: int, title: str = None, description: str = None, priority: str = None, status: str = None):
        """Update a task's title, description, priority or status using its ID."""
        todo = session.get(Todo, todo_id)
        if not todo or todo.user_id != current_user.id:
            return f"Error: Task {todo_id} not found."
        
        changes = []
        if title:
            todo.title = title
            changes.append(f"title to '{title}'")
        if description:
            todo.description = description
            changes.append(f"description to '{description}'")
        if priority:
            todo.priority = priority
            changes.append(f"priority to '{priority}'")
        if status:
            if status not in ["Complete", "Incomplete"]:
                 return "Error: Status must be 'Complete' or 'Incomplete'."
            todo.status = status
            changes.append(f"status to '{status}'")
            
        if not changes:
            return "No changes requested."
            
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return f"Success: Updated Task {todo_id} " + ", ".join(changes) + "."

    return {
        "add_task": add_todo_tool,
        "list_tasks": list_todos_tool,
        "complete_task": complete_todo_tool,
        "delete_task": delete_todo_tool,
        "update_task": update_todo_tool
    }

@app.post("/chat")
def chat_with_agent(data: dict, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    user_message = data.get("message", "")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Initialize Client inside to ensure correct API key loading
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Initialize tools
    tools = get_chat_tools(current_user, session)
    
    # Wrap tools to detect if any was called (for frontend refresh)
    refresh_called = [False]
    def wrap_tool(name, func):
        def wrapper(**kwargs):
            refresh_called[0] = True
            return func(**kwargs)
        wrapper.__name__ = name
        wrapper.__doc__ = func.__doc__
        return wrapper

    tool_functions = [wrap_tool(name, func) for name, func in tools.items()]

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                tools=tool_functions,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=False
                )
            )
        )

        return {
            "reply": response.text,
            "refresh": refresh_called[0]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Gemini Error: {e}")
        return {
            "reply": "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later.",
            "refresh": False
        }
