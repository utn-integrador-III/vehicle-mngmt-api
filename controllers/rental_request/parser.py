class RentalRequestParser:

    @staticmethod
    def parse_create(data: dict) -> dict:
        # Aquí puedes agregar validaciones o limpieza de campos si quieres
        return {
            "user_id": data.get("user_id"),
            "vehicle_id": data.get("vehicle_id"),
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "status": data.get("status", "pending"),
        }
