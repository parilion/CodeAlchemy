import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_enhance_missing_project_id_returns_422():
    resp = client.post("/api/enhance/", json={"modules": ["smart_search"]})
    assert resp.status_code == 422


def test_enhance_missing_modules_returns_422():
    resp = client.post("/api/enhance/", json={"project_id": "test-id"})
    assert resp.status_code == 422


def test_template_gen_missing_requirement_returns_422():
    resp = client.post("/api/templates/generate", json={"modules": []})
    assert resp.status_code == 422


def test_list_projects_returns_list():
    resp = client.get("/api/projects/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_enhance_nonexistent_project_returns_404():
    resp = client.post("/api/enhance/", json={
        "project_id": "nonexistent-project-id-xyz",
        "modules": ["smart_search"]
    })
    assert resp.status_code == 404
