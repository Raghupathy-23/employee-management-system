from sqlalchemy.orm import Session
from app.models.department import Department
from app.repositories.department_repository import DepartmentRepository

class DepartmentService:
    def __init__(self):
        self.repository = DepartmentRepository()

    def create(self, db: Session, data):
        if self.repository.get_by_name(db, data.name):
            raise ValueError("Department name already exists")
        return self.repository.create(db, Department(**data.model_dump()))

    def list(self, db, skip=0, limit=100):
        return self.repository.list(db, skip, limit)

    def get(self, db, department_id):
        return self.repository.get_by_id(db, department_id)

    def update(self, db, department_id, data):
        department = self.get(db, department_id)
        if not department:
            return None
        values = data.model_dump(exclude_unset=True)
        if "name" in values and values["name"] != department.name:
            if self.repository.get_by_name(db, values["name"]):
                raise ValueError("Department name already exists")
        for field, value in values.items():
            setattr(department, field, value)
        db.commit()
        db.refresh(department)
        return department

    def delete(self, db, department_id):
        department = self.get(db, department_id)
        if not department:
            return False
        self.repository.delete(db, department)
        return True
