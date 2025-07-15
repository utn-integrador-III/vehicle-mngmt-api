import time
from dotenv import load_dotenv
from db.mongo_client import client, db

load_dotenv()


class HealthDBManager:

    @staticmethod
    def check_database_connection():
        """Verifica la conexión a la base de datos MongoDB"""
        try:
            start_time = time.time()
            # Ping a la base de datos
            db.command('ping')
            response_time = (time.time() - start_time) * \
                1000  # en milisegundos

            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "database_name": db.name,
                "connection": "active"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "connection": "failed"
            }

    @staticmethod
    def check_collections():
        """Verifica que las colecciones principales existan y sean accesibles"""
        try:
            collections_info = []
            collection_names = db.list_collection_names()

            for collection_name in collection_names:
                try:
                    collection = db[collection_name]
                    doc_count = collection.count_documents({})
                    collections_info.append({
                        "name": collection_name,
                        "status": "healthy",
                        "document_count": doc_count
                    })
                except Exception as e:
                    collections_info.append({
                        "name": collection_name,
                        "status": "unhealthy",
                        "error": str(e)
                    })

            return {
                "status": "healthy",
                "collections": collections_info,
                "total_collections": len(collection_names)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "collections": []
            }

    @staticmethod
    def check_database_operations():
        """Verifica operaciones básicas de CRUD en la base de datos"""
        try:
            # Crear una colección temporal para testing
            test_collection = db['health_check_test']

            # Test CREATE
            test_doc = {"test": True, "timestamp": time.time()}
            insert_result = test_collection.insert_one(test_doc)

            # Test READ
            retrieved_doc = test_collection.find_one(
                {"_id": insert_result.inserted_id})

            # Test UPDATE
            update_result = test_collection.update_one(
                {"_id": insert_result.inserted_id},
                {"$set": {"updated": True}}
            )

            # Test DELETE
            delete_result = test_collection.delete_one(
                {"_id": insert_result.inserted_id})

            # Limpiar colección de test
            test_collection.drop()

            return {
                "status": "healthy",
                "operations": {
                    "create": "success",
                    "read": "success",
                    "update": "success",
                    "delete": "success"
                }
            }
        except Exception as e:
            # Intentar limpiar en caso de error
            try:
                db['health_check_test'].drop()
            except:
                pass

            return {
                "status": "unhealthy",
                "error": str(e),
                "operations": {
                    "create": "failed",
                    "read": "failed",
                    "update": "failed",
                    "delete": "failed"
                }
            }

    @staticmethod
    def get_database_stats():
        """Obtiene estadísticas generales de la base de datos"""
        try:
            stats = db.command("dbStats")
            return {
                "status": "healthy",
                "stats": {
                    "collections": stats.get("collections", 0),
                    "objects": stats.get("objects", 0),
                    "data_size": stats.get("dataSize", 0),
                    "storage_size": stats.get("storageSize", 0),
                    "indexes": stats.get("indexes", 0)
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
