import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from db.mongo_client import db

load_dotenv()

RENTAL_REQUEST_COLLECTION = os.getenv("RENTAL_REQUEST_COLLECTION")
rental_request_collection = db[RENTAL_REQUEST_COLLECTION]


class RentalRequestDBManager:

    @staticmethod
    def get_all():
        return list(rental_request_collection.find({}))

    @staticmethod
    def get_by_id(id: str):
        try:
            return rental_request_collection.find_one({"_id": ObjectId(id)})
        except Exception:
            return None

    @staticmethod
    def get_by_any(identifier: str):
        """
        Busca por _id, id interno de la boleta o applicant.
        Retorna una lista de resultados.
        """
        results = []

        # Intentamos buscar por _id de MongoDB
        try:
            doc = rental_request_collection.find_one({"_id": ObjectId(identifier)})
            if doc:
                results.append(doc)
        except Exception:
            pass

        # Buscamos por id interno de la boleta
        docs_by_internal_id = list(rental_request_collection.find({"id": identifier}))
        results.extend(docs_by_internal_id)

        # Buscamos por applicant (nombre), búsqueda insensible a mayúsculas
        docs_by_applicant = list(rental_request_collection.find({"applicant": {"$regex": identifier, "$options": "i"}}))
        results.extend(docs_by_applicant)

        # Eliminamos duplicados por _id
        unique_results = {str(doc["_id"]): doc for doc in results}
        return list(unique_results.values())

    @staticmethod
    def create(data: dict):
        return rental_request_collection.insert_one(data)

    @staticmethod
    def update(id: str, data: dict):
        return rental_request_collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    @staticmethod
    def delete(id: str):
        result = rental_request_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    @staticmethod
    def is_time_slot_taken(vehicle_plate: str, start_date: str, exclude_id: str = None):
        query = {
            "plate": vehicle_plate,
            "start_date": start_date,
            "status": {"$in": ["approved", "pending"]}
        }
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}

        return rental_request_collection.find_one(query) is not None
