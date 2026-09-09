from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.leave_balance import LeaveBalanceResponse
from app.services.leave_balance_service import LeaveBalanceService


router = APIRouter(tags=["Leave Balance"])
service = LeaveBalanceService()


@router.get(
    "/employees/{employee_id}/leave-balance",
    response_model=LeaveBalanceResponse,
)
def get_leave_balance(
    employee_id: int,
    year: int | None = Query(default=None, ge=2000, le=2100),
    db: Session = Depends(get_db),
):
    target_year = year or date.today().year
    return service.get_balance(db, employee_id, target_year)
