from models.login.db_quieries import UserDBManager

class UserModel:

    @staticmethod
    def login(cedula: str, password: str):
        return UserDBManager.verify_credentials(cedula, password)

    @staticmethod
    def get_by_cedula(cedula: str):
        return UserDBManager.get_by_cedula(cedula)

    @staticmethod
    def create(data: dict):
        return UserDBManager.create(data)
