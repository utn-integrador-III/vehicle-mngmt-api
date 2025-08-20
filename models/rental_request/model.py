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
        # Solo validar conflictos si el status es 'approved' o 'pending'
        if data.get("status") in ["approved", "pending"]:
            if RentalRequestDBManager.is_time_slot_taken(
                vehicle_id=data["vehicle_id"],
                start_date=data["start_date"],
                end_date=data["end_date"]
            ):
                raise ValueError(
                    "Time slot is already taken by an approved or pending request for this vehicle.")

        return RentalRequestDBManager.create(data)

    @staticmethod
    def update(id: str, data: dict):
        # PRIMERO verificar si el rental request existe
        current_data = RentalRequestDBManager.get_by_id(id)
        if not current_data:
            raise ValueError("Rental request not found")

        # Usar el vehicle_id de los datos actuales si no se está actualizando
        vehicle_id = data.get("vehicle_id", current_data.get("vehicle_id"))
        start_date = data.get("start_date", current_data.get("start_date"))
        end_date = data.get("end_date", current_data.get("end_date"))

        # Determinar el status final después de la actualización
        final_status = data.get("status", current_data.get("status"))

        # Solo validar conflictos si:
        # 1. Se están actualizando fechas, O
        # 2. El status final será 'approved' o 'pending'
        should_validate = (
            "start_date" in data or
            "end_date" in data or
            final_status in ["approved", "pending"]
        )

        if should_validate:
            # Validar si hay conflicto de horario con otra solicitud aprobada o pendiente para el mismo vehículo
            # (excluyendo esta misma solicitud)
            if RentalRequestDBManager.is_time_slot_taken(
                vehicle_id=vehicle_id,
                start_date=start_date,
                end_date=end_date,
                exclude_id=id
            ):
                raise ValueError(
                    "Time slot is already taken by an approved or pending request for this vehicle.")

        return RentalRequestDBManager.update(id, data)

    @staticmethod
    def delete(id: str):
        return RentalRequestDBManager.delete(id)
