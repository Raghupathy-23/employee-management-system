from app.schemas.notification import NotificationMessage, NotificationResult


class NotificationService:
    """Small provider-neutral notification interface.

    Phase 8 only defines the contract. Real email/in-app providers can be
    plugged in later without changing business services.
    """

    def send(self, message: NotificationMessage) -> NotificationResult:
        # Deliberately do not send external messages yet.
        return NotificationResult(
            accepted=False,
            channel=message.channel,
            recipient=message.recipient,
        )
