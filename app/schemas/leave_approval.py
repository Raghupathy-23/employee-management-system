from pydantic import BaseModel, Field


class LeaveApprovalRequest(BaseModel):
    comment: str | None = Field(default=None, max_length=1000)


class LeaveApprovalResponse(BaseModel):
    id: int
    status: str
    approver_user_id: int | None
    approval_comment: str | None
