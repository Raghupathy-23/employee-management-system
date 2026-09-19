# Portfolio / Interview Guide

## One-line project description

**Employee Management & HR Workflow System** — a full-stack FastAPI + React application that manages employees, departments, attendance and leave workflows with JWT authentication, RBAC, audit logs, notifications and Dockerized deployment.

## What to highlight in an interview

### 1. Architecture

> I used a layered backend architecture. FastAPI routers handle HTTP concerns, services contain business rules, repositories isolate SQLAlchemy queries, and models represent the relational data model.

### 2. Authentication and authorization

> Authentication uses JWT bearer tokens and Argon2 password hashing. Authorization is enforced on the server using the authenticated user's current database role rather than trusting only the role stored in the JWT.

### 3. Business rules

> Leave requests validate date ranges, yearly balances and overlapping pending/approved requests. Managers can approve only leave requests belonging to their direct reports, while HR/admin roles can manage broader workflows.

### 4. Reliability

> Database schema changes are versioned with Alembic. The Docker API container can apply migrations at startup, and health/readiness endpoints expose application and database status.

### 5. Testing

> API smoke tests are isolated from a developer's local MySQL instance, while CI runs linting, backend tests and the frontend production build.

### 6. DevOps

> Docker Compose provides MySQL, FastAPI and the React/Nginx frontend. Environment variables control secrets, database connectivity, CORS and public API URLs.

## Strong interview questions to prepare for

- Why did you choose FastAPI instead of Flask/Django?
- Why separate services and repositories?
- How does your JWT authentication flow work?
- How does RBAC prevent unauthorized API access?
- How would you handle refresh tokens?
- How do you prevent overlapping leave requests?
- Why use Alembic instead of creating tables on application startup?
- How would you scale notifications?
- How would you run this with multiple API replicas?
- How would you improve the browser token storage for a real production system?
- What would you monitor in production?

## Resume wording

**Employee Management & HR Workflow System** | Python, FastAPI, SQLAlchemy, MySQL, Alembic, React, Docker

- Developed a full-stack HR management platform with REST APIs for employee, department, attendance and leave operations.
- Implemented JWT authentication, role-based authorization, manager-based leave approvals, audit logging and persistent in-app notifications.
- Designed a layered FastAPI architecture using API, service, repository and ORM layers with versioned Alembic migrations and automated tests.
- Containerized the application and database with Docker Compose and added CI checks for backend quality and frontend builds.
