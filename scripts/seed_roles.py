from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.role import Role


DEFAULT_ROLES = [
    ("ADMIN", "System administrator"),
    ("HR", "Human resources user"),
    ("MANAGER", "Department or team manager"),
    ("EMPLOYEE", "Standard employee"),
]


def seed_roles() -> None:
    with SessionLocal() as db:
        for name, description in DEFAULT_ROLES:
            existing = db.scalar(select(Role).where(Role.name == name))
            if existing is None:
                db.add(Role(name=name, description=description))
        db.commit()


if __name__ == "__main__":
    seed_roles()
    print("Default roles seeded successfully.")
