from fastapi import APIRouter, HTTPException, status
from typing import List
from models.rental_request.model import VehicleModel
from controllers.rental_request.parser import CarCreateSchema, CarUpdateSchema
from utils.server_response import ServerResponse
from utils.message_codes import *

router = APIRouter(prefix="/car", tags=["Vehicles"])

@router.get("/", response_model=dict)
def get_vehicles():
    try:
        vehicles = VehicleModel.get_all()
        # Convertir _id a str y remover _id
        for car in vehicles:
            car["id"] = str(car["_id"])
            car.pop("_id", None)
        return ServerResponse.build(data=vehicles, message="Vehicles found", message_code=SUCCESS_MSG)
    except Exception:
        return ServerResponse.build(message_code=INTERNAL_SERVER_ERROR_MSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_vehicle(car: CarCreateSchema):
    try:
        data = car.dict()
        result = VehicleModel.create(data)
        data["id"] = str(result.inserted_id)
        return ServerResponse.build(data=data, message="Car created", message_code=CAR_SUCCESSFULLY_CREATED, status=status.HTTP_201_CREATED)
    except Exception:
        return ServerResponse.build(message_code=INTERNAL_SERVER_ERROR_MSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
