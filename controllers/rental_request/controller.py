from fastapi import APIRouter
from models.rental_request.car_model import CarModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *

router = APIRouter()

@router.get("/car")
def get_all_cars():
    try:
        cars = CarModel.get_all()
        for car in cars:
            car["id"] = str(car["_id"])
            car.pop("_id", None)
        return ServerResponse("Cars retrieved successfully", CARS_RETRIEVED, StatusCode.OK, cars)
    except Exception:
        return ServerResponse("Internal server error", INTERNAL_ERROR, StatusCode.INTERNAL_ERROR)
