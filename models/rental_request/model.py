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
        # Validar si hay conflicto de horario con otra solicitud aprobada
        if RentalRequestDBManager.is_time_slot_taken(data["start_date"], data["end_date"]):
            raise ValueError(
                "Time slot is already taken by an approved request.")

        return RentalRequestDBManager.create(data)

    @staticmethod
    def update(id: str, data: dict):
        # Validar si hay conflicto de horario con otra solicitud aprobada (excluyendo esta misma)
        if RentalRequestDBManager.is_time_slot_taken(data["start_date"], data["end_date"], exclude_id=id):
            raise ValueError(
                "Time slot is already taken by an approved request.")

        return RentalRequestDBManager.update(id, data)

    @staticmethod
    def delete(id: str):
        return RentalRequestDBManager.delete(id)
