import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_vehicle_by_id_not_found():
    response = client.get("/car/64b9c2f5b5a9e909f24e1aaa")  # id inventado
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "CAR_NOT_FOUND"

def test_update_vehicle_not_found():
    updated_data = {
        "plate": "TEST-123",
        "photo": "http://photo.url/test.jpg",
        "model": "Sedan",
        "type": "Personal",
        "brand": "Toyota",
        "year": "2020",
        "status": "available"
    }
    response = client.put("/car/64b9c2f5b5a9e909f24e1aaa", json=updated_data)
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "CAR_NOT_FOUND"

def test_delete_vehicle_not_found():
    response = client.delete("/car/64b9c2f5b5a9e909f24e1aaa")
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "CAR_NOT_FOUND"
