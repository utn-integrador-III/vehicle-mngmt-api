import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_vehicles():
    response = client.get("/car/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "message" in data
    assert "code" in data

def test_create_vehicle():
    vehicle_data = {
        "plate": "TEST-123",
        "photo": "http://photo.url/test.jpg",
        "model": "Sedan",
        "type": "Personal",
        "brand": "Toyota",
        "year": "2020",
        "status": "available"
    }
    response = client.post("/car/", json=vehicle_data)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Car created"
    assert "data" in data
    assert "id" in data["data"]
