def test_health(api):
    response = api.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness(api):
    response = api.get("/health/readiness")
    assert response.status_code == 200
    assert response.json()["status"] in {"ready", "not_ready"}
