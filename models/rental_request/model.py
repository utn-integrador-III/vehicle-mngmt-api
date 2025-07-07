from models.rental_request.db_queries import RentalRequestDBManager

class RentalRequestModel:

    @staticmethod
    def get_all():
        return RentalRequestDBManager.get_all()

    @staticmethod
    def get_by_id(id: str):
        return RentalRequestDBManager.get_by_id(id)

    @staticmethod
    def create(data: dict):
        return RentalRequestDBManager.create(data)

    @staticmethod
    def update(id: str, data: dict):
        return RentalRequestDBManager.update(id, data)

    @staticmethod
    def delete(id: str):
        return RentalRequestDBManager.delete(id)
