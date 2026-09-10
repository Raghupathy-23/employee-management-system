# Changelog

## 7.6 — Leave balance

- Added simple yearly leave allowances.
- Calculates approved and pending days from existing Leave records.
- Exposes a balance endpoint.
- Prevents new paid leave requests from exceeding available balance.
- No new database table or migration.

## 8.1 — Centralized exception handling

- Added a small `AppException` type.
- Added consistent handlers for application errors, validation errors, database integrity conflicts, and unexpected errors.
- Existing explicit `HTTPException` routes continue to work normally.

## 8.2 — Application logging

- Added one basic logging configuration.
- Added request method/path/status/duration logging.
- Unexpected errors are logged with tracebacks.

## Scope deliberately excluded

- Full test suite: Phase 9.
- Frontend: Phase 10.
- Notifications: Phase 8.6.
- Audit logging: Phase 8.3.
- Pagination utility: Phase 8.4.
- Health/readiness work: Phase 8.5.
