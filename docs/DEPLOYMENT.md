# Deployment Guide

The repository is prepared for deployment, but a real public deployment requires an external hosting account, a managed MySQL database and production environment variables.

## Production checklist

1. Provision a managed MySQL 8.x database.
2. Deploy the FastAPI `Dockerfile`.
3. Set `ENVIRONMENT=production`.
4. Set a strong random `SECRET_KEY`.
5. Set `DATABASE_URL` to the managed MySQL connection string.
6. Set `CORS_ORIGINS` to the exact frontend origin(s).
7. Set `VITE_API_BASE_URL` to the public API URL plus `/api/v1` when building the frontend.
8. Run the API container with `RUN_MIGRATIONS=true` for the initial deployment.
9. Create an admin account with `create_admin.py` or an equivalent secure provisioning process.
10. Load only synthetic/demo data into a portfolio environment.
11. Enable HTTPS at the hosting layer.
12. Confirm `/health` and `/health/readiness` before sharing the URL.

## Recommended public portfolio layout

```text
Browser
  │
  ├── HTTPS → React/Nginx frontend
  │
  └── HTTPS → FastAPI API → Managed MySQL
```

## Environment variables

Backend:

```text
APP_NAME
ENVIRONMENT
DATABASE_URL
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
JWT_ALGORITHM
CORS_ORIGINS
LOG_LEVEL
```

Frontend build:

```text
VITE_API_BASE_URL
```

Never commit `.env` or production credentials.

## Demo access

For an interview demo, create synthetic accounts for ADMIN, HR, MANAGER and EMPLOYEE roles. Do not use personal, employer or real employee information.
