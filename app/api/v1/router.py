from fastapi import APIRouter

from app.api.v1.system import router as system_router
from app.api.v1.auth import router as auth_router
from app.api.v1.departments import router as departments_router
from app.api.v1.employees import router as employees_router
from app.api.v1.attendance import router as attendance_router
from app.api.v1.leaves import router as leaves_router
from app.api.v1.leave_approval import router as leave_approval_router
from app.api.v1.leave_balance import router as leave_balance_router
from app.api.v1.notifications import router as notifications_router

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

router.include_router(leaves_router)

# Leave Approval
router.include_router(leave_approval_router)

router.include_router(leave_balance_router)

router.include_router(notifications_router)