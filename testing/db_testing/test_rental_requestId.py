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
