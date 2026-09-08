from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db


router = APIRouter(
    prefix="/system",
    tags=["System"],
)


@router.get("/info")
def system_info():
    return {
        "application": "Employee Management System",
        "version": "0.3.0",
        "environment": "development",
    }


@router.get("/database")
def database_status(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "database": "mysql",
        "status": "connected",
    }
