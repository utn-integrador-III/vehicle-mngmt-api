class RentalRequestIdParser:

    @staticmethod
    def parse_update(data: dict) -> dict:
        # Validamos solo los campos permitidos
        allowed_fields = ["start_date", "end_date", "status"]
        return {key: data[key] for key in allowed_fields if key in data}
