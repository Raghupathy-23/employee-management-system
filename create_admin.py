from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models.user import User
from app.models.role import Role


email = "admin@example.com"
password = "Admin@123"

db = SessionLocal()

try:
    role = db.query(Role).filter(Role.name == "ADMIN").first()

    if role is None:
        raise RuntimeError("ADMIN role does not exist.")

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        print(f"User already exists: {email}")
    else:
        user = User(
            email=email,
            password_hash=hash_password(password),
            role_id=role.id,
            is_active=True,
        )

        db.add(user)
        db.commit()

        print("Admin user created successfully.")
        print(f"Email: {email}")
        print(f"Password: {password}")

finally:
    db.close()