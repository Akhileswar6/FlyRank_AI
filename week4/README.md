# Auth API with Supabase

This is a secure API built with FastAPI and Supabase that handles user authentication (Sign Up, Log In, Log Out) and protects specific routes.

## Setup

1. Copy `.env.example` to `.env` and fill in your Supabase credentials:
   ```bash
   cp .env.example .env
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   fastapi dev main.py
   # or
   uvicorn main:app --reload
   ```

## API Reference

| Route | Purpose | Auth Required |
| ----- | ------- | ------------- |
| `POST /auth/signup` | Create a new user account | No |
| `POST /auth/login` | Authenticate & return a JWT | No |
| `POST /auth/logout` | End the user's session | Yes (Bearer Token) |
| `GET /protected/profile` | Read private profile data | Yes (Bearer Token) |
| `GET /public/info` | Read public open data | No |

## Swagger UI

You can view the interactive documentation and test the endpoints by navigating to `/docs` when the server is running. Use the **Authorize** padlock to authenticate with your JWT.
