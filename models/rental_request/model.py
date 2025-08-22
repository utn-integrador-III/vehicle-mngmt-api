from models.rental_request.db_queries import RentalRequestDBManager


class RentalRequestModel:

    @staticmethod
    def get_all():
        results = RentalRequestDBManager.get_all()
        return [{**doc, "_id": str(doc["_id"])} for doc in results]

    @staticmethod
    def get_by_id(id: str):
        doc = RentalRequestDBManager.get_by_id(id)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @staticmethod
    def get_by_any(identifier: str):
        docs = RentalRequestDBManager.get_by_any(identifier)
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return docs

    @staticmethod
    def create(data: dict):
        if data.get("status") in ["approved", "pending"]:
            if RentalRequestDBManager.is_time_slot_taken(
                vehicle_plate=data["plate"],
                start_date=data["start_date"]
            ):
                raise ValueError(
                    "Time slot is already taken by an approved or pending request for this vehicle."
                )

        return RentalRequestDBManager.create(data)

    @staticmethod
    def update(id: str, data: dict):
        current_data = RentalRequestDBManager.get_by_id(id)
        if not current_data:
            raise ValueError("Rental request not found")

        vehicle_plate = data.get("plate", current_data.get("plate"))
        start_date = data.get("start_date", current_data.get("start_date"))
        final_status = data.get("status", current_data.get("status"))

        should_validate = (
            "start_date" in data or
            final_status in ["approved", "pending"]
        )

        if should_validate:
            if RentalRequestDBManager.is_time_slot_taken(
                vehicle_plate=vehicle_plate,
                start_date=start_date,
                exclude_id=id
            ):
                raise ValueError(
                    "Time slot is already taken by an approved or pending request for this vehicle."
                )

        return RentalRequestDBManager.update(id, data)

    @staticmethod
    def delete(id: str):
        return RentalRequestDBManager.delete(id)
