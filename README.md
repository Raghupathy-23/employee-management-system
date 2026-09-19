# Employee Management System

A full-stack **Employee Management System** built as a Python/FastAPI learning and portfolio project.

The project was developed to practice and demonstrate real-world backend engineering concepts including REST API development, layered architecture, authentication, role-based access control, relational database design, database migrations, business logic, testing, Docker, CI, and frontend integration.

> **Project status:** Local development / portfolio project
> **Deployment:** Not currently deployed as a public live application

---

## 📌 Project Overview

The Employee Management System provides a centralized application for managing employee-related information and common employee operations.

The system includes:

* Employee management
* Department management
* Role and permission management
* JWT authentication
* Role-based access control
* Attendance tracking
* Leave management
* Leave approval
* Leave balance management
* Notifications
* Audit logging
* REST APIs
* React frontend
* MySQL database
* Database migrations using Alembic
* Automated testing
* Docker-based local development
* GitHub Actions CI

The project was developed incrementally using feature branches and multiple development phases.

---

## 🎯 Project Objectives

The main objective of this project was to build a practical full-stack application while developing stronger skills in **Python backend development and API engineering**.

The project focuses on:

* Building REST APIs using FastAPI
* Designing a maintainable backend architecture
* Implementing authentication and authorization
* Working with relational databases
* Using SQLAlchemy for database access
* Managing database changes with Alembic
* Separating API, business logic, and database responsibilities
* Implementing employee-related business operations
* Writing automated tests
* Containerizing the application with Docker
* Integrating a React frontend with a FastAPI backend
* Setting up CI using GitHub Actions

---

## ✨ Main Features

### 🔐 Authentication

* JWT-based user authentication
* Secure password hashing using Argon2
* Protected API endpoints
* Configurable application secret through environment variables

### 👥 Employee Management

* Create employees
* Update employee information
* Retrieve employee information
* Manage employee relationships
* Assign employees to departments
* Associate employees with managers
* Support manager/direct-report relationships

### 🏢 Department Management

* Create departments
* Update departments
* Retrieve department information
* Associate employees with departments

### 🛡️ Role-Based Access Control

The application supports multiple roles:

* `ADMIN`
* `HR`
* `HR_MANAGER`
* `MANAGER`
* `EMPLOYEE`

Access to protected operations is controlled on the backend based on the authenticated user's role.

### 📅 Attendance Management

* Record employee attendance
* Track attendance dates
* Store check-in and check-out information
* Prevent duplicate attendance records for the same employee/date
* Retrieve attendance information through API endpoints

### 📝 Leave Management

The system provides leave request and approval functionality.

```text
Employee submits leave
        ↓
Balance validation
        ↓
Date / overlap validation
        ↓
Pending
        ↓
Manager / HR review
        ↓
Approved / Rejected
        ↓
Notification + Audit Log
```

Implemented functionality includes:

* Leave requests
* Leave balance validation
* Date validation
* Overlapping leave validation
* Leave approval/rejection
* Manager/HR review
* Leave balance handling

### 🔔 Notifications

The application includes persistent in-app notifications.

Features include:

* Notification creation
* Read/unread status
* Notification retrieval
* Notifications triggered by relevant application operations

### 📋 Audit Logging

Important application operations can be recorded using audit logs.

This provides a record of significant actions performed within the system.

### 🔎 Validation, Pagination & Filtering

The API uses Pydantic schemas for request and response validation.

Selected API resources also support pagination and filtering to handle larger datasets more efficiently.

---

## 🏗️ Architecture

The backend follows a layered architecture:

```text
React Frontend
      │
      ▼
FastAPI Router
      │
      ▼
Authentication / Authorization
      │
      ▼
Service Layer
      │
      ▼
Repository Layer
      │
      ▼
SQLAlchemy
      │
      ▼
MySQL
```

### Architecture Responsibilities

**API Layer**

Handles HTTP requests, routing, dependencies and API responses.

**Service Layer**

Contains application and business logic.

**Repository Layer**

Handles database access and isolates persistence logic from the service layer.

**Models**

Represent database entities using SQLAlchemy.

**Schemas**

Define and validate API request and response structures using Pydantic.

This separation keeps the application organized and makes individual components easier to test and maintain.

---

## 🛠️ Technology Stack

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy 2.x
* Pydantic v2
* pydantic-settings
* MySQL 8.4
* Alembic
* JWT authentication
* Argon2 password hashing
* Pytest
* HTTPX

### Frontend

* React
* React Router
* Axios
* Vite
* JavaScript
* HTML
* CSS

### Development & DevOps

* Docker
* Docker Compose
* Git
* GitHub
* GitHub Actions
* Ruff
* Nginx

---

## 📁 Project Structure

```text
employee-management-system/
│
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── employees.py
│   │       ├── departments.py
│   │       ├── attendance.py
│   │       ├── leaves.py
│   │       ├── leave_approval.py
│   │       ├── leave_balance.py
│   │       ├── notifications.py
│   │       ├── roles.py
│   │       ├── audit.py
│   │       └── router.py
│   │
│   ├── core/
│   ├── db/
│   ├── middleware/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
├── tests/
├── docs/
├── docker/
├── scripts/
├── employee-management-demo-data/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── Dockerfile.frontend
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
├── pyproject.toml
├── package.json
├── .env.example
├── .gitignore
└── LICENSE
```

