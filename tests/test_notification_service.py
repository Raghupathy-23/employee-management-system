from app.schemas.notification import NotificationMessage
from app.services.notification_service import NotificationService


def test_notification_service_contract():
    result = NotificationService().send(
        NotificationMessage(
            channel="email",
            recipient="test@example.com",
            subject="Test",
            message="Hello",
        )
    )
    assert result.channel == "email"
    assert result.recipient == "test@example.com"
    assert result.accepted is False
