from pydantic import BaseModel, ConfigDict, Field


class RoleBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=255)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=255)


class RoleResponse(RoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
