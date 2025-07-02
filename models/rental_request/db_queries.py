# models/rental_request/db_queries.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
VEHICLE_COLLECTION = os.getenv("VEHICLE_COLLECTION")

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]
vehicle_collection = db[VEHICLE_COLLECTION]

class VehicleDBManager:

    @staticmethod
    def get_all():
        return list(vehicle_collection.find({}))

    @staticmethod
    def get_by_id(id: str):
        try:
            return vehicle_collection.find_one({"_id": ObjectId(id)})
        except Exception:
            return None

    @staticmethod
    def create(data: dict):
        return vehicle_collection.insert_one(data)

    @staticmethod
    def update(id: str, data: dict):
        return vehicle_collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    @staticmethod
    def delete(id: str):
        result = vehicle_collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
