# Task API - Postgres + Docker Containerized

A simple RESTful CRUD API built using **FastAPI** that manages a to-do list, now powered by a **PostgreSQL database** running in a **Docker container**. This project is part of the **FlyRank Backend Internship – Week 3 Assignment (A3)**.

## What is this?
This project demonstrates how to package a Python API and its database into a shippable stack using Docker Compose. Instead of installing a database on your machine, it spins up a real PostgreSQL server in a container.

---

## Running the App

### 1. Setup Environment Variables
Clone the repo and configure your `.env` file:
```bash
cp week3/.env.example week3/.env
```
*(The `.env` file contains your database connection string and secrets, which are securely ignored by Git)*

### 2. Start the Stack (One Command!)
Run everything with Docker Compose:
```bash
cd week3
docker compose up
```

This will:
- Download the official `postgres` image
- Spin up the database and mount a persistent volume (`taskdata`)
- Build the FastAPI app image from the `Dockerfile`
- Connect them together on an internal network

The API will be available at: `http://127.0.0.1:3000`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API Information |
| GET | `/health` | Health Check |
| GET | `/tasks` | Get All Tasks |
| GET | `/tasks/{id}` | Get Task by ID |
| POST | `/tasks` | Create Task |
| PUT | `/tasks/{id}` | Update Task |
| DELETE | `/tasks/{id}` | Delete Task |
| GET | `/stats` | Task Statistics |

### Testing with `curl`

To fetch all tasks, run:
```bash
curl -i http://localhost:3000/tasks
```
You should see output similar to this:
```http
HTTP/1.1 200 OK
content-length: 98
content-type: application/json
server: uvicorn

[{"id":1,"title":"Buy groceries","done":false},{"id":2,"title":"Finish assignment","done":false},{"id":3,"title":"Clean the room","done":true}]
```

---

## Database Details

- **Engine:** PostgreSQL
- **Persistence:** A Docker volume (`taskdata`) ensures that your rows survive container restarts.
- **Seeding:** The database automatically creates the `tasks` table and seeds 3 initial tasks when it starts for the first time.

### Screenshot
*(Add a screenshot of your Postgres GUI, such as pgAdmin, DBeaver, or psql terminal here)*

---

## Swagger Documentation
Interactive API documentation is available at:
```
http://127.0.0.1:3000/docs
```
