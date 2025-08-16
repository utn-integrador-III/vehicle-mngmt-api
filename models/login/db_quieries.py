import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from db.mongo_client import db

load_dotenv()

USER_COLLECTION = os.getenv("USER_COLLECTION")
user_collection = db[USER_COLLECTION]


class UserDBManager:
    @staticmethod
    def get_all():
        return list(user_collection.find())
    
    @staticmethod
    def get_by_cedula(cedula: str):
        return user_collection.find_one({"cedula": cedula})

    @staticmethod
    def get_by_id(user_id: str):
        try:
            return user_collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    @staticmethod
    def verify_credentials(cedula: str, password: str):
        user = UserDBManager.get_by_cedula(cedula)
        if user and user.get("contraseña") == password:
            return user
        return None

    @staticmethod
    def create(data: dict):
        return user_collection.insert_one(data).inserted_id

    @staticmethod
    def update_by_id(user_id: str, update_data: dict):
        try:
            result = user_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception:
            return False

    @staticmethod
    def delete_by_id(user_id: str):
        try:
            result = user_collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception:
            return False
