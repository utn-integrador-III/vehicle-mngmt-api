from models.rental_request.db_queries import __vehicle_db__
from bson import ObjectId

class CarModel:

    @staticmethod
    def get_all():
        return list(__vehicle_db__.get_all_data())

    @staticmethod
    def get_by_id(__vehicle_db__):
        return __vehicle_db__.get_by_id(__vehicle_db__id)

    @staticmethod
    def create(data):
        return __vehicle_db__.create_data(data)

    @staticmethod
    def update(__vehicle_db__, data):
        return __vehicle_db__.update_data(__vehicle_db___id, data)

    @staticmethod
    def delete(__vehicle_db__):
        return __vehicle_db__.delete_data(__vehicle_db__)
