from flask_restful import Resource
from controllers.rental_request.parser import car_parser_create
from models.rental_request.model import VehicleModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *

class VehicleListController(Resource):
    route = '/car'

    def get(self):
        try:
            vehicles = VehicleModel.get_all()
            for car in vehicles:
                car["id"] = str(car["_id"])
                car.pop("_id", None)
            return ServerResponse.build(data=vehicles, message="Vehicles found", message_code=SUCCESS_MSG)
        except:
            return ServerResponse.build(message_code=INTERNAL_SERVER_ERROR_MSG, status=StatusCode.INTERNAL_SERVER_ERROR)

    def post(self):
        parser = car_parser_create()
        data = parser.parse_args()
        try:
            result = VehicleModel.create(data)
            data["id"] = str(result.inserted_id)
            return ServerResponse.build(data=data, message="Car created", message_code=CAR_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except:
            return ServerResponse.build(message_code=INTERNAL_SERVER_ERROR_MSG, status=StatusCode.INTERNAL_SERVER_ERROR)
