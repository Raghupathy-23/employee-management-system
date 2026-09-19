from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


ALLOWED_ATTENDANCE_STATUSES = {"PRESENT", "ABSENT", "HALF_DAY", "ON_LEAVE"}


class AttendanceBase(BaseModel):
    employee_id: int
    attendance_date: date
    check_in: datetime | None = None
    check_out: datetime | None = None
    status: str = Field(default="PRESENT", min_length=2, max_length=30)
    remarks: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_times(self):
        self.status = self.status.upper()
        if self.status not in ALLOWED_ATTENDANCE_STATUSES:
            raise ValueError("Invalid attendance status")
        if self.check_in and self.check_out and self.check_out < self.check_in:
            raise ValueError("check_out cannot be earlier than check_in")
        return self


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    attendance_date: date | None = None
    check_in: datetime | None = None
    check_out: datetime | None = None
    status: str | None = Field(default=None, min_length=2, max_length=30)
    remarks: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_times(self):
        if self.status is not None:
            self.status = self.status.upper()
            if self.status not in ALLOWED_ATTENDANCE_STATUSES:
                raise ValueError("Invalid attendance status")
        if self.check_in and self.check_out and self.check_out < self.check_in:
            raise ValueError("check_out cannot be earlier than check_in")
        return self


class AttendanceResponse(AttendanceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
