from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:
    def get_by_id(self, db: Session, role_id: int) -> Role | None:
        return db.get(Role, role_id)

    def get_by_name(self, db: Session, name: str) -> Role | None:
        return db.scalar(select(Role).where(Role.name == name))

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[Role]:
        stmt = select(Role).order_by(Role.name).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def create(self, db: Session, role: Role) -> Role:
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    def delete(self, db: Session, role: Role) -> None:
        db.delete(role)
        db.commit()
