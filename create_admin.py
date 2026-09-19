import argparse
from getpass import getpass

from sqlalchemy import select

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models.role import Role
from app.models.user import User


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an administrator account")
    parser.add_argument("--email", required=True, help="Administrator email address")
    args = parser.parse_args()

    password = getpass("Password: ")
    confirm = getpass("Confirm password: ")
    if password != confirm:
        raise SystemExit("Passwords do not match.")
    if len(password) < 8:
        raise SystemExit("Password must contain at least 8 characters.")

    email = args.email.strip().lower()
    with SessionLocal() as db:
        role = db.scalar(select(Role).where(Role.name == "ADMIN"))
        if role is None:
            raise SystemExit("ADMIN role does not exist. Run: python scripts/seed_roles.py")

        existing_user = db.scalar(select(User).where(User.email == email))
        if existing_user:
            raise SystemExit(f"User already exists: {email}")

        user = User(
            email=email,
            password_hash=hash_password(password),
            role_id=role.id,
            is_active=True,
        )
        db.add(user)
        db.commit()
        print(f"Administrator created: {email}")


if __name__ == "__main__":
    main()
