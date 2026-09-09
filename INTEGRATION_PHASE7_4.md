# Phase 7.4 — Leave Model and API

This package continues the planned project tracker order.

Completed before this package:
- 7.1 Department management
- 7.2 Role management foundation
- 7.3 Attendance model and API

This package implements:
- 7.4 Leave model and API — create leave requests and view history

Do not implement approval/balance logic yet. Those are the next planned Phase 7 tasks:
- 7.5 Leave approval workflow
- 7.6 Leave balance rules

## Copy these files into the existing project

- `app/models/leave.py`
- `app/schemas/leave.py`
- `app/repositories/leave_repository.py`
- `app/services/leave_service.py`
- `app/api/v1/leaves.py`
- `alembic/versions/0003_create_leave_table.py`

## Add to `app/db/base.py`

```python
from app.models.leave import Leave  # noqa: F401
```

Keep the existing imports for Department, Role, User, Employee and Attendance.

## Add to `app/api/v1/router.py`

```python
from app.api.v1.leaves import router as leaves_router
```

Then include it with the other v1 routers:

```python
api_router.include_router(leaves_router)
```

## Migration

Do this later with the complete testing pass, consistent with the current workflow:

```powershell
alembic upgrade head
```

## Expected endpoints

- POST `/api/v1/leaves`
- GET `/api/v1/leaves`
- GET `/api/v1/leaves/{leave_id}`
- PATCH `/api/v1/leaves/{leave_id}`
- DELETE `/api/v1/leaves/{leave_id}`

Approval and balance calculations are intentionally not included in this package yet.
