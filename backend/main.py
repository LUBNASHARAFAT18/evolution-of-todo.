from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List

from .database import create_db_and_tables, get_session
from .models import User, UserCreate, Todo, TodoCreate, TodoUpdate, Token
from .auth import get_password_hash, verify_password, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

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
