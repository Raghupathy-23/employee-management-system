from app.schemas.notification import NotificationCreate


def test_notification_create_schema():
    payload = NotificationCreate(
        user_id=1,
        notification_type="LEAVE",
        title="Leave approved",
        message="Your leave request was approved.",
        link="/leaves/10",
    )

    assert payload.user_id == 1
    assert payload.notification_type == "LEAVE"
    assert payload.link == "/leaves/10"
