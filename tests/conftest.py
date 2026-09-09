import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client():
    # Tests use the application's configured database. Set TEST_DATABASE_URL
    # before running pytest when a separate test database is available.
    from app.main import app

    return TestClient(app)


@pytest.fixture
def api(client):
    return client
