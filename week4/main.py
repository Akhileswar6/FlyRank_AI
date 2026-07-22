from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional
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

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile")
def protected_profile(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=401, content={"error": "Access token required"})
    token = auth_header.split("Bearer ")[1]
    return {"message": "Token received"}
