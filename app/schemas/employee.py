from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class EmployeeBase(BaseModel):
    employee_code: str = Field(
        ...,
        min_length=2,
        max_length=30,
    )

    user_id: int
    department_id: int
    manager_id: int | None = None

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    date_of_birth: date | None = None

    date_of_joining: date

    designation: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    employment_status: str = Field(
        default="ACTIVE",
        max_length=30,
    )


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    date_of_birth: date | None = None

    date_of_joining: date | None = None

    designation: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    department_id: int | None = None
    manager_id: int | None = None

    employment_status: str | None = Field(
        default=None,
        max_length=30,
    )


class EmployeeResponse(EmployeeBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )