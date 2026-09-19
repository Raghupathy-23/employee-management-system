from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.role_repository import RoleRepository


SUPPORTED_ROLES = {"ADMIN", "HR", "HR_MANAGER", "MANAGER", "EMPLOYEE"}


class RoleService:
    def __init__(self) -> None:
        self.repository = RoleRepository()

    def create(self, db: Session, data) -> Role:
        name = data.name.strip().upper()
        if name not in SUPPORTED_ROLES:
            raise ValueError(f"Unsupported role. Allowed values: {', '.join(sorted(SUPPORTED_ROLES))}")
        if self.repository.get_by_name(db, name):
            raise ValueError("Role name already exists")
        return self.repository.create(db, Role(name=name, description=data.description))

    def list(self, db: Session, skip: int = 0, limit: int = 100) -> list[Role]:
        return self.repository.list(db, skip, limit)

    def get(self, db: Session, role_id: int) -> Role | None:
        return self.repository.get_by_id(db, role_id)

    def update(self, db: Session, role_id: int, data) -> Role | None:
        role = self.get(db, role_id)
        if not role:
            return None
        values = data.model_dump(exclude_unset=True)
        if "name" in values:
            values["name"] = values["name"].strip().upper()
            if values["name"] not in SUPPORTED_ROLES:
                raise ValueError(f"Unsupported role. Allowed values: {', '.join(sorted(SUPPORTED_ROLES))}")
            existing = self.repository.get_by_name(db, values["name"])
            if existing and existing.id != role.id:
                raise ValueError("Role name already exists")
        for field, value in values.items():
            setattr(role, field, value)
        db.commit()
        db.refresh(role)
        return role

    def delete(self, db: Session, role_id: int) -> bool:
        role = self.get(db, role_id)
        if not role:
            return False
        if role.users:
            raise ValueError("Role cannot be deleted while users are assigned to it")
        self.repository.delete(db, role)
        return True
