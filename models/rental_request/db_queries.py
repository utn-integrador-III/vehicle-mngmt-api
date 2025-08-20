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
    def is_time_slot_taken(vehicle_id: str, start_date: str, end_date: str, exclude_id: str = None):
        query = {
            "vehicle_id": vehicle_id,
            "status": {"$in": ["approved", "pending"]},
            "$or": [
                {"start_date": {"$lt": end_date}, "end_date": {"$gt": start_date}}
            ]
        }
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}

        return rental_request_collection.find_one(query) is not None
