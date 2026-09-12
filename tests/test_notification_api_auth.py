def test_notifications_requires_authentication(api):
    response = api.get("/api/v1/notifications")
    assert response.status_code in {401, 403}


def test_notification_unread_count_requires_authentication(api):
    response = api.get("/api/v1/notifications/unread-count")
    assert response.status_code in {401, 403}
