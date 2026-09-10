from pydantic import BaseModel, Field


class LeaveTypeBalance(BaseModel):
    leave_type: str
    allowance_days: int | None = Field(
        description="Configured yearly allowance. None means unlimited."
    )
    approved_days: int
    pending_days: int
    available_days: int | None = Field(
        description="Remaining days after approved and pending requests."
    )


class LeaveBalanceResponse(BaseModel):
    employee_id: int
    year: int
    balances: list[LeaveTypeBalance]
