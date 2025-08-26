from models.vehicle.db_queries import VehicleDBManager

class VehicleModel:

    @staticmethod
    def get_all():
        return VehicleDBManager.get_all()

    @staticmethod
    def get_by_id(id: str):
        return VehicleDBManager.get_by_id(id)

    @staticmethod
    def create(data: dict):
        return VehicleDBManager.create(data)

    @staticmethod
    def update(id: str, data: dict):
        return VehicleDBManager.update(id, data)

    @staticmethod
    def delete(id: str):
        return VehicleDBManager.delete(id)
