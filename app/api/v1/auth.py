from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token, verify_password
from app.db.database import get_db
from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

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
    except JWTError:
        raise credentials_exception

    user = db.get(User, int(user_id))

    if user is None or not user.is_active:
        raise credentials_exception

    return user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    print("LOGIN: request received", flush=True)
    print(f"LOGIN: email = {form_data.username}", flush=True)

    user = db.scalar(
        select(User).where(User.email == form_data.username)
    )

    print(f"LOGIN: user = {user}", flush=True)

    if user is None:
        print("LOGIN ERROR: user not found", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"LOGIN: user id = {user.id}", flush=True)
    print(f"LOGIN: role_id = {user.role_id}", flush=True)
    print(f"LOGIN: password hash exists = {bool(user.password_hash)}", flush=True)

    password_valid = verify_password(
        form_data.password,
        user.password_hash,
    )

    print(f"LOGIN: password valid = {password_valid}", flush=True)

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print("LOGIN: password verified", flush=True)

    print(f"LOGIN: role = {user.role}", flush=True)

    token = create_access_token(
        subject=str(user.id),
        role=user.role.name,
    )

    print("LOGIN: token created", flush=True)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
def current_user(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.name,
        "is_active": user.is_active,
    }
