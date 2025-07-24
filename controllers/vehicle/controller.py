from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi import status as fastapi_status
from typing import List
from models.vehicle.model import VehicleModel
from controllers.vehicle.parser import CarCreateSchema
from utils.server_response import StatusCode, ServerResponse
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

@router.post("/", response_model=dict, status_code=fastapi_status.HTTP_201_CREATED)
async def create_vehicle(
    plate: str = Form(...),
    model: str = Form(...),
    type: str = Form(...),
    brand: str = Form(...),
    year: str = Form(...),
    status: str = Form(...),
    photo: UploadFile = File(...)
):
    try:
        photo_bytes = await photo.read()
        
        data = {
            "plate": plate,
            "model": model,
            "type": type,
            "brand": brand,
            "year": year,
            "status": status,
            "photo": base64.b64encode(photo_bytes).decode("utf-8")
        }
        
        result = VehicleModel.create(data)

        data["id"] = str(result.inserted_id)

        if "_id" in data:
            del data["_id"]

        return ServerResponse.build(
            data=data,
            message="Car created",
            message_code=CAR_SUCCESSFULLY_CREATED,
            status=fastapi_status.HTTP_201_CREATED,
            code="SUCCESS"
        )

    except Exception as e:
        print("ERROR in create_vehicle:", e)
        return ServerResponse.build(
            message="Internal server error",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )
