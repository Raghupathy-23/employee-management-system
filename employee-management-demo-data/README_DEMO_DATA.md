# Employee Management System — Demo Data

This package provides realistic demo data for the current Employee Management System.
It is designed to demonstrate the existing application without changing the schema or creating another Alembic migration.

## What it seeds

- Roles: ADMIN, HR, HR_MANAGER, MANAGER, EMPLOYEE
- Demo users
- Four departments
- Six employees with manager relationships
- Attendance records covering PRESENT, HALF_DAY, ABSENT and ON_LEAVE
- Leave requests covering PENDING, APPROVED, REJECTED and CANCELLED
- In-app notifications, including unread notifications for the bell
- A small audit-log history

## Before running

Make sure the database is already migrated to the current head:

```powershell
alembic upgrade head
```

If you use Docker for the backend/database, make sure the MySQL container is running and the notification migration (`0006_create_notifications`) has already been applied.

## Demo login accounts

| Role | Email | Password |
|---|---|---|
| ADMIN | admin@example.com | Admin@123 |
| HR | hr@example.com | Hr@123 |
| HR_MANAGER | hr.manager@example.com | Manager@123 |
| MANAGER | manager@example.com | Employee@123 |
| EMPLOYEE | employee1@example.com | Employee@123 |
| EMPLOYEE | employee2@example.com | Employee@123 |

`admin@example.com` may already exist in your database. The SQL uses `INSERT IGNORE`, so it will not overwrite an existing admin account.

## Run with Docker MySQL

The exact database user/password depends on your `.env` and `docker-compose.yml`.

Typical pattern:

```powershell
docker compose exec -T mysql mysql -u<MYSQL_USER> -p<MYSQL_PASSWORD> employee_management < demo_data.sql
```

If your MySQL container/service is named differently, use the service name from:

```powershell
docker compose ps
```

If you prefer to open a MySQL shell first:

```powershell
docker compose exec mysql mysql -u<MYSQL_USER> -p employee_management
```

Then paste the contents of `demo_data.sql`.

## Run from a local MySQL client

```powershell
mysql -u <MYSQL_USER> -p employee_management < demo_data.sql
```

## Verify

After seeding, open:

```text
http://127.0.0.1:8000/docs
```

and the frontend:

```text
http://localhost:5174
```

Recommended demo sequence:

1. Login as `admin@example.com`.
2. Open Dashboard.
3. Open Employees and review the six employee records.
4. Open Departments.
5. Open Roles.
6. Open Attendance and review the mixed attendance statuses.
7. Open Leave and review pending/approved/rejected/cancelled requests.
8. Open Notifications and verify unread notifications.
9. Click the notification bell and verify the unread badge.
10. Mark one notification as read.
11. Mark all notifications as read.
12. Login as `manager@example.com` and verify manager-facing leave data/approval controls.
13. Login as `employee1@example.com` and verify the employee experience and notification data.

## Important

This is demo/portfolio data. Do not use these passwords or records in production.

The seed is intentionally additive. It does not drop tables or delete existing data.
