from fastapi import APIRouter, HTTPException, status
from typing import List
from models.vehicle.model import VehicleModel
from controllers.vehicle.parser import CarCreateSchema
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
import base64
from datetime import datetime
router = APIRouter(prefix="/car", tags=["Vehicles"])

@router.get("/", response_model=dict)
async def get_vehicles():
    try:
        vehicles = VehicleModel.get_all()  # Método que devuelve lista de dicts

        processed_vehicles = []
        for vehicle in vehicles:
            vehicle_dict = dict(vehicle)
            if "_id" in vehicle_dict:
                vehicle_dict["id"] = str(vehicle_dict["_id"])
                del vehicle_dict["_id"]
            for key, value in vehicle_dict.items():
                if isinstance(value, bytes):
                    vehicle_dict[key] = base64.b64encode(value).decode("utf-8")
                elif isinstance(value, datetime):
                    vehicle_dict[key] = value.isoformat()
            processed_vehicles.append(vehicle_dict)

        return ServerResponse.build(
            data=processed_vehicles,
            message="Vehicles found",
            message_code=SUCCESS_MSG,
            code="SUCCESS"  # explícito, aunque es default
        )

    except Exception as e:
        print("ERROR in get_vehicles:", e)
        return ServerResponse.build(
            message="Internal server error",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_vehicle(car: CarCreateSchema):
    try:
        data = car.model_dump()
        result = VehicleModel.create(data)
        
        # Ojo: Si `create` retorna el documento creado, debes convertir ObjectId a str
        # Si no, solo tomamos inserted_id para poner en el id:
        
        # Limpiar campos con ObjectId si existiesen, ejemplo:
        if "_id" in data:
            del data["_id"]
        
        data["id"] = str(result.inserted_id)
        
        return ServerResponse.build(
            data=data,
            message="Car created",
            message_code=CAR_SUCCESSFULLY_CREATED,
            status=status.HTTP_201_CREATED,
            code="SUCCESS"
        )
    except Exception as e:
        print("ERROR in create_vehicle:", e)
        return ServerResponse.build(
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )
