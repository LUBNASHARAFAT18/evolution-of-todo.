from sqlmodel import Session, create_engine, select
import sys
import os

# Adjust path to find backend module
sys.path.append(os.getcwd())

from backend.models import User

# Connect to the database in the CURRENT directory (root)
engine = create_engine("sqlite:///./todo.db")

with Session(engine) as session:
    users = session.exec(select(User)).all()
    print(f"Total Users: {len(users)}")
    for user in users:
        print(f"User: {user.email}, ID: {user.id}")
