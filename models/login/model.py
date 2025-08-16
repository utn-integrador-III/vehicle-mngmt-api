from models.login.db_quieries import UserDBManager

class UserModel:

    @staticmethod
    def get_all():
        return UserDBManager.get_all()

    @staticmethod
    def login(cedula: str, password: str):
        return UserDBManager.verify_credentials(cedula, password)

    @staticmethod
    def get_by_cedula(cedula: str):
        return UserDBManager.get_by_cedula(cedula)

    @staticmethod
    def get_by_id(user_id: str):
        return UserDBManager.get_by_id(user_id)

    @staticmethod
    def create(data: dict):
        return UserDBManager.create(data)

    @staticmethod
    def update_by_id(user_id: str, update_data: dict):
        return UserDBManager.update_by_id(user_id, update_data)

    @staticmethod
    def delete_by_id(user_id: str):
        return UserDBManager.delete_by_id(user_id)

