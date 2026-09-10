from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class AttendanceBase(BaseModel):
    employee_id: int
    attendance_date: date
    check_in: datetime | None = None
    check_out: datetime | None = None
    status: str = Field(default="PRESENT", min_length=2, max_length=30)
    remarks: str | None = Field(default=None, max_length=1000)


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    attendance_date: date | None = None
    check_in: datetime | None = None
    check_out: datetime | None = None
    status: str | None = Field(default=None, min_length=2, max_length=30)
    remarks: str | None = Field(default=None, max_length=1000)


class AttendanceResponse(AttendanceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
