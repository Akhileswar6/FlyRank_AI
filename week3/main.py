from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import init_db, get_db_connection

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks(search: str = None, done: bool = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM tasks"
    conditions = []
    params = []
    if search is not None:
        conditions.append("title ILIKE %s")
        params.append(f"%{search}%")
    if done is not None:
        conditions.append("done = %s")
        params.append(True if done else False)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY title ASC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return row

class TaskCreate(BaseModel):
    title: str
    done: bool = False

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *", (task.title, False))
    new_task = cursor.fetchone()
    conn.commit()
    conn.close()
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    # For compatibility, keeping just title update, or using done if available.
    # The instructions mentioned `done = $2`, so we will default it to False for now
    # if not provided by TaskCreate.
    cursor.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *", (task.title, getattr(task, 'done', False), task_id))
    updated_task = cursor.fetchone()
    conn.commit()
    conn.close()
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return None

@app.get("/stats")
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM tasks")
    total_tasks = cursor.fetchone()["count"]
    cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE done = 1")
    completed_tasks = cursor.fetchone()["count"]
    conn.close()
    return {
        "total": total_tasks,
        "completed": completed_tasks,
        "pending": total_tasks - completed_tasks
    }
