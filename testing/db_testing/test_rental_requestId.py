import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

FAKE_ID = "64b9c2f5b5a9e909f24e1aaa"


def test_get_rental_request_by_id_not_found():
    response = client.get(f"/rental_requestId/{FAKE_ID}")
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "NOT_FOUND_MSG"


def test_update_rental_request_not_found():
    updated_data = {
        "start_date": "2025-08-01",
        "end_date": "2025-08-05",
        "status": "approved"
    }
    response = client.put(f"/rental_requestId/{FAKE_ID}", json=updated_data)
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "NOT_FOUND_MSG"


def test_delete_rental_request_not_found():
    response = client.delete(f"/rental_requestId/{FAKE_ID}")
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "NOT_FOUND_MSG"


def test_update_rental_request_with_conflict():
    approved_request = {
        "user_id": "user_update_conflict1",
        "vehicle_id": "vehicle_update_conflict",
        "start_date": "2025-08-20",
        "end_date": "2025-08-25",
        "status": "approved"
    }
    response1 = client.post("/rental_request/", json=approved_request)
    assert response1.status_code == 201
    approved_id = response1.json()["data"]["inserted_id"]

    pending_request = {
        "user_id": "user_update_conflict2",
        "vehicle_id": "vehicle_update_conflict",
        "start_date": "2025-08-26",
        "end_date": "2025-08-30",
        "status": "pending"
    }
    response2 = client.post("/rental_request/", json=pending_request)
    assert response2.status_code == 201
    pending_id = response2.json()["data"]["inserted_id"]

    updated_data = {
        "start_date": "2025-08-24",  # Solapa con la solicitud aprobada
        "end_date": "2025-08-28",
        "status": "approved"
    }
    response3 = client.put(
        f"/rental_requestId/{pending_id}", json=updated_data)
    assert response3.status_code == 400
    data = response3.json()
    assert data["message"] == "Time slot is already taken by an approved request."
    assert data["message_code"] == "TIME_SLOT_TAKEN"
