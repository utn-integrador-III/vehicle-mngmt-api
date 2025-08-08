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


def test_conflict_on_approved_rental_request():
    approved_request = {
        "user_id": "user_conflict1",
        "vehicle_id": "vehicle_conflict1",
        "start_date": "2025-08-10",
        "end_date": "2025-08-15",
        "status": "approved"
    }
    response = client.post("/rental_request/", json=approved_request)
    assert response.status_code == 201
    approved_id = response.json()["data"]["inserted_id"]

    conflicting_request = {
        "user_id": "user_conflict2",
        "vehicle_id": "vehicle_conflict1",  # mismo vehículo
        "start_date": "2025-08-12",         # fechas se solapan
        "end_date": "2025-08-17",
        "status": "approved"
    }
    response = client.post("/rental_request/", json=conflicting_request)
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "Time slot is already taken by an approved request."
    assert data["message_code"] == "TIME_SLOT_TAKEN"
