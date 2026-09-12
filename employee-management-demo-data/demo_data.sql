-- Employee Management System - Demo Data
-- Safe seed: adds demo records without deleting existing application data.
-- Run AFTER: alembic upgrade head
-- Passwords for the demo users are documented in README_DEMO_DATA.md.

START TRANSACTION;

-- ============================================================
-- 1. ROLES
-- ============================================================

INSERT IGNORE INTO roles (name, description) VALUES
('ADMIN', 'Full system administration access'),
('HR', 'Human resources operations access'),
('HR_MANAGER', 'HR management and approval access'),
('MANAGER', 'Team management and leave approval access'),
('EMPLOYEE', 'Standard employee access');

-- ============================================================
-- 2. USERS
-- ============================================================
-- Argon2id hashes are compatible with the project's pwdlib setup.

INSERT IGNORE INTO users
    (email, password_hash, role_id, is_active, created_at, updated_at)
VALUES
(
    'admin@example.com',
    '$argon2id$v=19$m=65536,t=3,p=4$2KHJreag0tJg82gAGujZig$/ubYI5d7l+xNo7whZrfaHlbjXt/l7sW2crcYr+IGf1w',
    (SELECT id FROM roles WHERE name = 'ADMIN'),
    TRUE, NOW(), NOW()
),
(
    'hr@example.com',
    '$argon2id$v=19$m=65536,t=3,p=4$99jgKKaZW38/pBTikFlE0w$MufQdIs7u8fnr4YrawqCDCWnvH9qPl5AnKwc8Qc5LVc',
    (SELECT id FROM roles WHERE name = 'HR'),
    TRUE, NOW(), NOW()
),
(
    'hr.manager@example.com',
    '$argon2id$v=19$m=65536,t=3,p=4$qVHonfHSzNCIhmnStKqV+Q$Hfah/na1SmC0v3JEyA8C8vqnwGq/0yU/0PEDGgZotmw',
    (SELECT id FROM roles WHERE name = 'HR_MANAGER'),
    TRUE, NOW(), NOW()
),
(
    'manager@example.com',
    '$argon2id$v=19$m=65536,t=3,p=4$hlBSpjO7y1dD0qqcAxJwpw$vGitNMfIAN1dRd+9ov+spWrp1nzRVNx0SL0JwV9sNwM',
    (SELECT id FROM roles WHERE name = 'MANAGER'),
    TRUE, NOW(), NOW()
),
(
    'employee1@example.com',
    '$argon2id$v=19$m=65536,t=3,p=4$hlBSpjO7y1dD0qqcAxJwpw$vGitNMfIAN1dRd+9ov+spWrp1nzRVNx0SL0JwV9sNwM',
    (SELECT id FROM roles WHERE name = 'EMPLOYEE'),
    TRUE, NOW(), NOW()
),
(
    'employee2@example.com',
    '$argon2id$v=19$m=65536,t=3,p=4$hlBSpjO7y1dD0qqcAxJwpw$vGitNMfIAN1dRd+9ov+spWrp1nzRVNx0SL0JwV9sNwM',
    (SELECT id FROM roles WHERE name = 'EMPLOYEE'),
    TRUE, NOW(), NOW()
);

-- Correct employee2 password hash. The UPDATE is intentional so the seed
-- remains usable even if the row already existed from an earlier demo run.
UPDATE users
SET password_hash = '$argon2id$v=19$m=65536,t=3,p=4$hlBSpjO7y1dD0qqcAxJwpw$vGitNMfIAN1dRd+9ov+spWrp1nzRVNx0SL0JwV9sNwM',
    is_active = TRUE,
    updated_at = NOW()
WHERE email IN ('employee1@example.com', 'employee2@example.com');

-- ============================================================
-- 3. DEPARTMENTS
-- ============================================================

INSERT IGNORE INTO departments
    (name, description, is_active, created_at, updated_at)
VALUES
('Human Resources', 'People operations, policies and employee support', TRUE, NOW(), NOW()),
('Engineering', 'Software engineering and technical delivery', TRUE, NOW(), NOW()),
('Finance', 'Financial operations, reporting and controls', TRUE, NOW(), NOW()),
('Operations', 'Business operations and administration', TRUE, NOW(), NOW());

