from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.leave import LeaveCreate, LeaveResponse, LeaveUpdate
from app.services.leave_service import LeaveService


router = APIRouter(prefix="/leaves", tags=["Leave"])
service = LeaveService()


@router.post(
    "",
    response_model=LeaveResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave(payload: LeaveCreate, db: Session = Depends(get_db)):
    try:
        return service.create(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[LeaveResponse])
def list_leaves(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    employee_id: int | None = None,
    leave_status: str | None = Query(default=None, alias="status"),
    leave_type: str | None = None,
    db: Session = Depends(get_db),
):
    try:
        return service.list(
            db,
            skip,
            limit,
            employee_id,
            leave_status,
            leave_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = service.get(db, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave


@router.patch("/{leave_id}", response_model=LeaveResponse)
def update_leave(
    leave_id: int,
    payload: LeaveUpdate,
    db: Session = Depends(get_db),
):
    try:
        leave = service.update(db, leave_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave


@router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave(leave_id: int, db: Session = Depends(get_db)):
    try:
        deleted = service.delete(db, leave_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not deleted:
        raise HTTPException(status_code=404, detail="Leave request not found")
