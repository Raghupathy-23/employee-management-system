from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationCreate(BaseModel):
    user_id: int
    notification_type: str = Field(default="SYSTEM", max_length=50)
    title: str = Field(min_length=1, max_length=150)
    message: str = Field(min_length=1)
    link: str | None = Field(default=None, max_length=255)


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    notification_type: str
    title: str
    message: str
    link: str | None
    is_read: bool
    created_at: datetime
    read_at: datetime | None


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool


class UnreadCountResponse(BaseModel):
    unread_count: int


class NotificationMessage(BaseModel):
    channel: str
    recipient: str
    subject: str
    message: str


class NotificationDeliveryResult(BaseModel):
    channel: str
    recipient: str
    accepted: bool