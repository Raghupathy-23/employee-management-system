from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.department import Department

class DepartmentRepository:
    def get_by_id(self, db: Session, department_id: int):
        return db.get(Department, department_id)

    def get_by_name(self, db: Session, name: str):
        return db.scalar(select(Department).where(Department.name == name))

    def list(self, db: Session, skip=0, limit=100):
        return list(db.scalars(select(Department).offset(skip).limit(limit)).all())

    def create(self, db: Session, department):
        db.add(department)
        db.commit()
        db.refresh(department)
        return department

    def delete(self, db: Session, department):
        db.delete(department)
        db.commit()
