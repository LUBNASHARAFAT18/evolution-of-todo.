from backend.database import engine
from backend.models import User
from sqlmodel import Session, select

with Session(engine) as session:
    users = session.exec(select(User)).all()
    for user in users:
        print(f"ID: {user.id}, Email: {user.email}, Hash: {user.hashed_password[:10]}...")
