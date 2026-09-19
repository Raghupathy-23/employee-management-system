from sqlalchemy.orm import Session

from app.models.leave import Leave
from app.models.notification import Notification
from app.models.user import User


MANAGEMENT_ROLES = {"ADMIN", "HR", "HR_MANAGER", "MANAGER"}


class LeaveApprovalService:
    def _add_notification(self, db: Session, leave: Leave, title: str, message: str) -> None:
        employee = leave.employee
        if employee is None:
            return
        db.add(
            Notification(
                user_id=employee.user_id,
                notification_type="LEAVE",
                title=title,
                message=message,
                link=f"/leaves/{leave.id}",
            )
        )

    def _authorize(self, leave: Leave, approver: User) -> None:
        role_name = approver.role.name.upper()
        if role_name not in MANAGEMENT_ROLES:
            raise PermissionError("Only authorized management roles can approve leave")

        if role_name == "MANAGER":
            employee = leave.employee
            if approver.employee is None or employee is None or employee.manager_id != approver.employee.id:
                raise PermissionError("Managers can only approve leave for their direct reports")

        if leave.employee_id == getattr(approver.employee, "id", None):
            raise PermissionError("An employee cannot approve their own leave")

    def approve(self, db: Session, leave_id: int, approver: User, comment: str | None = None):
        leave = db.get(Leave, leave_id)
        if not leave:
            return None
        if leave.status != "PENDING":
            raise ValueError("Only pending leave requests can be approved")
        self._authorize(leave, approver)
        leave.status = "APPROVED"
        leave.approver_user_id = approver.id
        leave.approval_comment = comment
        self._add_notification(db, leave, "Leave approved", "Your leave request was approved.")
        db.commit()
        db.refresh(leave)
        return leave

    def reject(self, db: Session, leave_id: int, approver: User, comment: str | None = None):
        leave = db.get(Leave, leave_id)
        if not leave:
            return None
        if leave.status != "PENDING":
            raise ValueError("Only pending leave requests can be rejected")
        self._authorize(leave, approver)
        leave.status = "REJECTED"
        leave.approver_user_id = approver.id
        leave.approval_comment = comment
        self._add_notification(db, leave, "Leave rejected", "Your leave request was rejected.")
        db.commit()
        db.refresh(leave)
        return leave
