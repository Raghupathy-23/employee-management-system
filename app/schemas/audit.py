from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None
    action: str
    resource: str | None
    resource_id: str | None
    details: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
