# DevOps Basics

A small end-to-end educational web application designed to learn the fundamentals of **CI/CD and DevOps** step by step.

The application is intentionally simple: users can create, edit, view, and delete tasks. The goal is not to build a complex product, but to understand how a real application moves from **local development → testing → CI → deployment → CD → production**.

---

## Project Goals

This project teaches the basic DevOps workflow around a simple full-stack application.

We start with a small application and progressively introduce:

* Frontend development
* Backend API development
* Database persistence
* Automated testing
* Code quality checks
* Git and GitHub
* Continuous Integration (CI)
* Continuous Deployment (CD)
* Cloud deployment
* Environment separation
* Docker
* Docker Compose
* Container-based deployment
* Kubernetes concepts later

The project deliberately avoids unnecessary complexity.

---

## Application

The application is a simple task manager.

Users can:

* View tasks
* Create tasks
* Edit tasks
* Delete tasks

The frontend communicates with the backend through HTTP requests.

---

## Technology Stack

### Frontend

* HTML
* CSS
* JavaScript
* Browser `fetch()` API

No frontend framework is used.

### Backend

* Python
* FastAPI
* Pydantic
* SQLite

### Testing

* pytest
* FastAPI TestClient

### Code Quality

* Ruff

### Version Control

* Git
* GitHub

### CI/CD

* GitHub Actions
* Render

### Current Hosting

* Frontend: Render Static Site
* Backend: Render Web Service
* Database: SQLite

Docker and Kubernetes are planned as later learning stages.

---

## Project Structure

```text
devops-basics/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── database.py
│   │
│   ├── tests/
│   │   └── test_tasks.py
│   │
│   ├── requirements.txt
│   └── database.db
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
└── README.md
```

---

# Architecture

The application consists of three main layers:

```text
Browser
   │
   │ HTTP / HTTPS
   ▼
FastAPI
   │
   │ SQL
   ▼
SQLite
```

The frontend is a separate application from the backend.

In production:

```text
User
 │
 ▼
Render Static Site
 │
 │ HTTPS / fetch()
 ▼
Render Web Service
 │
 ▼
FastAPI
 │
 ▼
SQLite
```

---

# Frontend

The frontend is intentionally written using only standard web technologies:

```text
HTML
CSS
JavaScript
```

It communicates with the API using `fetch()`.

Example:

```javascript
fetch("https://devops-basics-l2bn.onrender.com/api/tasks");
```

The frontend does not directly access SQLite.

Instead:

```text
Frontend
   ↓ HTTP
FastAPI
   ↓ SQL
SQLite
```

This demonstrates the basic client/server architecture used by much larger applications.

---

# Backend

The backend is a FastAPI application.

The API provides CRUD operations for tasks.

## API Endpoints

| Operation   | Method   | Endpoint          |
| ----------- | -------- | ----------------- |
| List tasks  | `GET`    | `/api/tasks`      |
| Create task | `POST`   | `/api/tasks`      |
| Update task | `PUT`    | `/api/tasks/{id}` |
| Delete task | `DELETE` | `/api/tasks/{id}` |

---

## Example Task

```json
{
  "id": 1,
  "title": "Learn DevOps",
  "completed": false
}
```

---

# Database

SQLite is used because it is extremely simple and requires no separate database server.

The basic flow is:

```text
FastAPI
   ↓
sqlite3
   ↓
database.db
```

The database contains the `tasks` table.

SQLite is appropriate for this educational project because the goal is learning the application and DevOps workflow rather than database administration.

A production system would commonly use a server-based database such as PostgreSQL.

---

# Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/Education-materials/devops-basics.git
cd devops-basics
```

---

# Backend Setup

Move into the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI also provides interactive API documentation:

```text
http://localhost:8000/docs
```

---

# Start the Frontend

Open another terminal.

From the project root:

```bash
cd frontend
python3 -m http.server 5173
```

Open:

```text
http://localhost:5173
```

The local frontend communicates with:

```text
http://localhost:8000/api/tasks
```

---

# CORS

Because the frontend and backend are running on different origins during development, the backend enables CORS.

For example:

```text
Frontend
http://localhost:5173

Backend
http://localhost:8000
```

The browser treats these as different origins.

FastAPI therefore allows the frontend origin through `CORSMiddleware`.

In production, the Render frontend origin is also allowed.

---

# Testing

The project uses `pytest`.

From the `backend` directory:

```bash
python -m pytest
```

The tests verify the API behavior, including task creation, reading, updating, and deletion.

Example:

```text
5 passed
```

Testing is important because CI will run these tests automatically whenever changes are pushed to GitHub.

---

# Code Quality

Ruff is used to check the Python code.

Run:

```bash
python -m ruff check .
```

Ruff helps detect:

* Code-quality problems
* Common Python mistakes
* Import problems
* Style issues

The same check is executed by GitHub Actions.

---

# Continuous Integration

The CI workflow is located at:

```text
.github/workflows/ci.yml
```

Its purpose is to automatically verify the code whenever changes are pushed.

The basic pipeline is:

```text
git push
   ↓
GitHub
   ↓
GitHub Actions
   ↓
Install dependencies
   ↓
Ruff
   ↓
pytest
   ↓
CI result
```

If a test fails:

```text
pytest ❌
   ↓
CI fails
```

The change should not proceed to deployment.

---

# Continuous Deployment

The CD workflow is located at:

```text
.github/workflows/cd.yml
```

The deployment workflow runs after the CI workflow succeeds.

The pipeline is:

```text
git push
   ↓
