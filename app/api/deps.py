from fastapi import Depends, HTTPException, status

from app.api.v1.auth import get_current_user
from app.models.user import User


ADMIN_ROLES = {"ADMIN"}
HR_ROLES = {"ADMIN", "HR", "HR_MANAGER"}
MANAGEMENT_ROLES = {"ADMIN", "HR", "HR_MANAGER", "MANAGER"}


def require_roles(*allowed_roles: str):
    allowed = {role.upper() for role in allowed_roles}

    def dependency(user: User = Depends(get_current_user)) -> User:
        role_name = (user.role.name if user.role else "").upper()
        if role_name not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return user

    return dependency
