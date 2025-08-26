from fastapi import APIRouter, Request
from models.rental_request.model import RentalRequestModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import OK_MSG, CREATED_MSG, INTERNAL_SERVER_ERROR_MSG
from controllers.rental_request.parser import RentalRequestParser

router = APIRouter(prefix="/rental_request", tags=["Rental Requests"])


@router.get("/")
async def get_all_rental_requests():
    data = RentalRequestModel.get_all()
    return ServerResponse.build(data=data, message_code=OK_MSG)


@router.post("/")
async def create_rental_request(request: Request):
    payload = await request.json()
    parsed_data = RentalRequestParser.parse_create(payload)

    try:
        insert_result = RentalRequestModel.create(parsed_data)
        if insert_result.inserted_id:
            return ServerResponse.build(
                data={"inserted_id": str(insert_result.inserted_id)},
                message_code=CREATED_MSG,
                code=CREATED_MSG,
                status=StatusCode.CREATED
            )
    except ValueError as e:
        return ServerResponse.build(
            message=str(e),
            message_code="TIME_SLOT_TAKEN",
            status=StatusCode.BAD_REQUEST
        )

    return ServerResponse.build(
        message="Creation failed",
        message_code=INTERNAL_SERVER_ERROR_MSG,
        status=StatusCode.INTERNAL_SERVER_ERROR
    )
