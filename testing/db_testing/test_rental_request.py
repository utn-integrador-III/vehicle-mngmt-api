import pytest
from fastapi.testclient import TestClient
from app import app
from models.rental_request.model import RentalRequestModel

client = TestClient(app)

# Lista para almacenar IDs creados durante las pruebas
created_ids = []


@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Fixture que se ejecuta después de cada test para limpiar los datos creados"""
    yield
    # Limpiar todos los registros creados durante la prueba
    for rental_id in created_ids:
        try:
            RentalRequestModel.delete(rental_id)
        except:
            pass
    created_ids.clear()


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
        "start_date": "2025-12-24",
        "end_date": "2025-12-30",
        "status": "pending"
    }

    response = client.post("/rental_request/", json=rental_request_data)
    assert response.status_code == 201
    data = response.json()
    assert "data" in data
    assert "inserted_id" in data["data"]
    assert data["code"] == "CREATED_MSG"

    # Agregar el ID a la lista para limpieza
    created_ids.append(data["data"]["inserted_id"])


def test_conflict_on_approved_rental_request():
    """Test que verifica conflicto entre solicitudes aprobadas para el mismo vehículo"""
    approved_request = {
        "user_id": "user_conflict1",
        "vehicle_id": "vehicle_conflict1",
        "start_date": "2025-12-10",
        "end_date": "2025-12-15",
        "status": "approved"
    }
    response = client.post("/rental_request/", json=approved_request)
    assert response.status_code == 201
    approved_id = response.json()["data"]["inserted_id"]
    created_ids.append(approved_id)

    conflicting_request = {
        "user_id": "user_conflict2",
        "vehicle_id": "vehicle_conflict1",  # mismo vehículo
        "start_date": "2025-12-12",         # fechas se solapan
        "end_date": "2025-12-17",
        "status": "approved"
    }
    response = client.post("/rental_request/", json=conflicting_request)
    assert response.status_code == 400
    data = response.json()
    assert "Time slot is already taken by an approved or pending request for this vehicle" in data[
        "message"]
    assert data["message_code"] == "TIME_SLOT_TAKEN"


def test_conflict_on_pending_rental_request():
    """Test que verifica conflicto entre solicitudes pendientes para el mismo vehículo"""
    pending_request = {
        "user_id": "user_pending1",
        "vehicle_id": "vehicle_pending1",
        "start_date": "2026-01-01",
        "end_date": "2026-01-05",
        "status": "pending"
    }
    response = client.post("/rental_request/", json=pending_request)
    assert response.status_code == 201
    pending_id = response.json()["data"]["inserted_id"]
    created_ids.append(pending_id)

    conflicting_request = {
        "user_id": "user_pending2",
        "vehicle_id": "vehicle_pending1",  # mismo vehículo
        "start_date": "2026-01-03",        # fechas se solapan
        "end_date": "2026-01-07",
        "status": "pending"
    }
    response = client.post("/rental_request/", json=conflicting_request)
    assert response.status_code == 400
    data = response.json()
    assert "Time slot is already taken by an approved or pending request for this vehicle" in data[
        "message"]
    assert data["message_code"] == "TIME_SLOT_TAKEN"


def test_no_conflict_different_vehicles():
    """Test que verifica que NO hay conflicto entre solicitudes para diferentes vehículos"""
    request1 = {
        "user_id": "user_different1",
        "vehicle_id": "vehicle_different1",
        "start_date": "2026-02-10",
        "end_date": "2026-02-15",
        "status": "approved"
    }
    response1 = client.post("/rental_request/", json=request1)
    assert response1.status_code == 201
    id1 = response1.json()["data"]["inserted_id"]
    created_ids.append(id1)

    request2 = {
        "user_id": "user_different2",
        "vehicle_id": "vehicle_different2",  # vehículo diferente
        "start_date": "2026-02-12",          # fechas se solapan pero es otro vehículo
        "end_date": "2026-02-17",
        "status": "approved"
    }
    response2 = client.post("/rental_request/", json=request2)
    assert response2.status_code == 201  # No debe haber conflicto
    id2 = response2.json()["data"]["inserted_id"]
    created_ids.append(id2)


def test_no_conflict_with_rejected_request():
    """Test que verifica que NO hay conflicto con solicitudes rechazadas"""
    rejected_request = {
        "user_id": "user_rejected1",
        "vehicle_id": "vehicle_rejected1",
        "start_date": "2026-03-20",
        "end_date": "2026-03-25",
        "status": "rejected"
    }
    response1 = client.post("/rental_request/", json=rejected_request)
    assert response1.status_code == 201
    rejected_id = response1.json()["data"]["inserted_id"]
    created_ids.append(rejected_id)

    overlapping_request = {
        "user_id": "user_rejected2",
        "vehicle_id": "vehicle_rejected1",  # mismo vehículo
        "start_date": "2026-03-22",         # fechas se solapan
        "end_date": "2026-03-27",
        "status": "pending"
    }
    response2 = client.post("/rental_request/", json=overlapping_request)
    assert response2.status_code == 201  # No debe haber conflicto con rejected
    id2 = response2.json()["data"]["inserted_id"]
    created_ids.append(id2)


def test_conflict_approved_with_pending():
    """Test que verifica conflicto entre solicitud aprobada y nueva solicitud pendiente"""
    approved_request = {
        "user_id": "user_mixed1",
        "vehicle_id": "vehicle_mixed1",
        "start_date": "2026-04-01",
        "end_date": "2026-04-05",
        "status": "approved"
    }
    response1 = client.post("/rental_request/", json=approved_request)
    assert response1.status_code == 201
    approved_id = response1.json()["data"]["inserted_id"]
    created_ids.append(approved_id)

    pending_request = {
        "user_id": "user_mixed2",
        "vehicle_id": "vehicle_mixed1",  # mismo vehículo
        "start_date": "2026-04-03",      # fechas se solapan
        "end_date": "2026-04-07",
        "status": "pending"
    }
    response2 = client.post("/rental_request/", json=pending_request)
    assert response2.status_code == 400
    data = response2.json()
    assert "Time slot is already taken by an approved or pending request for this vehicle" in data[
        "message"]
    assert data["message_code"] == "TIME_SLOT_TAKEN"
