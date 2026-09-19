import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token, verify_password
from app.db.database import get_db
from app.models.user import User


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError, TypeError, ValueError):
        raise credentials_exception from None

    user = db.scalar(select(User).where(User.id == user_id).join(User.role))
    if user is None or not user.is_active or user.role is None:
        raise credentials_exception

    return user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    email = form_data.username.strip().lower()
    user = db.scalar(select(User).where(User.email == email))

    if user is None or not user.is_active or not verify_password(form_data.password, user.password_hash):
        logger.warning("Failed login attempt for %s", email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.role is None:
        logger.error("User %s has no assigned role", user.id)
        raise HTTPException(status_code=500, detail="User role is not configured")

    token = create_access_token(subject=str(user.id), role=user.role.name)
    logger.info("Successful login for user_id=%s", user.id)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def current_user(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.name,
        "is_active": user.is_active,
    }