-- ============================================================
-- 4. EMPLOYEES
-- ============================================================
-- Insert senior employees first because manager_id references employees.id.

INSERT IGNORE INTO employees
    (employee_code, user_id, department_id, manager_id, first_name, last_name,
     phone, date_of_birth, date_of_joining, designation, employment_status,
     created_at, updated_at)
VALUES
(
    'EMP-001',
    (SELECT id FROM users WHERE email = 'admin@example.com' LIMIT 1),
    (SELECT id FROM departments WHERE name = 'Operations' LIMIT 1),
    NULL,
    'Arun', 'Kumar', '+91-9000000001', '1985-04-12', '2022-01-10',
    'System Administrator', 'ACTIVE', NOW(), NOW()
),
(
    'EMP-002',
    (SELECT id FROM users WHERE email = 'hr.manager@example.com' LIMIT 1),
    (SELECT id FROM departments WHERE name = 'Human Resources' LIMIT 1),
    NULL,
    'Priya', 'Sharma', '+91-9000000002', '1988-08-21', '2021-06-14',
    'HR Manager', 'ACTIVE', NOW(), NOW()
),
(
    'EMP-003',
    (SELECT id FROM users WHERE email = 'manager@example.com' LIMIT 1),
    (SELECT id FROM departments WHERE name = 'Engineering' LIMIT 1),
    NULL,
    'Vikram', 'Rao', '+91-9000000003', '1989-02-17', '2020-09-01',
    'Engineering Manager', 'ACTIVE', NOW(), NOW()
);

-- Resolve manager IDs after the senior employees exist.
-- Using variables avoids MySQL 8.4 error 1093 when inserting into
-- employees while also selecting from employees.

SET @emp002_id = (
    SELECT id FROM employees
    WHERE employee_code = 'EMP-002'
    LIMIT 1
);

SET @emp003_id = (
    SELECT id FROM employees
    WHERE employee_code = 'EMP-003'
    LIMIT 1
);

INSERT IGNORE INTO employees
    (employee_code, user_id, department_id, manager_id, first_name, last_name,
     phone, date_of_birth, date_of_joining, designation, employment_status,
     created_at, updated_at)
VALUES
(
    'EMP-004',
    (SELECT id FROM users WHERE email = 'hr@example.com' LIMIT 1),
    (SELECT id FROM departments WHERE name = 'Human Resources' LIMIT 1),
    @emp002_id,
    'Anita', 'Menon', '+91-9000000004', '1992-11-05', '2023-03-06',
    'HR Executive', 'ACTIVE', NOW(), NOW()
),
(
    'EMP-005',
    (SELECT id FROM users WHERE email = 'employee1@example.com' LIMIT 1),
    (SELECT id FROM departments WHERE name = 'Engineering' LIMIT 1),
    @emp003_id,
    'Rahul', 'Nair', '+91-9000000005', '1995-07-18', '2024-02-12',
    'Software Engineer', 'ACTIVE', NOW(), NOW()
),
(
    'EMP-006',
    (SELECT id FROM users WHERE email = 'employee2@example.com' LIMIT 1),
    (SELECT id FROM departments WHERE name = 'Engineering' LIMIT 1),
    @emp003_id,
    'Meera', 'Iyer', '+91-9000000006', '1996-12-02', '2024-05-20',
    'Software Engineer', 'ON_LEAVE', NOW(), NOW()
);

-- ============================================================
-- 5. ATTENDANCE
-- ============================================================
-- A mixture of PRESENT, ABSENT, HALF_DAY and ON_LEAVE records.

INSERT IGNORE INTO attendance
    (employee_id, attendance_date, check_in, check_out, status, remarks,
     created_at, updated_at)
