import asyncio
from typing import Optional
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server.stdio import stdio_server
from sqlmodel import Session, select
from backend.database import engine, create_db_and_tables
from backend.models import Todo, User

# Ensure tables are created
create_db_and_tables()

app = Server("todo-agent")

DEFAULT_USER_EMAIL = "agent@todo.ai"

def get_agent_user_id(session: Session) -> int:
    user = session.exec(select(User).where(User.email == DEFAULT_USER_EMAIL)).first()
    if not user:
        # Create a system user for the agent
        user = User(email=DEFAULT_USER_EMAIL, hashed_password="system_user_no_password")
        session.add(user)
        session.commit()
        session.refresh(user)
    return user.id

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="add_task",
            description="Create a new task",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the task"},
                },
                "required": ["title"],
            },
        ),
        types.Tool(
            name="list_tasks",
            description="List todos for the agent user",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"},
                },
            },
        ),
        types.Tool(
            name="complete_task",
            description="Mark a task as complete",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to complete"},
                },
                "required": ["task_id"],
            },
        ),
        types.Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to delete"},
                },
                "required": ["task_id"],
            },
        ),
        types.Tool(
            name="update_task",
            description="Update title or status of a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to update"},
                    "title": {"type": "string", "description": "New title"},
                    "status": {"type": "string", "enum": ["Incomplete", "Complete"], "description": "New status"},
                },
                "required": ["task_id"],
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    with Session(engine) as session:
        user_id = get_agent_user_id(session)
        
        if name == "add_task":
            title = arguments["title"]
            todo = Todo(title=title, user_id=user_id)
            session.add(todo)
            session.commit()
            session.refresh(todo)
            return [types.TextContent(type="text", text=f"Task '{title}' (ID: {todo.id}) has been added successfully.")]

        elif name == "list_tasks":
            status_filter = arguments.get("status", "all")
            query = select(Todo).where(Todo.user_id == user_id)
            if status_filter == "pending":
                query = query.where(Todo.status == "Incomplete")
            elif status_filter == "completed":
                query = query.where(Todo.status == "Complete")
            
            todos = session.exec(query).all()
            if not todos:
                return [types.TextContent(type="text", text="You have no tasks matching the filter.")]
            
            output = "Your tasks:\n"
            for t in todos:
                output += f"- [{t.id}] {t.title} ({t.status})\n"
            return [types.TextContent(type="text", text=output)]

        elif name == "complete_task":
            task_id = arguments["task_id"]
            todo = session.get(Todo, task_id)
            if not todo or todo.user_id != user_id:
                return [types.TextContent(type="text", text=f"Task with ID {task_id} not found.")]
            todo.status = "Complete"
            session.add(todo)
            session.commit()
            return [types.TextContent(type="text", text=f"Task '{todo.title}' marked as complete.")]

        elif name == "delete_task":
            task_id = arguments["task_id"]
            todo = session.get(Todo, task_id)
            if not todo or todo.user_id != user_id:
                return [types.TextContent(type="text", text=f"Task with ID {task_id} not found.")]
            title = todo.title
            session.delete(todo)
            session.commit()
            return [types.TextContent(type="text", text=f"Task '{title}' has been deleted.")]

        elif name == "update_task":
            task_id = arguments["task_id"]
            todo = session.get(Todo, task_id)
            if not todo or todo.user_id != user_id:
                return [types.TextContent(type="text", text=f"Task with ID {task_id} not found.")]
            
            if "title" in arguments:
                todo.title = arguments["title"]
            if "status" in arguments:
                todo.status = arguments["status"]
            
            session.add(todo)
            session.commit()
            session.refresh(todo)
            return [types.TextContent(type="text", text=f"Task {task_id} updated successfully.")]
        
        else:
            raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="todo-agent",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
