from fastapi import FastAPI, HTTPException
from data import tasks
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints":[
            "/tasks"
        ]
    }

@app.get("/health")
def read_health():
    return {"status": "ok"}



@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail="Task not found")        


class TaskCreate(BaseModel):
    title: str

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")
    
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

