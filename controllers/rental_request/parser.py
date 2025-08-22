class RentalRequestParser:

    @staticmethod
    def parse_create(data: dict) -> dict:
        return {
            "applicant": data.get("applicant"),
            "direccion": data.get("direccion"),
            "necesidad": data.get("necesidad"),
            "start_date": data.get("start_date"),
            "end_date": None,
            "estimate": data.get("estimate"),
            "companions": data.get("companions", []),
            "date": {
                "day": data.get("day"),
                "month": data.get("month"),
                "year": data.get("year")
            },
            "plate": data.get("plate"),
            "model": data.get("model"),
            "status": data.get("status", "pending")
        }