CI
   ├── Ruff
   └── pytest
   ↓
✅ CI passes
   ↓
CD
   ├── Deploy backend
   └── Deploy frontend
   ↓
Render
   ↓
Production
```

The Render deployment hooks are stored as **GitHub Actions Secrets**.

They are not stored directly in the repository.

Example secret names:

```text
RENDER_BACKEND_DEPLOY_HOOK
RENDER_FRONTEND_DEPLOY_HOOK
```

---

# Why Separate CI and CD?

CI and CD have different responsibilities.

## CI

Continuous Integration answers:

> "Is the code safe to integrate?"

It performs checks such as:

```text
Lint
Tests
Build checks
```

## CD

Continuous Deployment answers:

> "Should the successfully tested code be deployed?"

It performs:

```text
Deployment
```

Therefore:

```text
CI = verify
CD = deploy
```

---

# Deployment

The project is deployed using Render.

There are two Render services.

## Frontend

The frontend is deployed as a:

```text
Static Site
```

It serves:

```text
HTML
CSS
JavaScript
```

## Backend

The FastAPI application is deployed as a:

```text
Web Service
```

It runs the Python application.

---

# Production Architecture

```text
                       GitHub
                         │
                      git push
                         │
                         ▼
                ┌─────────────────┐
                │ GitHub Actions   │
                │                 │
                │ Ruff            │
                │ pytest          │
                └────────┬────────┘
                         │
                    CI passes
                         │
                         ▼
                ┌─────────────────┐
                │       CD        │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Render Static Site     Render Web Service
            Frontend               FastAPI
              │                     │
              │ HTTPS               │
              └──────────►──────────┘
                                    │
                                    ▼
                                  SQLite
```

---

# Git Workflow

The basic development workflow is:

```text
Make change
    ↓
Run tests locally
    ↓
Run Ruff locally
    ↓
git add
    ↓
git commit
    ↓
git push
    ↓
GitHub Actions
    ↓
CI
    ↓
CD
    ↓
Render
```

Example:

```bash
git add .
git commit -m "Add task editing"
git push
```

---

# CI/CD Failure Behavior

One of the most important lessons in this project is that deployment should depend on successful CI.

If tests pass:

```text
pytest
  ↓
✅
  ↓
CD
  ↓
Deploy
```

If tests fail:

```text
pytest
  ↓
❌
  ↓
CD does not deploy
```

This creates a basic quality gate between development and production.

---

# Educational Progression

The project is intentionally built in stages.

### Stage 1 — HTTP Basics

Learn:

* HTTP
* Requests
* Responses
* JSON
* CRUD
* Frontend `fetch()`

### Stage 2 — Backend

Introduce:

* FastAPI
* REST API
* SQLite
* Database queries
* CORS

### Stage 3 — Testing

Introduce:

* pytest
* API tests
* TestClient

### Stage 4 — Code Quality

Introduce:

* Ruff
* Automated linting

### Stage 5 — Continuous Integration

Introduce:

* GitHub Actions
* Automated tests
* Automated linting

### Stage 6 — Cloud Deployment

Introduce:

* Render
* Static sites
* Web services
* Production environment

### Stage 7 — Continuous Deployment

Introduce:

* `cd.yml`
* Render deploy hooks
* CI → CD dependency
* Automated production deployments

### Stage 8 — Docker

Next, the application will be containerized.

The goal will be to understand:

```text
Application
    ↓
Dockerfile
    ↓
Docker Image
    ↓
Container
```

### Stage 9 — Docker Compose

Later, multiple services can be managed together.

### Stage 10 — Kubernetes

Kubernetes will be introduced only after the concepts of containers, images, networking, services, and deployment are understood.

---

# Why Keep the Project Simple?

Real DevOps systems can involve:

* Docker
* Kubernetes
* Terraform
* Cloud platforms
* Container registries
* Reverse proxies
* Load balancers
* Monitoring
* Logging
* Secrets management
* Message queues
* Multiple databases

Introducing all of these immediately makes it difficult to understand what each component actually does.

This project therefore follows a gradual approach:

```text
Simple application
        ↓
Understand it
        ↓
Test it
        ↓
Automate it
        ↓
Deploy it
        ↓
Containerize it
        ↓
Scale it
```

The objective is **understanding the architecture**, not simply copying a complicated DevOps stack.

---

# Current Status

At the current stage, the project has:

* [x] HTML frontend
* [x] CSS
* [x] JavaScript
* [x] FastAPI backend
* [x] SQLite database
* [x] Create task
* [x] Read tasks
* [x] Edit task
* [x] Delete task
* [x] CORS
* [x] pytest
* [x] Ruff
* [x] GitHub repository
* [x] GitHub Actions CI
* [x] Render backend deployment
* [x] Render frontend deployment
* [x] GitHub Actions CD
* [x] CI → CD deployment gate

## Next Stage

The next major stage is:

```text
Docker
```

After Docker:

```text
Docker Compose
        ↓
Container Registry
        ↓
Container-based CI/CD
        ↓
Kubernetes
```

---

## Main Lesson

The most important concept demonstrated by this project is the complete path from code to production:

```text
Developer
   ↓
Code
   ↓
Git
   ↓
GitHub
   ↓
CI
   ├── Ruff
   └── pytest
   ↓
CD
   ↓
Render
   ↓
Production
```

A small application is enough to learn the fundamentals. Once these concepts are understood, the same ideas can be applied to much larger systems.
