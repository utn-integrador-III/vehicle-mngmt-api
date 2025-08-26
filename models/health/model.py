from models.health.db_queries import HealthDBManager
import os
import time
from datetime import datetime


class HealthModel:

    @staticmethod
    def check_api_health():
        """Verifica el estado general de la API"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": "running",
            "version": os.getenv("API_VERSION", "1.0.0"),
            "environment": os.getenv("ENVIRONMENT", "development")
        }

    @staticmethod
    def check_database_health():
        """Verifica el estado de la base de datos"""
        db_connection = HealthDBManager.check_database_connection()
        db_operations = HealthDBManager.check_database_operations()
        db_collections = HealthDBManager.check_collections()
        db_stats = HealthDBManager.get_database_stats()

        overall_status = "healthy"
        if (db_connection.get("status") != "healthy" or
            db_operations.get("status") != "healthy" or
            db_collections.get("status") != "healthy" or
                db_stats.get("status") != "healthy"):
            overall_status = "unhealthy"

        return {
            "status": overall_status,
            "connection": db_connection,
            "operations": db_operations,
            "collections": db_collections,
            "stats": db_stats
        }

    @staticmethod
    def check_environment_variables():
        """Verifica que las variables de entorno críticas estén configuradas"""
        critical_vars = [
            "MONGO_URI",
            "MONGO_DB_NAME",
            "RENTAL_REQUEST_COLLECTION",
            "VEHICLE_COLLECTION"
        ]

        env_status = []
        all_present = True

        for var in critical_vars:
            value = os.getenv(var)
            if value:
                env_status.append({
                    "variable": var,
                    "status": "present",
                    "value_length": len(value)
                })
            else:
                env_status.append({
                    "variable": var,
                    "status": "missing"
                })
                all_present = False

        return {
            "status": "healthy" if all_present else "unhealthy",
            "variables": env_status,
            "total_checked": len(critical_vars),
            "missing_count": len([v for v in env_status if v["status"] == "missing"])
        }

    @staticmethod
    def get_comprehensive_health():
        """Obtiene un reporte completo de salud del sistema"""
        start_time = time.time()

        api_health = HealthModel.check_api_health()
        db_health = HealthModel.check_database_health()
        env_health = HealthModel.check_environment_variables()

        # Determinar estado general
        overall_status = "healthy"
        if (db_health.get("status") != "healthy" or
                env_health.get("status") != "healthy"):
            overall_status = "unhealthy"

        response_time = (time.time() - start_time) * 1000

        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "response_time_ms": round(response_time, 2),
            "components": {
                "api": api_health,
                "database": db_health,
                "environment": env_health
            },
            "summary": {
                "healthy_components": sum([
                    1 if api_health.get("status") == "healthy" else 0,
                    1 if db_health.get("status") == "healthy" else 0,
                    1 if env_health.get("status") == "healthy" else 0
                ]),
                "total_components": 3
            }
        }
