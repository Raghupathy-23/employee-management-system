# Employee Management System — Notification + Frontend Cleanup + Testing Bundle

Single integration bundle for the next development checkpoint.

## Included

### 1. Notification foundation
- Persistent in-app notification model
- Alembic migration `0006_create_notifications`
- Notification service
- Authenticated notification APIs
- Unread count
- Mark one/all as read
- Notification producer guidance for leave workflows

### 2. Frontend integration cleanup
- Notification API service
- Notification bell with unread badge and polling
- Full Notifications page
- Notification styling
- Attendance/Leave employee lookup regression fix: `limit: 100`
- Integration snippets for `App.jsx` and `Layout.jsx`

### 3. Testing starter suite
- Health/readiness regression tests
- Auth boundary test
- Pagination regression tests
- Notification schema test
- Notification API authentication tests
- Frontend employee lookup limit regression test
- Manual smoke checklist

## Integration model

This is an **overlay package**, not a replacement for the complete project. Copy the files into the existing Employee Management System root and follow:

1. `docs/INTEGRATION_BACKEND.md`
2. `docs/INTEGRATION_FRONTEND.md`
3. `docs/NOTIFICATION_PRODUCERS.md`
4. `docs/TESTING.md`

## Important migration note

The migration assumes the current project head is `0005_create_audit_logs`. If your local repository has a different head, update the `down_revision` in `0006_create_notifications.py` before running Alembic.

## Recommended order

```text
Backend notification migration/API
        ↓
Frontend notification integration
        ↓
Frontend cleanup/regression fix
        ↓
pytest
        ↓
Manual smoke test
```
