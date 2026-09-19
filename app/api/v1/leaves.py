from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.leave import LeaveCreate, LeaveResponse, LeaveUpdate
from app.services.audit_service import AuditService
from app.services.leave_service import LeaveService

router = APIRouter(prefix="/leaves", tags=["Leave"])
service = LeaveService()
audit_service = AuditService()


MANAGEMENT_ROLES = {"ADMIN", "HR", "HR_MANAGER", "MANAGER"}


def _can_access_employee(user: User, employee_id: int, db: Session) -> bool:
    role = user.role.name.upper()
    if role in {"ADMIN", "HR", "HR_MANAGER"}:
        return True
    if role == "EMPLOYEE":
        return getattr(user.employee, "id", None) == employee_id
    if role == "MANAGER":
        employee = service.get_employee(db, employee_id)
        return user.employee is not None and employee is not None and employee.manager_id == user.employee.id
    return False


@router.post("", response_model=LeaveResponse, status_code=status.HTTP_201_CREATED)
def create_leave(
    payload: LeaveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not _can_access_employee(current_user, payload.employee_id, db):
        raise HTTPException(status_code=403, detail="You cannot create leave for this employee")
    try:
        leave = service.create(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    audit_service.record(db, "LEAVE_CREATED", current_user.id, "leave", leave.id)
    return leave


@router.get("", response_model=list[LeaveResponse])
def list_leaves(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    employee_id: int | None = None,
    leave_status: str | None = Query(default=None, alias="status"),
    leave_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.name.upper()
    if role == "EMPLOYEE":
        employee_id = getattr(current_user.employee, "id", None)
    elif role == "MANAGER":
        if employee_id is not None and not _can_access_employee(current_user, employee_id, db):
            raise HTTPException(status_code=403, detail="You can only view leave for your direct reports")
    manager_id = current_user.employee.id if role == "MANAGER" and current_user.employee else None
    try:
        rows = service.list(db, skip, limit, employee_id, leave_status, leave_type, manager_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return rows


@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    leave = service.get(db, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if not _can_access_employee(current_user, leave.employee_id, db):
        raise HTTPException(status_code=403, detail="You cannot access this leave request")
    return leave


@router.patch("/{leave_id}", response_model=LeaveResponse)
def update_leave(
    leave_id: int,
    payload: LeaveUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = service.get(db, leave_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if not _can_access_employee(current_user, existing.employee_id, db):
        raise HTTPException(status_code=403, detail="You cannot modify this leave request")
    if current_user.role.name.upper() == "MANAGER":
        raise HTTPException(status_code=403, detail="Managers cannot edit leave requests")
    try:
        leave = service.update(db, leave_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    audit_service.record(db, "LEAVE_UPDATED", current_user.id, "leave", leave.id)
    return leave


@router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = service.get(db, leave_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if current_user.role.name.upper() not in MANAGEMENT_ROLES and not _can_access_employee(current_user, existing.employee_id, db):
        raise HTTPException(status_code=403, detail="You cannot delete this leave request")
    try:
        deleted = service.delete(db, leave_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="Leave request not found")
    audit_service.record(db, "LEAVE_DELETED", current_user.id, "leave", leave_id)
