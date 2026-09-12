from datetime import datetime

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import (
    NotificationCreate,
    NotificationDeliveryResult,
    NotificationMessage,
)


class NotificationService:
    """Persistence-backed in-app notification service.

    Delivery providers such as email or push can be added later without
    changing the application-facing notification model.
    """

    def create(self, db: Session, payload: NotificationCreate) -> Notification:
        notification = Notification(**payload.model_dump())
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    def send(
        self,
        notification: NotificationMessage,
    ) -> NotificationDeliveryResult:
        """Prepare a notification for delivery.

        Actual email/push providers can be integrated later.
        """
        return NotificationDeliveryResult(
            channel=notification.channel,
            recipient=notification.recipient,
            accepted=False,
        )

    def list_for_user(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False,
    ) -> tuple[list[Notification], int]:
        filters = [Notification.user_id == user_id]

        if unread_only:
            filters.append(Notification.is_read.is_(False))

        total = db.scalar(
            select(func.count(Notification.id)).where(*filters)
        ) or 0

        rows = db.scalars(
            select(Notification)
            .where(*filters)
            .order_by(
                Notification.created_at.desc(),
                Notification.id.desc(),
            )
            .offset(skip)
            .limit(limit)
        ).all()

        return rows, total

    def unread_count(self, db: Session, user_id: int) -> int:
        return db.scalar(
            select(func.count(Notification.id)).where(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
        ) or 0

    def mark_read(
        self,
        db: Session,
        user_id: int,
        notification_id: int,
    ) -> Notification | None:
        notification = db.scalar(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        )

        if not notification:
            return None

        if not notification.is_read:
            notification.is_read = True
            notification.read_at = datetime.utcnow()

            db.commit()
            db.refresh(notification)

        return notification

    def mark_all_read(self, db: Session, user_id: int) -> int:
        now = datetime.utcnow()

        result = db.execute(
            update(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .values(
                is_read=True,
                read_at=now,
            )
        )

        db.commit()

        return result.rowcount or 0