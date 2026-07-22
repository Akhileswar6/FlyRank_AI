from fastapi import FastAPI
from supabase_client import supabase

app = FastAPI(
    title="Task Auth API",
    version="1.0.0",
)

@app.get("/")
def home():
    return {
        "message": "FastAPI connected to Supabase successfully!"
    }
