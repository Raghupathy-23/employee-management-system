from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.api.v1.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.audit_service import AuditService
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])
service = EmployeeService()
audit_service = AuditService()


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("ADMIN", "HR", "HR_MANAGER")),
):
    try:
        employee = service.create(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    audit_service.record(db, "EMPLOYEE_CREATED", current_user.id, "employee", employee.id)
    return employee


@router.get("", response_model=list[EmployeeResponse])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str | None = None,
    department_id: int | None = None,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.name.upper()
    manager_id = None
    if role == "EMPLOYEE":
        if not current_user.employee:
            return []
        return [current_user.employee]
    if role == "MANAGER" and current_user.employee:
        manager_id = current_user.employee.id
    return service.list(db, skip, limit, search, department_id, active_only, manager_id)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = service.get(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    role = current_user.role.name.upper()
    if role == "EMPLOYEE" and employee.id != getattr(current_user.employee, "id", None):
        raise HTTPException(status_code=403, detail="You can only access your own employee record")
    if role == "MANAGER" and employee.id != getattr(current_user.employee, "id", None) and employee.manager_id != getattr(current_user.employee, "id", None):
        raise HTTPException(status_code=403, detail="You can only access your direct reports")
    return employee


@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("ADMIN", "HR", "HR_MANAGER")),
):
    try:
        employee = service.update(db, employee_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    audit_service.record(db, "EMPLOYEE_UPDATED", current_user.id, "employee", employee.id, payload.model_dump(exclude_unset=True))
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("ADMIN", "HR", "HR_MANAGER")),
):
    if not service.delete(db, employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    audit_service.record(db, "EMPLOYEE_DELETED", current_user.id, "employee", employee_id)
