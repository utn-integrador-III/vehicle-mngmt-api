import pytest
from fastapi.testclient import TestClient
from app import app
from models.rental_request.model import RentalRequestModel

client = TestClient(app)

FAKE_ID = "64b9c2f5b5a9e909f24e1aaa"

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


def test_get_rental_request_by_id_not_found():
    response = client.get(f"/rental_requestId/{FAKE_ID}")
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "NOT_FOUND_MSG"


def test_update_rental_request_not_found():
    updated_data = {
        "start_date": "2026-01-01",
        "end_date": "2026-01-05",
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


def test_successful_get_rental_request_by_id():
    """Test que verifica obtener una solicitud por ID exitosamente"""
    rental_request = {
        "user_id": "user_get_test",
        "vehicle_id": "vehicle_get_test",
        "start_date": "2026-05-01",
        "end_date": "2026-05-05",
        "status": "pending"
    }
    response = client.post("/rental_request/", json=rental_request)
    assert response.status_code == 201
    rental_id = response.json()["data"]["inserted_id"]
    created_ids.append(rental_id)

    # Obtener por ID
    response = client.get(f"/rental_requestId/{rental_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["user_id"] == "user_get_test"
    assert data["data"]["vehicle_id"] == "vehicle_get_test"


def test_successful_update_rental_request_status_only():
    """Test que verifica actualización exitosa de solo el status"""
    rental_request = {
        "user_id": "user_update_success",
        "vehicle_id": "vehicle_update_success",
        "start_date": "2026-05-10",
        "end_date": "2026-05-15",
        "status": "pending"
    }
    response = client.post("/rental_request/", json=rental_request)
    assert response.status_code == 201
    rental_id = response.json()["data"]["inserted_id"]
    created_ids.append(rental_id)

    # Actualizar solo el status (sin fechas)
    updated_data = {
        "status": "rejected"  # rejected no genera conflictos
    }
    response = client.put(f"/rental_requestId/{rental_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["modified"] == 1


def test_successful_delete_rental_request():
    """Test que verifica eliminación exitosa de una solicitud"""
    rental_request = {
        "user_id": "user_delete_test",
        "vehicle_id": "vehicle_delete_test",
        "start_date": "2026-05-20",
        "end_date": "2026-05-25",
        "status": "pending"
    }
    response = client.post("/rental_request/", json=rental_request)
    assert response.status_code == 201
    rental_id = response.json()["data"]["inserted_id"]

    # Eliminar (no agregamos a created_ids porque se va a eliminar)
    response = client.delete(f"/rental_requestId/{rental_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["deleted"] == True


def test_update_rental_request_with_approved_conflict():
    """Test que verifica conflicto al actualizar fechas con solicitud aprobada existente"""
    # Crear solicitud aprobada
    approved_request = {
        "user_id": "user_update_conflict1",
        "vehicle_id": "vehicle_update_conflict",
        "start_date": "2026-06-20",
        "end_date": "2026-06-25",
        "status": "approved"
    }
    response1 = client.post("/rental_request/", json=approved_request)
    assert response1.status_code == 201
    approved_id = response1.json()["data"]["inserted_id"]
    created_ids.append(approved_id)

    # Crear solicitud pendiente
    pending_request = {
        "user_id": "user_update_conflict2",
        "vehicle_id": "vehicle_update_conflict",  # mismo vehículo
        "start_date": "2026-06-26",
        "end_date": "2026-06-30",
        "status": "pending"
    }
    response2 = client.post("/rental_request/", json=pending_request)
    assert response2.status_code == 201
    pending_id = response2.json()["data"]["inserted_id"]
    created_ids.append(pending_id)

    # Intentar actualizar fechas para que solape con la aprobada
    updated_data = {
        "start_date": "2026-06-24",  # Solapa con la solicitud aprobada
        "end_date": "2026-06-28"
    }
    response3 = client.put(
        f"/rental_requestId/{pending_id}", json=updated_data)
    assert response3.status_code == 400
    data = response3.json()
    assert "Time slot is already taken by an approved or pending request for this vehicle" in data[
        "message"]
    assert data["message_code"] == "TIME_SLOT_TAKEN"


def test_update_rental_request_with_pending_conflict():
    """Test que verifica conflicto al actualizar fechas con solicitud pendiente existente"""
    # Crear primera solicitud pendiente
    pending_request1 = {
        "user_id": "user_pending_conflict1",
        "vehicle_id": "vehicle_pending_conflict",
        "start_date": "2026-07-01",
        "end_date": "2026-07-05",
        "status": "pending"
    }
    response1 = client.post("/rental_request/", json=pending_request1)
    assert response1.status_code == 201
    pending_id1 = response1.json()["data"]["inserted_id"]
    created_ids.append(pending_id1)

    # Crear segunda solicitud pendiente
    pending_request2 = {
        "user_id": "user_pending_conflict2",
        "vehicle_id": "vehicle_pending_conflict",  # mismo vehículo
        "start_date": "2026-07-06",
        "end_date": "2026-07-10",
        "status": "pending"
    }
    response2 = client.post("/rental_request/", json=pending_request2)
    assert response2.status_code == 201
    pending_id2 = response2.json()["data"]["inserted_id"]
    created_ids.append(pending_id2)

    # Intentar actualizar fechas de la segunda para que solape con la primera
    updated_data = {
        "start_date": "2026-07-04",  # Solapa con la primera solicitud pendiente
        "end_date": "2026-07-08"
    }
    response3 = client.put(
        f"/rental_requestId/{pending_id2}", json=updated_data)
    assert response3.status_code == 400
    data = response3.json()
    assert "Time slot is already taken by an approved or pending request for this vehicle" in data[
        "message"]
    assert data["message_code"] == "TIME_SLOT_TAKEN"


def test_update_no_conflict_different_vehicle():
    """Test que verifica que NO hay conflicto al actualizar para vehículo diferente"""
    # Crear solicitud para vehículo 1
    request1 = {
        "user_id": "user_no_conflict1",
        "vehicle_id": "vehicle_no_conflict1",
        "start_date": "2026-08-01",
        "end_date": "2026-08-05",
        "status": "approved"
    }
    response1 = client.post("/rental_request/", json=request1)
    assert response1.status_code == 201
    id1 = response1.json()["data"]["inserted_id"]
    created_ids.append(id1)

    # Crear solicitud para vehículo 2
    request2 = {
        "user_id": "user_no_conflict2",
        "vehicle_id": "vehicle_no_conflict2",
        "start_date": "2026-08-06",
        "end_date": "2026-08-10",
        "status": "pending"
    }
    response2 = client.post("/rental_request/", json=request2)
    assert response2.status_code == 201
    id2 = response2.json()["data"]["inserted_id"]
    created_ids.append(id2)

    # Actualizar fechas de la segunda para que solape en fechas pero es vehículo diferente
    updated_data = {
        "start_date": "2026-08-03",  # Solapa en fechas
        "end_date": "2026-08-07"
    }
    response3 = client.put(f"/rental_requestId/{id2}", json=updated_data)
    assert response3.status_code == 200  # No debe haber conflicto
    data = response3.json()
    assert data["data"]["modified"] == 1


def test_update_no_conflict_with_rejected():
    """Test que verifica que NO hay conflicto al actualizar con solicitud rechazada"""
    # Crear solicitud rechazada
    rejected_request = {
        "user_id": "user_rejected_update",
        "vehicle_id": "vehicle_rejected_update",
        "start_date": "2026-09-15",
        "end_date": "2026-09-20",
        "status": "rejected"
    }
    response1 = client.post("/rental_request/", json=rejected_request)
    assert response1.status_code == 201
    rejected_id = response1.json()["data"]["inserted_id"]
    created_ids.append(rejected_id)

    # Crear solicitud pendiente para el mismo vehículo
    pending_request = {
        "user_id": "user_pending_update",
        "vehicle_id": "vehicle_rejected_update",  # mismo vehículo
        "start_date": "2026-09-21",
        "end_date": "2026-09-25",
        "status": "pending"
    }
    response2 = client.post("/rental_request/", json=pending_request)
    assert response2.status_code == 201
    pending_id = response2.json()["data"]["inserted_id"]
    created_ids.append(pending_id)

    # Actualizar fechas para que solape con la rechazada (no debe haber conflicto)
    updated_data = {
        "start_date": "2026-09-18",  # Solapa con la rechazada
        "end_date": "2026-09-23"
    }
    response3 = client.put(
        f"/rental_requestId/{pending_id}", json=updated_data)
    assert response3.status_code == 200  # No debe haber conflicto con rejected
    data = response3.json()
    assert data["data"]["modified"] == 1


def test_update_status_to_approved_with_conflict():
    """Test que verifica conflicto al cambiar status a approved cuando hay conflicto de fechas"""
    # Crear solicitud aprobada
    approved_request = {
        "user_id": "user_status_conflict1",
        "vehicle_id": "vehicle_status_conflict",
        "start_date": "2026-10-01",
        "end_date": "2026-10-05",
        "status": "approved"
    }
    response1 = client.post("/rental_request/", json=approved_request)
    assert response1.status_code == 201
    approved_id = response1.json()["data"]["inserted_id"]
    created_ids.append(approved_id)

    # Crear solicitud pendiente que solapa en fechas
    pending_request = {
        "user_id": "user_status_conflict2",
        "vehicle_id": "vehicle_status_conflict",  # mismo vehículo
        "start_date": "2026-10-03",               # fechas que solapan
        "end_date": "2026-10-07",
        "status": "rejected"  # inicialmente rejected para que no haya conflicto al crear
    }
    response2 = client.post("/rental_request/", json=pending_request)
    assert response2.status_code == 201
    pending_id = response2.json()["data"]["inserted_id"]
    created_ids.append(pending_id)

    # Intentar cambiar status a approved (debe generar conflicto)
    updated_data = {
        "status": "approved"
    }
    response3 = client.put(
        f"/rental_requestId/{pending_id}", json=updated_data)
    assert response3.status_code == 400
    data = response3.json()
    assert "Time slot is already taken by an approved or pending request for this vehicle" in data[
        "message"]
    assert data["message_code"] == "TIME_SLOT_TAKEN"
