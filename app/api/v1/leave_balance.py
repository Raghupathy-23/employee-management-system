from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.leave_balance import LeaveBalanceResponse
from app.services.leave_balance_service import LeaveBalanceService

router = APIRouter(tags=["Leave Balance"])
service = LeaveBalanceService()


@router.get("/employees/{employee_id}/leave-balance", response_model=LeaveBalanceResponse)
def get_leave_balance(
    employee_id: int,
    year: int | None = Query(default=None, ge=2000, le=2100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.name.upper()
    if role == "EMPLOYEE" and getattr(current_user.employee, "id", None) != employee_id:
        raise HTTPException(status_code=403, detail="You can only access your own leave balance")
    if role == "MANAGER":
        from app.repositories.employee_repository import EmployeeRepository
        employee = EmployeeRepository().get_by_id(db, employee_id)
        if employee is None or employee.manager_id != getattr(current_user.employee, "id", None):
            raise HTTPException(status_code=403, detail="You can only access leave balance for your direct reports")
    target_year = year or date.today().year
    return service.get_balance(db, employee_id, target_year)
