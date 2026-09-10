from typing import Literal

from pydantic import BaseModel, EmailStr


class NotificationMessage(BaseModel):
    channel: Literal["email", "in_app"]
    recipient: str
    subject: str
    message: str


class NotificationResult(BaseModel):
    accepted: bool
    channel: str
    recipient: str
