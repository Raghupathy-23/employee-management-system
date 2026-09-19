from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.database import get_db
from app.models.user import User
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])
service = RoleService()


@router.get("", response_model=list[RoleResponse])
def list_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    _: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    return service.list(db, skip, limit)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int,
    _: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    role = service.get(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreate,
    _: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    try:
        return service.create(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.patch("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    payload: RoleUpdate,
    _: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    try:
        role = service.update(db, role_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    _: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    try:
        deleted = service.delete(db, role_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
