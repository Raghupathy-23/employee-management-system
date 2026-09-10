from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.leave import Leave


# Keep the first version intentionally simple and easy to change later.
# UNPAID is not limited by a yearly allowance.
LEAVE_ALLOWANCES: dict[str, int | None] = {
    "ANNUAL": 18,
    "SICK": 12,
    "CASUAL": 12,
    "UNPAID": None,
    "OTHER": 0,
}


class LeaveBalanceService:
    def _days_in_year(self, start_date: date, end_date: date, year: int) -> int:
        year_start = date(year, 1, 1)
        year_end = date(year, 12, 31)
        start = max(start_date, year_start)
        end = min(end_date, year_end)
        if end < start:
            return 0
        return (end - start).days + 1

    def _days_by_status(
        self,
        db: Session,
        employee_id: int,
        leave_type: str,
        year: int,
    ) -> tuple[int, int]:
        stmt = select(Leave).where(
            Leave.employee_id == employee_id,
            Leave.leave_type == leave_type,
            Leave.status.in_(["PENDING", "APPROVED"]),
            Leave.start_date <= date(year, 12, 31),
            Leave.end_date >= date(year, 1, 1),
        )

        approved_days = 0
        pending_days = 0

        for leave in db.scalars(stmt).all():
            days = self._days_in_year(leave.start_date, leave.end_date, year)
            if leave.status == "APPROVED":
                approved_days += days
            else:
                pending_days += days

        return approved_days, pending_days

    def get_balance(
        self,
        db: Session,
        employee_id: int,
        year: int,
    ) -> dict:
        balances = []

        for leave_type, allowance in LEAVE_ALLOWANCES.items():
            approved_days, pending_days = self._days_by_status(
                db,
                employee_id,
                leave_type,
                year,
            )

            if allowance is None:
                available_days = None
            else:
                available_days = max(
                    allowance - approved_days - pending_days,
                    0,
                )

            balances.append(
                {
                    "leave_type": leave_type,
                    "allowance_days": allowance,
                    "approved_days": approved_days,
                    "pending_days": pending_days,
                    "available_days": available_days,
                }
            )

        return {
            "employee_id": employee_id,
            "year": year,
            "balances": balances,
        }

    def validate_request(
        self,
        db: Session,
        employee_id: int,
        leave_type: str,
        start_date: date,
        end_date: date,
    ) -> None:
        leave_type = leave_type.upper()

        if leave_type not in LEAVE_ALLOWANCES:
            raise ValueError("Invalid leave type")

        allowance = LEAVE_ALLOWANCES[leave_type]
        if allowance is None:
            return

        # A request spanning two calendar years is validated one year at a time.
        for year in range(start_date.year, end_date.year + 1):
            requested_days = self._days_in_year(start_date, end_date, year)
            if requested_days == 0:
                continue

            approved_days, pending_days = self._days_by_status(
                db,
                employee_id,
                leave_type,
                year,
            )
            available_days = allowance - approved_days - pending_days

            if requested_days > max(available_days, 0):
                raise ValueError(
                    f"Insufficient {leave_type} leave balance for {year}. "
                    f"Available: {max(available_days, 0)} day(s), "
                    f"requested: {requested_days} day(s)"
                )
