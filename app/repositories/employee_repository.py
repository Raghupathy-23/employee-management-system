from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.employee import Employee


class EmployeeRepository:
    def get_by_id(self, db: Session, employee_id: int):
        return db.get(Employee, employee_id)

    def get_by_code(self, db: Session, employee_code: str):
        return db.scalar(select(Employee).where(Employee.employee_code == employee_code))

    def get_by_user_id(self, db: Session, user_id: int):
        return db.scalar(select(Employee).where(Employee.user_id == user_id))

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        department_id: int | None = None,
        active_only: bool | None = True,
        manager_id: int | None = None,
    ):
        stmt = select(Employee).order_by(Employee.id.desc())

        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                or_(
                    Employee.employee_code.ilike(term),
                    Employee.first_name.ilike(term),
                    Employee.last_name.ilike(term),
                    Employee.designation.ilike(term),
                )
            )

        if department_id is not None:
            stmt = stmt.where(Employee.department_id == department_id)

        if active_only:
            stmt = stmt.where(Employee.employment_status == "ACTIVE")

        if manager_id is not None:
            stmt = stmt.where(Employee.manager_id == manager_id)

        return list(db.scalars(stmt.offset(skip).limit(limit)).all())

    def create(self, db: Session, employee: Employee):
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee

    def delete(self, db: Session, employee: Employee):
        db.delete(employee)
        db.commit()
