# Integration — Phases 8 and 9

This package intentionally skips the remaining HR/business-module phase for now.
It completes the tracker items needed before frontend work: Production Backend Features and Testing & Quality.

## 8.3 Audit logging

1. Copy `app/models/audit_log.py`.
2. Add this import to `app/db/base.py`:
   `from app.models.audit_log import AuditLog`
3. Add `app/services/audit_service.py`.
4. Add the migration `0003_create_audit_logs.py` to `alembic/versions/`.
5. Run:
   `alembic upgrade head`
6. Record important create/update/delete/approve/reject actions from the corresponding services using `AuditService.record(...)`.

Example:
```python
AuditService().record(
    db,
    action="LEAVE_APPROVED",
    user_id=current_user.id,
    resource="leave",
    resource_id=leave.id,
)
```

## 8.4 Pagination utility

Copy:
- `app/utils/pagination.py`
- `app/schemas/pagination.py`

The utility is additive. Existing list endpoints can be converted one at a time without breaking the current API.

## 8.5 Health/readiness

Copy `app/api/v1/health.py` and include its router in `app/api/v1/router.py`:

```python
from app.api.v1.health import router as health_router
router.include_router(health_router)
```

This adds `/api/v1/health` and `/api/v1/health/readiness`.

## 8.6 Notification foundation

Copy:
- `app/schemas/notification.py`
- `app/services/notification_service.py`

No external email provider is added yet. The service is a simple interface so a provider can be introduced later.

## Phase 9 — automated testing

Copy the `tests/` folder. The tests cover:
- health/readiness
- pagination behavior
- notification service contract
- protected authentication route

Run:
```powershell
pytest -q
```

Before running integration tests against real data, use a dedicated test database. Do not point destructive tests at a production database.

## Full development verification

After integration:
```powershell
alembic current
alembic upgrade head
uvicorn app.main:app --reload
pytest -q
```

Then open Swagger at `/docs` and verify the health endpoints.