VALUES
(
    (SELECT id FROM employees WHERE employee_code = 'EMP-005'),
    '2026-09-07', '2026-09-07 09:05:00', '2026-09-07 18:10:00',
    'PRESENT', 'Regular working day', NOW(), NOW()
),
(
    (SELECT id FROM employees WHERE employee_code = 'EMP-005'),
    '2026-09-08', '2026-09-08 09:15:00', '2026-09-08 18:05:00',
    'PRESENT', 'Worked from office', NOW(), NOW()
),
(
    (SELECT id FROM employees WHERE employee_code = 'EMP-005'),
    '2026-09-09', '2026-09-09 09:20:00', '2026-09-09 13:00:00',
    'HALF_DAY', 'Personal appointment', NOW(), NOW()
),
(
    (SELECT id FROM employees WHERE employee_code = 'EMP-006'),
    '2026-09-07', NULL, NULL,
    'ON_LEAVE', 'Approved annual leave', NOW(), NOW()
),
(
    (SELECT id FROM employees WHERE employee_code = 'EMP-006'),
    '2026-09-08', NULL, NULL,
    'ON_LEAVE', 'Approved annual leave', NOW(), NOW()
),
(
    (SELECT id FROM employees WHERE employee_code = 'EMP-006'),
    '2026-09-09', NULL, NULL,
    'ABSENT', 'Unplanned absence', NOW(), NOW()
),
(
    (SELECT id FROM employees WHERE employee_code = 'EMP-004'),
    '2026-09-09', '2026-09-09 09:00:00', '2026-09-09 17:45:00',
    'PRESENT', 'Regular working day', NOW(), NOW()
),
(
    (SELECT id FROM employees WHERE employee_code = 'EMP-003'),
    '2026-09-09', '2026-09-09 08:50:00', '2026-09-09 18:30:00',
    'PRESENT', 'Team management day', NOW(), NOW()
);

-- ============================================================
-- 6. LEAVE REQUESTS
-- ============================================================
-- Includes PENDING, APPROVED, REJECTED and CANCELLED examples.

INSERT INTO leaves
    (employee_id, leave_type, start_date, end_date, reason, status,
     approver_user_id, approval_comment, created_at, updated_at)
SELECT
    e.id, 'ANNUAL', '2026-09-14', '2026-09-16',
    'Family function', 'PENDING', NULL, NULL, NOW(), NOW()
FROM employees e
WHERE e.employee_code = 'EMP-005'
  AND NOT EXISTS (
      SELECT 1 FROM leaves l
      WHERE l.employee_id = e.id
        AND l.start_date = '2026-09-14'
        AND l.end_date = '2026-09-16'
  );

INSERT INTO leaves
    (employee_id, leave_type, start_date, end_date, reason, status,
     approver_user_id, approval_comment, created_at, updated_at)
SELECT
    e.id, 'ANNUAL', '2026-09-07', '2026-09-08',
    'Personal travel', 'APPROVED',
    (SELECT id FROM users WHERE email = 'manager@example.com'),
    'Approved by reporting manager.', NOW(), NOW()
FROM employees e
WHERE e.employee_code = 'EMP-006'
  AND NOT EXISTS (
      SELECT 1 FROM leaves l
      WHERE l.employee_id = e.id
        AND l.start_date = '2026-09-07'
        AND l.end_date = '2026-09-08'
  );

INSERT INTO leaves
    (employee_id, leave_type, start_date, end_date, reason, status,
     approver_user_id, approval_comment, created_at, updated_at)
SELECT
    e.id, 'SICK', '2026-08-18', '2026-08-18',
    'Medical appointment', 'REJECTED',
    (SELECT id FROM users WHERE email = 'manager@example.com'),
    'Please provide supporting details before submitting again.', NOW(), NOW()
FROM employees e
WHERE e.employee_code = 'EMP-005'
  AND NOT EXISTS (
      SELECT 1 FROM leaves l
      WHERE l.employee_id = e.id
        AND l.start_date = '2026-08-18'
        AND l.end_date = '2026-08-18'
  );

INSERT INTO leaves
    (employee_id, leave_type, start_date, end_date, reason, status,
     approver_user_id, approval_comment, created_at, updated_at)
SELECT
    e.id, 'CASUAL', '2026-07-20', '2026-07-20',
    'Personal work', 'CANCELLED', NULL, NULL, NOW(), NOW()
FROM employees e
WHERE e.employee_code = 'EMP-004'
  AND NOT EXISTS (
      SELECT 1 FROM leaves l
      WHERE l.employee_id = e.id
        AND l.start_date = '2026-07-20'
        AND l.end_date = '2026-07-20'
  );

-- ============================================================
-- 7. NOTIFICATIONS
-- ============================================================
-- Several unread notifications make the notification bell visible.

