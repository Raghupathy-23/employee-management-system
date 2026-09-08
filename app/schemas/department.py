from pydantic import BaseModel, ConfigDict, Field

class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)

class DepartmentResponse(DepartmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
