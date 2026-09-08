from fastapi import APIRouter

from app.api.v1.system import router as system_router
from app.api.v1.auth import router as auth_router
from app.api.v1.departments import router as departments_router
from app.api.v1.employees import router as employees_router
from app.api.v1.attendance import router as attendance_router


router = APIRouter(prefix="/api/v1")


# System
router.include_router(system_router)

# Authentication
router.include_router(auth_router)

# Departments
router.include_router(departments_router)

# Employees
router.include_router(employees_router)

# Attendance
router.include_router(attendance_router)