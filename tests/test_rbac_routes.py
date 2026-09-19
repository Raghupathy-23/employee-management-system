def test_role_admin_endpoints_require_authentication(api):
    assert api.get("/api/v1/roles").status_code in {401, 403}


def test_employee_create_requires_authentication(api):
    response = api.post("/api/v1/employees", json={})
    assert response.status_code in {401, 403, 422}


def test_department_create_requires_authentication(api):
    response = api.post("/api/v1/departments", json={})
    assert response.status_code in {401, 403, 422}
