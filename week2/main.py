from fastapi import FastAPI
from data import tasks

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