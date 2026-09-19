from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.leave import Leave


class LeaveRepository:
    def get_by_id(self, db: Session, leave_id: int):
        return db.get(Leave, leave_id)

    def has_overlap(
        self,
        db: Session,
        employee_id: int,
        start_date: date,
        end_date: date,
        exclude_leave_id: int | None = None,
    ) -> bool:
        stmt = select(Leave.id).where(
            Leave.employee_id == employee_id,
            Leave.status.in_(["PENDING", "APPROVED"]),
            Leave.start_date <= end_date,
            Leave.end_date >= start_date,
        )
        if exclude_leave_id is not None:
            stmt = stmt.where(Leave.id != exclude_leave_id)
        return db.scalar(stmt.limit(1)) is not None

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        employee_id: int | None = None,
        status: str | None = None,
        leave_type: str | None = None,
        manager_id: int | None = None,
    ):
        stmt = select(Leave).order_by(Leave.start_date.desc(), Leave.id.desc())

        if employee_id is not None:
            stmt = stmt.where(Leave.employee_id == employee_id)
        if status is not None:
            stmt = stmt.where(Leave.status == status)
        if leave_type is not None:
            stmt = stmt.where(Leave.leave_type == leave_type)
        if manager_id is not None:
            stmt = stmt.where(Leave.employee.has(manager_id=manager_id))

        return list(db.scalars(stmt.offset(skip).limit(limit)).all())

    def create(self, db: Session, leave: Leave):
        db.add(leave)
        db.commit()
        db.refresh(leave)
        return leave

    def delete(self, db: Session, leave: Leave):
        db.delete(leave)
        db.commit()
