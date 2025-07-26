from fastapi import APIRouter, HTTPException, status
from models.health.model import HealthModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *

router = APIRouter(prefix="/health", tags=["Health Check"])


@router.get("/", response_model=dict)
async def basic_health_check():
    """Endpoint básico de health check"""
    try:
        health_data = HealthModel.check_api_health()

        return ServerResponse.build(
            data=health_data,
            message="API is healthy",
            message_code=SUCCESS_MSG,
            code="SUCCESS"
        )
    except Exception as e:
        print("ERROR in basic_health_check:", e)
        return ServerResponse.build(
            message="Health check failed",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )


@router.get("/comprehensive", response_model=dict)
async def comprehensive_health_check():
    """Endpoint completo de health check que verifica todos los componentes"""
    try:
        health_data = HealthModel.get_comprehensive_health()

        # Determinar el status code basado en el estado general
        response_status = StatusCode.OK if health_data["status"] == "healthy" else StatusCode.TIMEOUT

        return ServerResponse.build(
            data=health_data,
            message=f"System is {health_data['status']}",
            message_code=SUCCESS_MSG if health_data["status"] == "healthy" else "SYSTEM_UNHEALTHY",
            status=response_status,
            code="SUCCESS" if health_data["status"] == "healthy" else "SYSTEM_UNHEALTHY"
        )
    except Exception as e:
        print("ERROR in comprehensive_health_check:", e)
        return ServerResponse.build(
            message="Comprehensive health check failed",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )


@router.get("/database", response_model=dict)
async def database_health_check():
    """Endpoint específico para verificar el estado de la base de datos"""
    try:
        db_health = HealthModel.check_database_health()

        response_status = StatusCode.OK if db_health["status"] == "healthy" else StatusCode.TIMEOUT

        return ServerResponse.build(
            data=db_health,
            message=f"Database is {db_health['status']}",
            message_code=SUCCESS_MSG if db_health["status"] == "healthy" else "DATABASE_UNHEALTHY",
            status=response_status,
            code="SUCCESS" if db_health["status"] == "healthy" else "DATABASE_UNHEALTHY"
        )
    except Exception as e:
        print("ERROR in database_health_check:", e)
        return ServerResponse.build(
            message="Database health check failed",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )


@router.get("/environment", response_model=dict)
async def environment_health_check():
    """Endpoint para verificar las variables de entorno"""
    try:
        env_health = HealthModel.check_environment_variables()

        response_status = StatusCode.OK if env_health["status"] == "healthy" else StatusCode.TIMEOUT

        return ServerResponse.build(
            data=env_health,
            message=f"Environment variables are {env_health['status']}",
            message_code=SUCCESS_MSG if env_health["status"] == "healthy" else "ENVIRONMENT_UNHEALTHY",
            status=response_status,
            code="SUCCESS" if env_health["status"] == "healthy" else "ENVIRONMENT_UNHEALTHY"
        )
    except Exception as e:
        print("ERROR in environment_health_check:", e)
        return ServerResponse.build(
            message="Environment health check failed",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )


@router.get("/ping", response_model=dict)
async def ping():
    """Endpoint simple de ping para verificación básica de conectividad"""
    try:
        return ServerResponse.build(
            data={"ping": "pong", "timestamp": HealthModel.check_api_health()[
                "timestamp"]},
            message="Pong",
            message_code=SUCCESS_MSG,
            code="SUCCESS"
        )
    except Exception as e:
        print("ERROR in ping:", e)
        return ServerResponse.build(
            message="Ping failed",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )
