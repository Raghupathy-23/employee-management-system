# Changelog

## 1.0.0 - Production-readiness pass

- Added server-side role-based access control to sensitive resources.
- Added role administration API to match the React roles UI.
- Added audit-log read API and audit events for important mutations.
- Added manager/direct-report authorization to leave approval and employee access.
- Added leave approval fields to the SQLAlchemy model.
- Fixed employee search to use real employee fields.
- Fixed leave approval request payload mismatch in the frontend.
- Removed authentication debug prints and sensitive login logging.
- Improved 500-error responses so internal exception details are not exposed.
- Made CORS configurable through environment variables.
- Added health/readiness checks with database connectivity validation.
- Added SQLite-isolated API smoke-test configuration.
- Added Ruff configuration and GitHub Actions CI.
- Added production-style frontend Docker image and Nginx SPA routing.
- Added Docker startup migrations.
- Removed committed virtual environments, dependency caches, `.env`, and generated Python files from the portfolio package.
- Reworked documentation for interview/recruiter readability.
