from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LeaveBase(BaseModel):
    employee_id: int
    leave_type: str = Field(..., min_length=2, max_length=30)
    start_date: date
    end_date: date
    reason: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date")
        return self


class LeaveCreate(LeaveBase):
    pass


class LeaveUpdate(BaseModel):
    leave_type: str | None = Field(default=None, min_length=2, max_length=30)
    start_date: date | None = None
    end_date: date | None = None
    reason: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date")
        return self


class LeaveResponse(LeaveBase):
    id: int
    status: str
    approver_user_id: int | None = None
    approval_comment: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
