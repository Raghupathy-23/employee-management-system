# Phase 9 — Testing starter suite

The bundle includes focused regression tests for:

- health and readiness endpoints
- authentication protection
- pagination helper
- notification request schema
- notification authentication boundaries
- frontend employee lookup limit regression

## Run

From the existing backend project root:

```powershell
pytest -q
```

For only the new notification/regression tests:

```powershell
pytest -q tests/test_notification_schema.py tests/test_notification_api_auth.py tests/test_frontend_cleanup.py
```

## Test order for the full project

1. Start MySQL/Docker.
2. Run `alembic upgrade head`.
3. Start the FastAPI backend.
4. Run `pytest -q`.
5. Start the Vite frontend.
6. Perform the manual smoke checklist below.

## Manual smoke checklist

### Authentication
- Login with the development admin account.
- Refresh the browser and confirm the session remains available.
- Logout and confirm protected routes redirect to login.

### Employee/HR UI
- Dashboard loads.
- Departments loads.
- Employees loads.
- Attendance loads employee choices without a `limit > 100` validation error.
- Leave loads employee choices without a `limit > 100` validation error.
- Roles is visible to ADMIN only.
- Leave approve/reject actions respect the frontend role gate and backend authorization.

### Notifications
- Open the notification bell.
- Confirm unread count loads.
- Confirm notification list loads.
- Mark one notification read.
- Mark all notifications read.
- Open `/notifications` and test the unread-only filter.
- Confirm another user's notification cannot be read through the current user's endpoint.

## Important

The tests are intentionally additive. They do not replace the comprehensive Phase 9 test plan. Full workflow, repository/service, authorization, and coverage tests should be expanded after the application code is integrated and the test database configuration is confirmed.