INSERT INTO notifications
    (user_id, notification_type, title, message, link, is_read,
     created_at, read_at)
SELECT
    u.id, 'LEAVE', 'New leave request',
    'Rahul Nair submitted a leave request for 14-Sep-2026 to 16-Sep-2026.',
    '/leaves', FALSE, NOW(), NULL
FROM users u
WHERE u.email = 'manager@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM notifications n
      WHERE n.user_id = u.id
        AND n.title = 'New leave request'
  );

INSERT INTO notifications
    (user_id, notification_type, title, message, link, is_read,
     created_at, read_at)
SELECT
    u.id, 'LEAVE', 'Leave approved',
    'Your annual leave request for 07-Sep-2026 to 08-Sep-2026 was approved.',
    '/leaves', FALSE, NOW(), NULL
FROM users u
WHERE u.email = 'employee2@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM notifications n
      WHERE n.user_id = u.id
        AND n.title = 'Leave approved'
  );

INSERT INTO notifications
    (user_id, notification_type, title, message, link, is_read,
     created_at, read_at)
SELECT
    u.id, 'SYSTEM', 'Welcome to Employee Management System',
    'Your demo employee account is ready. Explore attendance and leave management.',
    '/dashboard', TRUE, DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_SUB(NOW(), INTERVAL 1 DAY)
FROM users u
WHERE u.email = 'employee1@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM notifications n
      WHERE n.user_id = u.id
        AND n.title = 'Welcome to Employee Management System'
  );

INSERT INTO notifications
    (user_id, notification_type, title, message, link, is_read,
     created_at, read_at)
SELECT
    u.id, 'SYSTEM', 'System notification test',
    'This notification demonstrates the unread notification workflow.',
    '/notifications', FALSE, NOW(), NULL
FROM users u
WHERE u.email = 'admin@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM notifications n
      WHERE n.user_id = u.id
        AND n.title = 'System notification test'
  );

-- ============================================================
-- 8. AUDIT LOGS
-- ============================================================
-- Optional demo audit history for the audit-log screen/API.

INSERT INTO audit_logs
    (user_id, action, resource, resource_id, details, created_at)
SELECT
    u.id, 'CREATE', 'employee',
    CAST(e.id AS CHAR),
    CONCAT('Demo employee created: ', e.first_name, ' ', e.last_name),
    DATE_SUB(NOW(), INTERVAL 2 DAY)
FROM users u
JOIN employees e ON e.employee_code = 'EMP-005'
WHERE u.email = 'admin@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM audit_logs a
      WHERE a.user_id = u.id
        AND a.action = 'CREATE'
        AND a.resource = 'employee'
        AND a.resource_id = CAST(e.id AS CHAR)
  );

INSERT INTO audit_logs
    (user_id, action, resource, resource_id, details, created_at)
SELECT
    u.id, 'APPROVE', 'leave',
    CAST(l.id AS CHAR),
    'Demo annual leave request approved by manager.',
    DATE_SUB(NOW(), INTERVAL 1 DAY)
FROM users u
JOIN leaves l ON l.leave_type = 'ANNUAL' AND l.status = 'APPROVED'
JOIN employees e ON e.id = l.employee_id AND e.employee_code = 'EMP-006'
WHERE u.email = 'manager@example.com'
  AND NOT EXISTS (
      SELECT 1 FROM audit_logs a
      WHERE a.user_id = u.id
        AND a.action = 'APPROVE'
        AND a.resource = 'leave'
        AND a.resource_id = CAST(l.id AS CHAR)
  )
LIMIT 1;

COMMIT;

-- ============================================================
-- QUICK VERIFICATION
-- ============================================================
SELECT 'roles' AS table_name, COUNT(*) AS demo_count FROM roles
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'departments', COUNT(*) FROM departments
UNION ALL
SELECT 'employees', COUNT(*) FROM employees
UNION ALL
SELECT 'attendance', COUNT(*) FROM attendance
UNION ALL
SELECT 'leaves', COUNT(*) FROM leaves
UNION ALL
SELECT 'notifications', COUNT(*) FROM notifications
UNION ALL
SELECT 'audit_logs', COUNT(*) FROM audit_logs;
