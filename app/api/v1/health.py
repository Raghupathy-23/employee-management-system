from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health():
    return {"status": "ok", "service": settings.app_name}


@router.get("/readiness")
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "database": "unavailable"},
        ) from None
    return {"status": "ready", "database": "ok"}
