from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import init_db, get_db_connection

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Finish assignment", "done": False},
    {"id": 3, "title": "Clean the room", "done": True}
]

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
        conditions.append("title LIKE ?")
        params.append(f"%$search%")
    if done is not None:
        conditions.append("done = ?")
        params.append(1 if done else 0)
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
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return row

class TaskCreate(BaseModel):
    title: str

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
    new_task = {"id": len(tasks) + 1, "title": task.title, "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = task.title
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
