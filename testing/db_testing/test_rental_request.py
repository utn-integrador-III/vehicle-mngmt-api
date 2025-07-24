import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_all_rental_requests():
    response = client.get("/rental_request/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "message" in data
    assert "code" in data

def test_create_rental_request():
    rental_request_data = {
        "user_id": "user123",
        "vehicle_id": "vehicle123",
        "start_date": "2025-07-24",
        "end_date": "2025-07-30",
        "status": "pending"
    }

    response = client.post("/rental_request/", json=rental_request_data)
    assert response.status_code == 201
    data = response.json()
    assert "data" in data
    assert "inserted_id" in data["data"]
    assert data["code"] == "CREATED_MSG"
