def test_protected_me_requires_authentication(api):
    response = api.get("/api/v1/auth/me")
    assert response.status_code in {401, 403}
