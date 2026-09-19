# Testing Strategy

## Fast feedback

```powershell
pytest
ruff check app tests scripts
npm ci
npm run build
```

## Current test categories

- Authentication protection
- Role endpoint protection
- Health/readiness behavior
- Notification endpoint protection
- Notification service contract
- Schema validation
- Pagination behavior
- JWT token validation
- Frontend/API request-limit regression

## Test environment

API smoke tests use SQLite so a contributor does not need a local MySQL server just to run the basic suite. Production and Docker configuration continue to use MySQL.

## Future test coverage

The next high-value tests should be MySQL integration tests for:

- leave balance calculations
- overlapping leave requests
- manager-only approval
- employee ownership boundaries
- notification persistence
- audit-log persistence
- employee/department CRUD transactions
