# Production-readiness pass

This package has been cleaned and upgraded for portfolio/interview presentation.

## Completed

- Removed local `.venv`, `node_modules`, `.env`, caches and generated Python bytecode.
- Added configurable CORS and environment validation.
- Removed login debug output and sensitive authentication logging.
- Added server-side RBAC for sensitive operations.
- Added manager/direct-report access checks.
- Added role administration API required by the React Roles page.
- Added audit-log API and mutation audit events.
- Added leave approval notifications.
- Fixed employee search against a non-existent `Employee.email` field.
- Added leave approval fields to the ORM model.
- Fixed frontend leave approval payload naming.
- Improved health/readiness behavior.
- Added Docker startup migrations and idempotent role seeding.
- Added production-style React/Nginx Docker image.
- Added `.dockerignore` and environment-driven Docker ports.
- Added isolated API smoke-test configuration.
- Added Ruff configuration and GitHub Actions CI.
- Reworked README and added architecture, deployment, frontend, testing and interview documentation.

## Verification performed in this package

- Python AST parsing passed.
- Python bytecode compilation passed.
- Docker Compose YAML parsed successfully.

## Local verification before publishing

Run these commands on a machine with internet access and Docker:

```powershell
pip install -r requirements.txt
pytest
ruff check app tests scripts
npm ci
npm run build
docker compose up --build -d
docker compose ps
```

The sandbox used to prepare this package did not have network access to install the missing Python packages (`pymysql`, `python-jose`, `pwdlib`), so a full dependency-backed pytest run could not be executed here. The repository's CI workflow installs the declared dependencies and runs the complete checks on GitHub Actions.

## Public deployment

The project is **deployment-ready**, but a public live URL cannot be created from this package alone because it requires an external hosting account, managed MySQL instance and production secrets. Follow `docs/DEPLOYMENT.md` after uploading the repository to GitHub.