---

## 🐳 Running Locally

This project is currently intended for **local development and learning**.

### Prerequisites

* Python 3.12+
* Node.js
* npm
* Docker Desktop
* Git

### Using Docker Compose

Clone the repository:

```bash
git clone https://github.com/Raghupathy16/employee-management-system.git
```

Navigate into the project:

```bash
cd employee-management-system
```

Create the environment file.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Update the required values in `.env`.

Start the application:

```bash
docker compose up --build -d
```

Check the containers:

```bash
docker compose ps
```

### Local URLs

```text
Frontend:
http://localhost:5174

Backend:
http://localhost:8000

Swagger:
http://localhost:8000/docs

Health:
http://localhost:8000/health
```

> These URLs are for local development only. There is currently no public live deployment.

---

## 🧪 Testing

The backend includes automated tests using Pytest.

Run:

```bash
pytest
```

The test suite covers areas including:

* Health checks
* Schema validation
* RBAC routes
* Security functionality
* Leave-related validation

### Linting

Run Ruff:

```bash
ruff check app tests scripts
```

### Frontend Build

Install dependencies:

```bash
npm ci
```

Build the frontend:

```bash
npm run build
```

---

## 🔄 Continuous Integration

The repository includes a GitHub Actions workflow:

```text
.github/workflows/ci.yml
```

The CI pipeline performs automated checks including:

* Python code quality checks
* Backend tests
* Frontend build

This helps catch issues before changes are merged.

---

## 📖 API Documentation

When running locally, FastAPI provides interactive Swagger documentation at:

```text
http://localhost:8000/docs
```

The API is versioned under:

```text
/api/v1
```

Main API resources include:

```text
/auth
/employees
/departments
/attendance
/leaves
/roles
/notifications
/audit-logs
/employees/{employee_id}/leave-balance
/health
```

---

## 🗄️ Database & Migrations

The application uses:

```text
MySQL
  ↓
SQLAlchemy
  ↓
Alembic
```

Database schema changes are managed using Alembic migrations.

Apply migrations with:

```bash
alembic upgrade head
```

This allows the database schema to be recreated consistently in a new development environment.

---

## 🔐 Security

The project includes several security-related practices:

* JWT-based authentication
* Argon2 password hashing
* Backend-enforced role-based authorization
* Protected API routes
* Environment-based configuration
* Configurable CORS
* Centralized exception handling
* `.env` excluded from Git tracking

Sensitive credentials are not intended to be committed to the repository.

---

## 🔀 Development Phases

The project was developed incrementally using Git feature branches.

The main development stages included:

1. Project setup
2. Database architecture
3. Authentication
4. Employee management
5. Department management
6. Attendance management
7. Frontend integration
8. Leave management
9. Leave approval
10. Leave balance management
11. Notifications
12. Role-based access control
13. Audit logging
14. Dashboard improvements
15. Docker integration
16. Automated testing
17. GitHub Actions CI
18. Documentation and code improvements

The complete development history is available through the repository's Git commits and branches.

---

## 📚 Project Documentation

Additional documentation is available in the repository:

* `docs/ARCHITECTURE.md`
* `docs/DEPLOYMENT.md`
* `docs/FRONTEND.md`
* `docs/TESTING.md`
* `docs/PORTFOLIO.md`
* `PHASE_PLAN.md`
* `CHANGELOG.md`
* `PRODUCTION_READINESS.md`

---

## 🚧 Current Status

### Implemented

* FastAPI backend
* React frontend
* MySQL database
* SQLAlchemy ORM
* Alembic migrations
* JWT authentication
* Argon2 password hashing
* Role-based access control
* Employee management
* Department management
* Attendance management
* Leave management
* Leave approval
* Leave balance management
* Notifications
* Audit logging
* API validation
* Pagination/filtering
* Docker Compose
* Automated tests
* GitHub Actions CI
* Project documentation

### Not Yet Implemented

The following are planned or possible future improvements:

* Public cloud deployment
* Refresh-token/session management
* Background job processing
* Email notification service
* More granular permission management
* Full integration testing against MySQL in CI
* Centralized logging and observability
* Production secrets management
* Production monitoring

---

## 🚀 Future Improvements

Possible future improvements include:

* Deploying the application to a cloud platform
* Implementing refresh-token/session management
* Adding background jobs
* Adding email notifications
* Improving permission granularity
* Expanding integration test coverage
* Adding structured logging
* Adding application monitoring
* Improving frontend error handling
* Adding production infrastructure

---

## 📌 Portfolio Note

This project is intentionally presented as a **learning and portfolio project**.

The application has been developed locally to practice full-stack development and backend engineering concepts using FastAPI, React, MySQL, Docker and related technologies.

It is **not currently deployed as a public production application** and is not presented as an enterprise HR product.

The main purpose of this project is to demonstrate practical experience with:

* Python backend development
* REST API design
* Database design
* Authentication and authorization
* Business logic
* Testing
* Docker
* CI
* Frontend/backend integration
* Maintainable project architecture

---

## 👨‍💻 Author

**Raghupathy**

Computer Science & Business Systems

GitHub:
https://github.com/Raghupathy16

---

## 📄 License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for details.
