"""Router tests for departments endpoints."""

from fastapi.testclient import TestClient

from app.main import app
from app.routers.departments import get_department_service


class StubDepartmentService:
    def list_departments(self):
        return [{"id": 1, "name": "Engineering", "description": "Core team"}]

    def create_department(self, name: str, description: str | None):
        return {"id": 2, "name": name, "description": description}



def test_list_departments_returns_200_and_payload() -> None:
    app.dependency_overrides[get_department_service] = lambda: StubDepartmentService()
    client = TestClient(app)

    response = client.get("/departments")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Engineering", "description": "Core team"}]

    app.dependency_overrides.clear()



def test_create_department_returns_201() -> None:
    app.dependency_overrides[get_department_service] = lambda: StubDepartmentService()
    client = TestClient(app)

    response = client.post("/departments", json={"name": "HR", "description": "People Ops"})

    assert response.status_code == 201
    assert response.json()["name"] == "HR"

    app.dependency_overrides.clear()
