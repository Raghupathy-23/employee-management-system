# Architecture Notes

## Backend layers

```text
Router / API
    ↓
Dependencies (authentication + authorization)
    ↓
Service Layer
    ↓
Repository Layer
    ↓
SQLAlchemy Models
    ↓
MySQL
```

### API layer

Responsible for:

- HTTP routes and status codes
- dependency injection
- authentication/authorization dependencies
- request/response schemas
- translating business exceptions into HTTP responses

### Service layer

Responsible for business rules:

- employee uniqueness
- attendance duplicate prevention
- leave balance calculation
- leave overlap validation
- leave approval authorization
- notifications
- audit recording

### Repository layer

Responsible for database queries and persistence operations. This keeps SQLAlchemy query details out of HTTP handlers and business workflows.

## Security model

JWT contains a user subject and role claim, but authorization is based on the currently loaded user and role from the database. This avoids trusting stale role information in a token after a role change.

## Data model

```text
Role 1 ─── * User 1 ─── 0..1 Employee
                         │
                         ├── * Attendance
                         ├── * Leave
                         └── manager_id ──> Employee

Department 1 ─── * Employee

User 1 ─── * Notification
User 1 ─── * AuditLog
Leave * ─── 0..1 User (approver)
```
