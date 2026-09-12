# Backend integration — Notification + Testing

This is an overlay for the existing Employee Management System backend. It does not replace the existing project.

## 1. Copy files

Copy the contents of `app/`, `alembic/versions/`, and `tests/` into the existing backend root, preserving folders.

## 2. Register the model

Add:

```python
from app.models.notification import Notification
```

to `app/models/__init__.py` and, if your Alembic base imports models explicitly, to `app/db/base.py` as well.

## 3. Register the API router

In `app/api/v1/router.py` add:

```python
from app.api.v1.notifications import router as notifications_router
router.include_router(notifications_router)
```

## 4. Run the migration

```powershell
alembic upgrade head
```

The migration is intentionally linear and starts from the current project head `0005_create_audit_logs`.

## 5. Notification API

- `GET /api/v1/notifications`
- `GET /api/v1/notifications/unread-count`
- `PATCH /api/v1/notifications/{notification_id}/read`
- `PATCH /api/v1/notifications/read-all`

All notification reads are scoped to the authenticated user.

## 6. Creating notifications from business logic

Example:

```python
from app.schemas.notification import NotificationCreate
from app.services.notification_service import NotificationService

NotificationService().create(
    db,
    NotificationCreate(
        user_id=employee_user_id,
        notification_type="LEAVE",
        title="Leave request updated",
        message="Your leave request was approved.",
        link=f"/leaves/{leave.id}",
    ),
)
```

For the first pass, notifications are persisted in-app. Email/push delivery can be added later without changing the notification API.

## 7. Important

The migration assumes the current Alembic head is `0005_create_audit_logs`. Do not create a second head. If your local migration numbering differs, update `down_revision` to the actual current head before running Alembic.
