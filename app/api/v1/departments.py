from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.api.v1.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.services.audit_service import AuditService
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])
service = DepartmentService()
audit_service = AuditService()


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("ADMIN", "HR", "HR_MANAGER")),
):
    try:
        department = service.create(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    audit_service.record(db, "DEPARTMENT_CREATED", current_user.id, "department", department.id)
    return department


@router.get("", response_model=list[DepartmentResponse])
def list_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return service.list(db, skip, limit)


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    department = service.get(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.patch("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    payload: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("ADMIN", "HR", "HR_MANAGER")),
):
    try:
        department = service.update(db, department_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    audit_service.record(db, "DEPARTMENT_UPDATED", current_user.id, "department", department.id, payload.model_dump(exclude_unset=True))
    return department


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("ADMIN", "HR", "HR_MANAGER")),
):
    if not service.delete(db, department_id):
        raise HTTPException(status_code=404, detail="Department not found")
    audit_service.record(db, "DEPARTMENT_DELETED", current_user.id, "department", department_id)
