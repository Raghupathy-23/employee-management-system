from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.attendance import Attendance


class AttendanceRepository:
    def get_by_id(self, db: Session, attendance_id: int):
        return db.get(Attendance, attendance_id)

    def get_by_employee_date(
        self,
        db: Session,
        employee_id: int,
        attendance_date: date,
    ):
        return db.scalar(
            select(Attendance).where(
                Attendance.employee_id == employee_id,
                Attendance.attendance_date == attendance_date,
            )
        )

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        employee_id: int | None = None,
        attendance_date: date | None = None,
        status: str | None = None,
    ):
        stmt = select(Attendance).order_by(
            Attendance.attendance_date.desc(),
            Attendance.id.desc(),
        )

        if employee_id is not None:
            stmt = stmt.where(Attendance.employee_id == employee_id)

        if attendance_date is not None:
            stmt = stmt.where(Attendance.attendance_date == attendance_date)

        if status is not None:
            stmt = stmt.where(Attendance.status == status)

        return list(db.scalars(stmt.offset(skip).limit(limit)).all())

    def create(self, db: Session, attendance: Attendance):
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance

    def delete(self, db: Session, attendance: Attendance):
        db.delete(attendance)
        db.commit()
