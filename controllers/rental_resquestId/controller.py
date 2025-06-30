from fastapi import APIRouter, UploadFile, File, Form
from models.rental_request.car_model import CarModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
import shutil, os

router = APIRouter()

@router.get("/car/{car_id}")
def get_car(car_id: str):
    car = CarModel.get_by_id(car_id)
    if not car:
        return ServerResponse("Car not found", CAR_NOT_FOUND, StatusCode.NOT_FOUND)
    car["id"] = str(car["_id"])
    car.pop("_id", None)
    return ServerResponse("Car retrieved successfully", CAR_RETRIEVED, StatusCode.OK, car)

@router.put("/car/{car_id}")
def update_car(
    car_id: str,
    plate: str = Form(...),
    brand: str = Form(...),
    year: str = Form(...),
    status: str = Form(...),
    picture: UploadFile = File(None)
):
    car = CarModel.get_by_id(car_id)
    if not car:
        return ServerResponse("Car not found", CAR_NOT_FOUND, StatusCode.NOT_FOUND)

    update_data = {
        "plate": plate,
        "brand": brand,
        "year": year,
        "status": status
    }

    if picture:
        path = f"static/pictures/{car_id}_{picture.filename}"
        with open(path, "wb") as f:
            shutil.copyfileobj(picture.file, f)
        update_data["picture"] = path

    CarModel.update(car_id, update_data)
    update_data["id"] = car_id
    return ServerResponse("Car updated successfully", CAR_UPDATED, StatusCode.OK, update_data)

@router.delete("/car/{car_id}")
def delete_car(car_id: str):
    result = CarModel.delete(car_id)
    if not result:
        return ServerResponse("Car not found", CAR_NOT_FOUND, StatusCode.NOT_FOUND)
    return ServerResponse("Car deleted successfully", CAR_DELETED, StatusCode.OK)
