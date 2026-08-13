import sqlite3
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import get_connection, init_database

app = FastAPI(title="DevOps Basics API")


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://devops-basics-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Database
# -----------------------------
def get_db():
    connection = get_connection()

    try:
        yield connection
    finally:
        connection.close()


DbConnection = Annotated[
    sqlite3.Connection,
    Depends(get_db),
]

init_database()

# -----------------------------
# Request models
# -----------------------------

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    completed: bool


# -----------------------------
# GET /api/tasks
# -----------------------------

@app.get("/api/tasks")
def get_tasks(connection: DbConnection):

    rows = connection.execute("""
        SELECT id, title, completed
        FROM tasks
        ORDER BY id DESC
    """).fetchall()

    return [dict(row) for row in rows]


# -----------------------------
# POST /api/tasks
# -----------------------------

@app.post("/api/tasks", status_code=201)
def create_task(
    task: TaskCreate,
    connection: DbConnection,
):

    cursor = connection.execute(
        """
        INSERT INTO tasks (title)
        VALUES (?)
        """,
        (task.title,),
    )

    connection.commit()

    task_id = cursor.lastrowid

    row = connection.execute(
        """
        SELECT id, title, completed
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    ).fetchone()

    return dict(row)


# -----------------------------
# PUT /api/tasks/{task_id}
# -----------------------------

@app.put("/api/tasks/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    connection: DbConnection,
):

    cursor = connection.execute(
        """
        UPDATE tasks
        SET title = ?, completed = ?
        WHERE id = ?
        """,
        (
            task.title,
            int(task.completed),
            task_id,
        ),
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    row = connection.execute(
        """
        SELECT id, title, completed
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    ).fetchone()

    return dict(row)


# -----------------------------
# DELETE /api/tasks/{task_id}
# -----------------------------

@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    connection: DbConnection,
):

    cursor = connection.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )