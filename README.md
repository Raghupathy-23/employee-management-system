# Employee Management System API

## Phase 5 - Authentication and Authorization

This phase adds:

- JWT access-token authentication
- Secure password hashing with Argon2
- OAuth2 password flow for Swagger
- Current-user endpoint
- Role-aware dependency
- MySQL Docker Compose environment
- Default role seeding script

## Start MySQL and API

```powershell
docker compose up -d mysql
```

Create `.env` from `.env.example` and verify `DATABASE_URL`.

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the Phase 4 migration:

```powershell
alembic upgrade head
```

Seed default roles:

```powershell
python -m scripts.seed_roles
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

## Authentication

Open:

```text
http://127.0.0.1:8000/docs
```

The login endpoint is:

```text
POST /api/v1/auth/login
```

It expects OAuth2 form fields:

- username = email
- password = password

Then use the returned bearer token with:

```text
GET /api/v1/auth/me
```

## Important

Do not commit `.env`, database passwords, or production JWT secrets.
The Docker Compose credentials are development-only placeholders and must be changed for real deployment.
