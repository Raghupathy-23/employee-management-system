# Employee Management System API

A production-style Employee Management System built with FastAPI.

## Phase 3 - Project Setup

Current foundation includes:

- FastAPI application
- Versioned API structure (`/api/v1`)
- Application configuration using Pydantic Settings
- Health endpoint
- System information endpoint
- Layered package structure ready for database, services, repositories, schemas, and models

## Run locally

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/api/v1/system/info
- http://127.0.0.1:8000/docs

Database implementation starts in Phase 4.
