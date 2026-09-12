from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.notification import (
    NotificationListResponse,
    NotificationResponse,
    UnreadCountResponse,
)
from app.services.notification_service import NotificationService


router = APIRouter(prefix="/notifications", tags=["Notifications"])
service = NotificationService()


@router.get("", response_model=NotificationListResponse)
def list_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows, total = service.list_for_user(
        db,
        current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only,
    )
    return NotificationListResponse(
        items=rows,
        total=total,
        skip=skip,
        limit=limit,
        has_next=skip + len(rows) < total,
        has_previous=skip > 0,
    )


@router.get("/unread-count", response_model=UnreadCountResponse)
def unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {"unread_count": service.unread_count(db, current_user.id)}


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = service.mark_read(db, current_user.id, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.patch("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {"updated": service.mark_all_read(db, current_user.id)}
