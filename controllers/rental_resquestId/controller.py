# controllers/rental_requestId/controller.py
from fastapi import APIRouter, HTTPException, status
from models.rental_request.model import VehicleModel
from controllers.rental_resquestId.parser import CarUpdateSchema
from utils.server_response import ServerResponse
from utils.message_codes import *

router = APIRouter(prefix="/car", tags=["Vehicles"])

@router.get("/{id}", response_model=dict)
def get_vehicle_by_id(id: str):
    car = VehicleModel.get_by_id(id)
    if not car:
        return ServerResponse.build(message_code=CAR_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
    car["id"] = str(car["_id"])
    car.pop("_id", None)
    return ServerResponse.build(data=car, message="Vehicle found", message_code=SUCCESS_MSG)

@router.put("/{id}", response_model=dict)
def update_vehicle(id: str, car: CarUpdateSchema):
    existing_car = VehicleModel.get_by_id(id)
    if not existing_car:
        return ServerResponse.build(message_code=CAR_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
    try:
        VehicleModel.update(id, car.dict())
        data = car.dict()
        data["id"] = id
        return ServerResponse.build(data=data, message="Updated", message_code=CAR_SUCCESSFULLY_UPDATED)
    except Exception:
        return ServerResponse.build(message_code=INTERNAL_SERVER_ERROR_MSG, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/{id}", response_model=dict)
def delete_vehicle(id: str):
    deleted = VehicleModel.delete(id)
    if not deleted:
        return ServerResponse.build(message_code=CAR_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
    return ServerResponse.build(message="Deleted", message_code=CAR_SUCCESSFULLY_DELETED)
