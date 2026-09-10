from sqlalchemy.orm import Session

from app.models.leave import Leave


class LeaveApprovalService:
    def approve(self, db: Session, leave_id: int, approver_user_id: int, comment: str | None = None):
        leave = db.get(Leave, leave_id)
        if not leave:
            return None
        if leave.status != "PENDING":
            raise ValueError("Only pending leave requests can be approved")
        if leave.employee_id == getattr(leave, "approver_employee_id", None):
            raise ValueError("An employee cannot approve their own leave")
        leave.status = "APPROVED"
        leave.approver_user_id = approver_user_id
        leave.approval_comment = comment
        db.commit()
        db.refresh(leave)
        return leave

    def reject(self, db: Session, leave_id: int, approver_user_id: int, comment: str | None = None):
        leave = db.get(Leave, leave_id)
        if not leave:
            return None
        if leave.status != "PENDING":
            raise ValueError("Only pending leave requests can be rejected")
        leave.status = "REJECTED"
        leave.approver_user_id = approver_user_id
        leave.approval_comment = comment
        db.commit()
        db.refresh(leave)
        return leave
