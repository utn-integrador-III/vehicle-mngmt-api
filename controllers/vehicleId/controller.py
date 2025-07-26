from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi import status as fastapi_status
from typing import Optional
from models.vehicle.model import VehicleModel
from controllers.vehicleId.parser import CarUpdateSchema
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
import base64
from datetime import datetime

router = APIRouter(prefix="/car", tags=["Vehicles"])


@router.get("/{id}", response_model=dict)
def get_vehicle_by_id(id: str):
    try:
        car = VehicleModel.get_by_id(id)
        if not car:
            return ServerResponse.build(
                message="Car not found",
                message_code=CAR_NOT_FOUND,
                status=StatusCode.NOT_FOUND,
                code="CAR_NOT_FOUND"
            )

        # Procesar los datos del vehículo
        car_dict = dict(car)
        car_dict["id"] = str(car_dict["_id"])
        car_dict.pop("_id", None)

        # Convertir bytes a base64 si es necesario
        for key, value in car_dict.items():
            if isinstance(value, bytes):
                car_dict[key] = base64.b64encode(value).decode("utf-8")
            elif isinstance(value, datetime):
                car_dict[key] = value.isoformat()

        return ServerResponse.build(
            data=car_dict,
            message="Vehicle found",
            message_code=SUCCESS_MSG,
            code="SUCCESS"
        )
    except Exception as e:
        print("ERROR in get_vehicle_by_id:", e)
        return ServerResponse.build(
            message="Internal server error",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )


@router.put("/{id}", response_model=dict)
async def update_vehicle(
    id: str,
    plate: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    type: Optional[str] = Form(None),
    brand: Optional[str] = Form(None),
    year: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None)
):
    try:
        existing_car = VehicleModel.get_by_id(id)
        if not existing_car:
            return ServerResponse.build(
                message="Car not found",
                message_code=CAR_NOT_FOUND,
                status=StatusCode.NOT_FOUND,
                code="CAR_NOT_FOUND"
            )

        # Construir el objeto de actualización con solo los campos proporcionados
        update_data = {}

        if plate is not None:
            update_data["plate"] = plate
        if model is not None:
            update_data["model"] = model
        if type is not None:
            update_data["type"] = type
        if brand is not None:
            update_data["brand"] = brand
        if year is not None:
            update_data["year"] = year
        if status is not None:
            update_data["status"] = status

        # Procesar la foto si se proporciona
        if photo is not None:
            photo_bytes = await photo.read()
            update_data["photo"] = base64.b64encode(
                photo_bytes).decode("utf-8")

        if not update_data:
            return ServerResponse.build(
                message="No data provided for update",
                message_code=INTERNAL_SERVER_ERROR_MSG,
                status=StatusCode.BAD_REQUEST,
                code="BAD_REQUEST"
            )

        VehicleModel.update(id, update_data)

        # Preparar los datos de respuesta
        response_data = update_data.copy()
        response_data["id"] = id

        return ServerResponse.build(
            data=response_data,
            message="Updated",
            message_code=CAR_SUCCESSFULLY_UPDATED,
            code="CAR_SUCCESSFULLY_UPDATED"
        )
    except Exception as e:
        print("ERROR in update_vehicle:", e)
        return ServerResponse.build(
            message="Internal server error",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )


@router.delete("/{id}", response_model=dict)
def delete_vehicle(id: str):
    try:
        deleted = VehicleModel.delete(id)
        if not deleted:
            return ServerResponse.build(
                message="Car not found",
                message_code=CAR_NOT_FOUND,
                status=StatusCode.NOT_FOUND,
                code="CAR_NOT_FOUND"
            )
        return ServerResponse.build(
            message="Deleted",
            message_code=CAR_SUCCESSFULLY_DELETED,
            code="CAR_SUCCESSFULLY_DELETED"
        )
    except Exception as e:
        print("ERROR in delete_vehicle:", e)
        return ServerResponse.build(
            message="Internal server error",
            message_code=INTERNAL_SERVER_ERROR_MSG,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR"
        )
