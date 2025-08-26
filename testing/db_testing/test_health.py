import pytest
from fastapi.testclient import TestClient
from app import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


def test_basic_health_check():
    """Test del endpoint básico de health check"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "message" in data
    assert "code" in data
    assert data["code"] == "SUCCESS"
    assert data["data"]["status"] == "healthy"
    assert "timestamp" in data["data"]
    assert "uptime" in data["data"]


def test_ping_endpoint():
    """Test del endpoint de ping"""
    response = client.get("/health/ping")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["ping"] == "pong"
    assert "timestamp" in data["data"]
    assert data["message"] == "Pong"
    assert data["code"] == "SUCCESS"


def test_comprehensive_health_check_healthy():
    """Test del health check comprensivo cuando todo está saludable"""
    with patch('models.health.model.HealthModel.get_comprehensive_health') as mock_health:
        mock_health.return_value = {
            "status": "healthy",
            "timestamp": "2025-07-25T10:00:00",
            "response_time_ms": 150.5,
            "components": {
                "api": {"status": "healthy"},
                "database": {"status": "healthy"},
                "environment": {"status": "healthy"}
            },
            "summary": {
                "healthy_components": 3,
                "total_components": 3
            }
        }

        response = client.get("/health/comprehensive")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "SUCCESS"
        assert data["data"]["status"] == "healthy"
        assert "components" in data["data"]
        assert "summary" in data["data"]


def test_comprehensive_health_check_unhealthy():
    """Test del health check comprensivo cuando hay problemas"""
    with patch('models.health.model.HealthModel.get_comprehensive_health') as mock_health:
        mock_health.return_value = {
            "status": "unhealthy",
            "timestamp": "2025-07-25T10:00:00",
            "response_time_ms": 250.0,
            "components": {
                "api": {"status": "healthy"},
                "database": {"status": "unhealthy"},
                "environment": {"status": "healthy"}
            },
            "summary": {
                "healthy_components": 2,
                "total_components": 3
            }
        }

        response = client.get("/health/comprehensive")
        assert response.status_code == 503  # TIMEOUT
        data = response.json()
        assert data["code"] == "SYSTEM_UNHEALTHY"
        assert data["data"]["status"] == "unhealthy"


def test_database_health_check_healthy():
    """Test del health check de base de datos cuando está saludable"""
    with patch('models.health.model.HealthModel.check_database_health') as mock_db_health:
        mock_db_health.return_value = {
            "status": "healthy",
            "connection": {
                "status": "healthy",
                "response_time_ms": 25.5,
                "database_name": "test_db",
                "connection": "active"
            },
            "operations": {
                "status": "healthy",
                "operations": {
                    "create": "success",
                    "read": "success",
                    "update": "success",
                    "delete": "success"
                }
            },
            "collections": {
                "status": "healthy",
                "collections": [],
                "total_collections": 0
            },
            "stats": {
                "status": "healthy",
                "stats": {
                    "collections": 5,
                    "objects": 100,
                    "data_size": 1024,
                    "storage_size": 2048,
                    "indexes": 10
                }
            }
        }

        response = client.get("/health/database")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "SUCCESS"
        assert data["data"]["status"] == "healthy"
        assert "connection" in data["data"]
        assert "operations" in data["data"]
        assert "collections" in data["data"]
        assert "stats" in data["data"]


def test_database_health_check_unhealthy():
    """Test del health check de base de datos cuando hay problemas"""
    with patch('models.health.model.HealthModel.check_database_health') as mock_db_health:
        mock_db_health.return_value = {
            "status": "unhealthy",
            "connection": {
                "status": "unhealthy",
                "error": "Connection failed",
                "connection": "failed"
            },
            "operations": {
                "status": "unhealthy",
                "error": "Cannot perform operations"
            },
            "collections": {
                "status": "unhealthy",
                "error": "Cannot access collections"
            },
            "stats": {
                "status": "unhealthy",
                "error": "Cannot get stats"
            }
        }

        response = client.get("/health/database")
        assert response.status_code == 503  # TIMEOUT
        data = response.json()
        assert data["code"] == "DATABASE_UNHEALTHY"
        assert data["data"]["status"] == "unhealthy"


def test_environment_health_check_healthy():
    """Test del health check de variables de entorno cuando están correctas"""
    with patch('models.health.model.HealthModel.check_environment_variables') as mock_env_health:
        mock_env_health.return_value = {
            "status": "healthy",
            "variables": [
                {"variable": "MONGO_URI", "status": "present", "value_length": 50},
                {"variable": "MONGO_DB_NAME", "status": "present", "value_length": 10},
                {"variable": "RENTAL_REQUEST_COLLECTION",
                    "status": "present", "value_length": 15},
                {"variable": "VEHICLE_COLLECTION",
                    "status": "present", "value_length": 12}
            ],
            "total_checked": 4,
            "missing_count": 0
        }

        response = client.get("/health/environment")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "SUCCESS"
        assert data["data"]["status"] == "healthy"
        assert data["data"]["missing_count"] == 0
        assert len(data["data"]["variables"]) == 4


def test_environment_health_check_unhealthy():
    """Test del health check de variables de entorno cuando faltan algunas"""
    with patch('models.health.model.HealthModel.check_environment_variables') as mock_env_health:
        mock_env_health.return_value = {
            "status": "unhealthy",
            "variables": [
                {"variable": "MONGO_URI", "status": "missing"},
                {"variable": "MONGO_DB_NAME", "status": "present", "value_length": 10},
                {"variable": "RENTAL_REQUEST_COLLECTION", "status": "missing"},
                {"variable": "VEHICLE_COLLECTION",
                    "status": "present", "value_length": 12}
            ],
            "total_checked": 4,
            "missing_count": 2
        }

        response = client.get("/health/environment")
        assert response.status_code == 503  # TIMEOUT
        data = response.json()
        assert data["code"] == "ENVIRONMENT_UNHEALTHY"
        assert data["data"]["status"] == "unhealthy"
        assert data["data"]["missing_count"] == 2


def test_basic_health_check_exception():
    """Test del manejo de excepciones en el health check básico"""
    with patch('models.health.model.HealthModel.check_api_health') as mock_api_health:
        mock_api_health.side_effect = Exception("Test exception")

        response = client.get("/health/")
        assert response.status_code == 500
        data = response.json()
        assert data["code"] == "INTERNAL_SERVER_ERROR"
        assert "Health check failed" in data["message"]


def test_comprehensive_health_check_exception():
    """Test del manejo de excepciones en el health check comprensivo"""
    with patch('models.health.model.HealthModel.get_comprehensive_health') as mock_health:
        mock_health.side_effect = Exception("Test exception")

        response = client.get("/health/comprehensive")
        assert response.status_code == 500
        data = response.json()
        assert data["code"] == "INTERNAL_SERVER_ERROR"
        assert "Comprehensive health check failed" in data["message"]


def test_database_health_check_exception():
    """Test del manejo de excepciones en el health check de base de datos"""
    with patch('models.health.model.HealthModel.check_database_health') as mock_db_health:
        mock_db_health.side_effect = Exception("Database test exception")

        response = client.get("/health/database")
        assert response.status_code == 500
        data = response.json()
        assert data["code"] == "INTERNAL_SERVER_ERROR"
        assert "Database health check failed" in data["message"]


def test_environment_health_check_exception():
    """Test del manejo de excepciones en el health check de entorno"""
    with patch('models.health.model.HealthModel.check_environment_variables') as mock_env_health:
        mock_env_health.side_effect = Exception("Environment test exception")

        response = client.get("/health/environment")
        assert response.status_code == 500
        data = response.json()
        assert data["code"] == "INTERNAL_SERVER_ERROR"
        assert "Environment health check failed" in data["message"]


def test_ping_exception():
    """Test del manejo de excepciones en el endpoint de ping"""
    with patch('models.health.model.HealthModel.check_api_health') as mock_api_health:
        mock_api_health.side_effect = Exception("Ping test exception")

        response = client.get("/health/ping")
        assert response.status_code == 500
        data = response.json()
        assert data["code"] == "INTERNAL_SERVER_ERROR"
        assert "Ping failed" in data["message"]

# Tests de integración más específicos


def test_health_response_structure():
    """Verifica que todos los endpoints de health tengan la estructura de respuesta correcta"""
    endpoints = ["/health/", "/health/ping", "/health/comprehensive",
                 "/health/database", "/health/environment"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        data = response.json()

        # Estructura básica de ServerResponse
        assert "data" in data or "message" in data
        assert "message" in data
        assert "message_code" in data
        assert "code" in data


def test_health_endpoints_return_json():
    """Verifica que todos los endpoints devuelvan JSON válido"""
    endpoints = ["/health/", "/health/ping", "/health/comprehensive",
                 "/health/database", "/health/environment"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.headers["content-type"] == "application/json"
        # Si llega aquí sin excepción, el JSON es válido
        data = response.json()
        assert isinstance(data, dict)
