from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.leave import LeaveResponse
from app.schemas.leave_approval import LeaveApprovalRequest
from app.services.audit_service import AuditService
from app.services.leave_approval_service import LeaveApprovalService

router = APIRouter(prefix="/leaves", tags=["Leave Approval"])
service = LeaveApprovalService()
audit_service = AuditService()


@router.patch("/{leave_id}/approve", response_model=LeaveResponse)
def approve_leave(
    leave_id: int,
    payload: LeaveApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        leave = service.approve(db, leave_id, current_user, payload.comment)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    audit_service.record(db, "LEAVE_APPROVED", current_user.id, "leave", leave.id, {"status": leave.status})
    return leave


@router.patch("/{leave_id}/reject", response_model=LeaveResponse)
def reject_leave(
    leave_id: int,
    payload: LeaveApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        leave = service.reject(db, leave_id, current_user, payload.comment)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    audit_service.record(db, "LEAVE_REJECTED", current_user.id, "leave", leave.id, {"status": leave.status})
    return leave
