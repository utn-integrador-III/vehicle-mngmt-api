from models.rental_request.db_queries import RentalRequestDBManager

class RentalRequestModel:

    @staticmethod
    def get_all():
        results = RentalRequestDBManager.get_all()
        # Convertir ObjectId a str en cada documento
        return [{**doc, "_id": str(doc["_id"])} for doc in results]

    @staticmethod
    def get_by_id(id: str):
        doc = RentalRequestDBManager.get_by_id(id)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @staticmethod
    def create(data: dict):
        return RentalRequestDBManager.create(data)

    @staticmethod
    def update(id: str, data: dict):
        return RentalRequestDBManager.update(id, data)

    @staticmethod
    def delete(id: str):
        return RentalRequestDBManager.delete(id)
