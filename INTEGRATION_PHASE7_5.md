# Phase 7.5 — Leave Approval Workflow

This package adds approval/rejection workflow to the existing Leave module.

## 1. Update `app/models/leave.py`
Add these imports/fields to the existing `Leave` model:

```python
from sqlalchemy import Text
```

Inside `class Leave(Base)`:

```python
approver_user_id: Mapped[int | None] = mapped_column(
    ForeignKey("users.id"), nullable=True, index=True
)
approval_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
```

## 2. Update `app/schemas/leave.py`
Add to `LeaveResponse`:

```python
approver_user_id: int | None = None
approval_comment: str | None = None
```

## 3. Update `app/api/v1/router.py`
Add:

```python
from app.api.v1.leave_approval import router as leave_approval_router
```

Then:

```python
router.include_router(leave_approval_router)
```

## 4. Copy the new files
- `app/schemas/leave_approval.py`
- `app/services/leave_approval_service.py`
- `app/api/v1/leave_approval.py`
- `alembic/versions/0004_add_leave_approval_fields.py`

## 5. Apply migration
```powershell
alembic upgrade head
```

## 6. Start API
```powershell
uvicorn app.main:app --reload
```

## 7. Swagger endpoints
- PATCH `/api/v1/leaves/{leave_id}/approve`
- PATCH `/api/v1/leaves/{leave_id}/reject`

Both require the existing authentication dependency and therefore a Bearer token.

## Important
This phase adds the workflow mechanics. Full role/manager authorization rules should be hardened in the authorization/security phase and full testing phase. Do not test approval until a leave request exists and you have a valid authenticated user.
