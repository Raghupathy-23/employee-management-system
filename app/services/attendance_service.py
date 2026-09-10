from datetime import date

from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.repositories.attendance_repository import AttendanceRepository


ALLOWED_STATUSES = {"PRESENT", "ABSENT", "HALF_DAY", "ON_LEAVE"}


class AttendanceService:
    def __init__(self):
        self.repository = AttendanceRepository()

    def create(self, db: Session, data):
        if data.status not in ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid attendance status. Allowed values: "
                f"{', '.join(sorted(ALLOWED_STATUSES))}"
            )

        if self.repository.get_by_employee_date(
            db, data.employee_id, data.attendance_date
        ):
            raise ValueError(
                "Attendance already exists for this employee and date"
            )

        if data.check_in and data.check_out and data.check_out < data.check_in:
            raise ValueError("check_out cannot be earlier than check_in")

        return self.repository.create(
            db, Attendance(**data.model_dump())
        )

    def list(
        self,
        db: Session,
        skip=0,
        limit=100,
        employee_id=None,
        attendance_date: date | None = None,
        status=None,
    ):
        if status is not None and status not in ALLOWED_STATUSES:
            raise ValueError("Invalid attendance status")

        return self.repository.list(
            db, skip, limit, employee_id, attendance_date, status
        )

    def get(self, db: Session, attendance_id: int):
        return self.repository.get_by_id(db, attendance_id)

    def update(self, db: Session, attendance_id: int, data):
        attendance = self.get(db, attendance_id)
        if not attendance:
            return None

        values = data.model_dump(exclude_unset=True)

        if "status" in values and values["status"] not in ALLOWED_STATUSES:
            raise ValueError("Invalid attendance status")

        new_date = values.get("attendance_date", attendance.attendance_date)
        existing = self.repository.get_by_employee_date(
            db, attendance.employee_id, new_date
        )

        if existing and existing.id != attendance.id:
            raise ValueError(
                "Attendance already exists for this employee and date"
            )

        new_check_in = values.get("check_in", attendance.check_in)
        new_check_out = values.get("check_out", attendance.check_out)

        if new_check_in and new_check_out and new_check_out < new_check_in:
            raise ValueError("check_out cannot be earlier than check_in")

        for field, value in values.items():
            setattr(attendance, field, value)

        db.commit()
        db.refresh(attendance)
        return attendance

    def delete(self, db: Session, attendance_id: int):
        attendance = self.get(db, attendance_id)
        if not attendance:
            return False

        self.repository.delete(db, attendance)
        return True
