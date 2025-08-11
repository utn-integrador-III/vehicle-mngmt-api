import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from db.mongo_client import db  # asumo tienes un cliente mongo ya preparado

load_dotenv()

USER_COLLECTION = os.getenv("USER_COLLECTION")
user_collection = db[USER_COLLECTION]


class UserDBManager:

    @staticmethod
    def get_by_cedula(cedula: str):
        return user_collection.find_one({"cedula": cedula})

    @staticmethod
    def verify_credentials(cedula: str, password: str):
        user = UserDBManager.get_by_cedula(cedula)
        if user and user.get("contraseña") == password:
            return user
        return None

    @staticmethod
    def create(data: dict):
        return user_collection.insert_one(data).inserted_id
