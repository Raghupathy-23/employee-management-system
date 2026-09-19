from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.api.v1.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceUpdate
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance"])
service = AttendanceService()


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.name.upper()
    if role == "EMPLOYEE" and getattr(current_user.employee, "id", None) != payload.employee_id:
        raise HTTPException(status_code=403, detail="You can only create attendance for yourself")
    if role == "MANAGER" and current_user.employee is None:
        raise HTTPException(status_code=403, detail="Manager employee profile is required")
    if role == "MANAGER" and payload.employee_id != getattr(current_user.employee, "id", None):
        target = service.get_employee(db, payload.employee_id)
        if target is None or target.manager_id != current_user.employee.id:
            raise HTTPException(status_code=403, detail="You can only manage attendance for your direct reports")
    if role not in {"ADMIN", "HR", "HR_MANAGER", "MANAGER", "EMPLOYEE"}:
        raise HTTPException(status_code=403, detail="You do not have permission to manage attendance")
    try:
        return service.create(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("", response_model=list[AttendanceResponse])
def list_attendance(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    employee_id: int | None = None,
    attendance_date: date | None = None,
    attendance_status: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.name.upper()
    if role == "EMPLOYEE":
        employee_id = getattr(current_user.employee, "id", None)
    elif role == "MANAGER" and employee_id is not None:
        employee = service.get_employee(db, employee_id)
        if employee is None or employee.manager_id != getattr(current_user.employee, "id", None):
            raise HTTPException(status_code=403, detail="You can only view attendance for your direct reports")
    try:
        return service.list(db, skip, limit, employee_id, attendance_date, attendance_status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attendance = service.get(db, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    role = current_user.role.name.upper()
    if role == "EMPLOYEE" and attendance.employee_id != getattr(current_user.employee, "id", None):
        raise HTTPException(status_code=403, detail="You can only access your own attendance")
    return attendance


@router.patch("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    payload: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = service.get(db, attendance_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    if current_user.role.name.upper() == "EMPLOYEE":
        raise HTTPException(status_code=403, detail="Employees cannot edit attendance records")
    if current_user.role.name.upper() == "MANAGER":
        target = service.get_employee(db, existing.employee_id)
        if target is None or target.manager_id != getattr(current_user.employee, "id", None):
            raise HTTPException(status_code=403, detail="You can only manage attendance for your direct reports")
    try:
        attendance = service.update(db, attendance_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return attendance


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("ADMIN", "HR", "HR_MANAGER")),
):
    if not service.delete(db, attendance_id):
        raise HTTPException(status_code=404, detail="Attendance record not found")
