from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health():
    return {"status": "ok"}


@router.get("/readiness")
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "ok"}
    except Exception as exc:
        return {"status": "not_ready", "database": "unavailable", "detail": str(exc)}
