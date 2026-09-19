
from sqlalchemy.orm import Session

from app.models.leave import Leave
from app.repositories.leave_repository import LeaveRepository
from app.repositories.employee_repository import EmployeeRepository
from app.services.leave_balance_service import LeaveBalanceService


ALLOWED_LEAVE_TYPES = {
    "ANNUAL",
    "SICK",
    "CASUAL",
    "UNPAID",
    "OTHER",
}

ALLOWED_STATUSES = {
    "PENDING",
    "APPROVED",
    "REJECTED",
    "CANCELLED",
}


class LeaveService:
    def __init__(self):
        self.repository = LeaveRepository()
        self.balance_service = LeaveBalanceService()
        self.employee_repository = EmployeeRepository()

    def get_employee(self, db: Session, employee_id: int):
        return self.employee_repository.get_by_id(db, employee_id)

    def _validate_leave_type(self, leave_type: str):
        normalized = leave_type.upper()

        if normalized not in ALLOWED_LEAVE_TYPES:
            raise ValueError(
                "Invalid leave type. Allowed values: "
                + ", ".join(sorted(ALLOWED_LEAVE_TYPES))
            )

        return normalized

    def create(self, db: Session, data):
        # Validate leave type
        leave_type = self._validate_leave_type(data.leave_type)

        # Validate leave balance
        self.balance_service.validate_request(
            db,
            data.employee_id,
            leave_type,
            data.start_date,
            data.end_date,
        )

        # Check for overlapping leave requests
        if self.repository.has_overlap(
            db,
            data.employee_id,
            data.start_date,
            data.end_date,
        ):
            raise ValueError(
                "Leave dates overlap an existing pending or approved leave"
            )

        # Create the leave request
        return self.repository.create(
            db,
            Leave(
                **data.model_dump(exclude={"leave_type"}),
                leave_type=leave_type,
                status="PENDING",
            ),
        )

    def list(
        self,
        db: Session,
        skip=0,
        limit=100,
        employee_id=None,
        status=None,
        leave_type=None,
        manager_id=None,
    ):
        # Validate status
        if status is not None:
            status = status.upper()

            if status not in ALLOWED_STATUSES:
                raise ValueError("Invalid leave status")

        # Validate leave type
        if leave_type is not None:
            leave_type = self._validate_leave_type(leave_type)

        return self.repository.list(
            db,
            skip,
            limit,
            employee_id,
            status,
            leave_type,
            manager_id,
        )

    def get(self, db: Session, leave_id: int):
        return self.repository.get_by_id(db, leave_id)

    def update(self, db: Session, leave_id: int, data):
        leave = self.get(db, leave_id)

        if not leave:
            return None

        # Only pending requests can be modified
        if leave.status != "PENDING":
            raise ValueError(
                "Only pending leave requests can be updated"
            )

        values = data.model_dump(exclude_unset=True)

        # Get the new values, or keep the existing values
        new_leave_type = values.get(
            "leave_type",
            leave.leave_type,
        )

        new_start = values.get(
            "start_date",
            leave.start_date,
        )

        new_end = values.get(
            "end_date",
            leave.end_date,
        )

        # Validate leave type
        new_leave_type = self._validate_leave_type(
            new_leave_type
        )

        # Validate date range
        if new_end < new_start:
            raise ValueError(
                "end_date cannot be earlier than start_date"
            )

        # Check for overlapping leave requests
        if self.repository.has_overlap(
            db,
            leave.employee_id,
            new_start,
            new_end,
            exclude_leave_id=leave.id,
        ):
            raise ValueError(
                "Leave dates overlap an existing pending or approved leave"
            )

        # Validate leave balance for the updated request
        self.balance_service.validate_request(
            db,
            leave.employee_id,
            new_leave_type,
            new_start,
            new_end,
            exclude_leave_id=leave.id,
        )

        values["leave_type"] = new_leave_type

        # Apply changes
        for field, value in values.items():
            setattr(leave, field, value)

        db.commit()
        db.refresh(leave)

        return leave

    def delete(self, db: Session, leave_id: int):
        leave = self.get(db, leave_id)

        if not leave:
            return False

        # Only pending requests can be deleted
        if leave.status != "PENDING":
            raise ValueError(
                "Only pending leave requests can be deleted"
            )

        self.repository.delete(db, leave)

        return True

