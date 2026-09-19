from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository


class EmployeeService:
    def __init__(self) -> None:
        self.repository = EmployeeRepository()

    def create(self, db: Session, data) -> Employee:
        if self.repository.get_by_code(db, data.employee_code):
            raise ValueError("Employee code already exists")
        if self.repository.get_by_user_id(db, data.user_id):
            raise ValueError("Employee already exists for this user")
        return self.repository.create(db, Employee(**data.model_dump()))

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        department_id: int | None = None,
        active_only: bool = True,
        manager_id: int | None = None,
    ) -> list[Employee]:
        return self.repository.list(db, skip, limit, search, department_id, active_only, manager_id)

    def get(self, db: Session, employee_id: int) -> Employee | None:
        return self.repository.get_by_id(db, employee_id)

    def update(self, db: Session, employee_id: int, data) -> Employee | None:
        employee = self.get(db, employee_id)
        if not employee:
            return None

        values = data.model_dump(exclude_unset=True)
        if "employee_code" in values:
            existing = self.repository.get_by_code(db, values["employee_code"])
            if existing and existing.id != employee.id:
                raise ValueError("Employee code already exists")
        if "user_id" in values:
            existing = self.repository.get_by_user_id(db, values["user_id"])
            if existing and existing.id != employee.id:
                raise ValueError("Employee already exists for this user")

        for field, value in values.items():
            setattr(employee, field, value)
        db.commit()
        db.refresh(employee)
        return employee

    def delete(self, db: Session, employee_id: int) -> bool:
        employee = self.get(db, employee_id)
        if not employee:
            return False
        self.repository.delete(db, employee)
        return True
