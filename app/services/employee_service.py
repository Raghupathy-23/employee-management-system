from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository


class EmployeeService:
    def __init__(self):
        self.repository = EmployeeRepository()

    def create(self, db: Session, data):
        if self.repository.get_by_code(db, data.employee_code):
            raise ValueError("Employee code already exists")

        if self.repository.get_by_user_id(db, data.user_id):
            raise ValueError("Employee already exists for this user")

        employee = Employee(**data.model_dump())

        return self.repository.create(db, employee)

    def list(
        self,
        db,
        skip=0,
        limit=100,
        search=None,
        department_id=None,
        active_only=True,
    ):
        return self.repository.list(
            db,
            skip,
            limit,
            search,
            department_id,
            active_only,
        )

    def get(self, db, employee_id):
        return self.repository.get_by_id(db, employee_id)

    def update(self, db, employee_id, data):
        employee = self.get(db, employee_id)

        if not employee:
            return None

        values = data.model_dump(exclude_unset=True)

        if "employee_code" in values:
            existing = self.repository.get_by_code(
                db,
                values["employee_code"],
            )

            if existing and existing.id != employee.id:
                raise ValueError("Employee code already exists")

        if "user_id" in values:
            existing = self.repository.get_by_user_id(
                db,
                values["user_id"],
            )

            if existing and existing.id != employee.id:
                raise ValueError(
                    "Employee already exists for this user"
                )

        for field, value in values.items():
            setattr(employee, field, value)

        db.commit()
        db.refresh(employee)

        return employee

    def delete(self, db, employee_id):
        employee = self.get(db, employee_id)

        if not employee:
            return False

        self.repository.delete(db, employee)

        return True