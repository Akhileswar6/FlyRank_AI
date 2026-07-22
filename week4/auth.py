from fastapi import APIRouter, HTTPException, Depends
from schemas import UserSignup, UserLogin
from supabase_client import supabase
from dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", status_code=201)
def signup(user: UserSignup):
    try:
        response = supabase.auth.sign_up(
            {"email": user.email, "password": user.password}
        )
        return {"message": "User signed up successfully.", "user": response.user.email}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": user.email, "password": user.password}
        )

        if response.user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials.")
        return {
            "message": "User logged in successfully.",
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "Bearer",
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.post("/logout", status_code=204)
def logout(user=Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to log out")
    return None
