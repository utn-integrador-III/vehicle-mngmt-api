from flask_restful import Resource
from controllers.rental_resquestId.parser import car_parser_update
from models.rental_request.model import VehicleModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *

class VehicleByIdController(Resource):
    route = '/car/<string:id>'

    def get(self, id):
        car = VehicleModel.get_by_id(id)
        if not car:
            return ServerResponse.build(message_code=CAR_NOT_FOUND, status=StatusCode.NOT_FOUND)
        car["id"] = str(car["_id"])
        car.pop("_id", None)
        return ServerResponse.build(data=car, message="Vehicle found", message_code=CAR_SUCCESSFULLY_CREATED)

    def put(self, id):
        parser = car_parser_update()
        data = parser.parse_args()

        car = VehicleModel.get_by_id(id)
        if not car:
            return ServerResponse.build(message_code=CAR_NOT_FOUND, status=StatusCode.NOT_FOUND)

        try:
            VehicleModel.update(id, data)
            data["id"] = id
            return ServerResponse.build(data=data, message="Updated", message_code=CAR_SUCCESSFULLY_UPDATED)
        except:
            return ServerResponse.build(message_code=INTERNAL_SERVER_ERROR_MSG, status=StatusCode.INTERNAL_SERVER_ERROR)

    def delete(self, id):
        deleted = VehicleModel.delete(id)
        if not deleted:
            return ServerResponse.build(message_code=CAR_NOT_FOUND, status=StatusCode.NOT_FOUND)
        return ServerResponse.build(message="Deleted", message_code=CAR_SUCCESSFULLY_DELETED)
