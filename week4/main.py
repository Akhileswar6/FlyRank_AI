from fastapi import FastAPI
from supabase_client import supabase
from auth import router as auth_router

app = FastAPI(
    title="Task Auth API",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Authentication API for user signup and login using Supabase.",
    }

