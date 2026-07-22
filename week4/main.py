from fastapi import FastAPI, Header, HTTPException, Request, Depends
from typing import Optional
from supabase_client import supabase
from auth import router as auth_router
from dependencies import get_current_user

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


@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
def protected_profile(user=Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "created_at": user.created_at}


@app.get("/protected/dashboard")
def protected_dashboard(user=Depends(get_current_user)):
    return {"message": "Welcome to your dashboard", "email": user.email}
