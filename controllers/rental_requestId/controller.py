from fastapi import APIRouter, Request
from models.rental_request.model import RentalRequestModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import OK_MSG, NOT_FOUND_MSG
from controllers.rental_requestId.parser import RentalRequestIdParser

router = APIRouter(prefix="/rental_requestId", tags=["Rental Requests By ID"])


@router.get("/{rental_request_id}")
async def get_rental_request_by_id(rental_request_id: str):
    result = RentalRequestModel.get_by_id(rental_request_id)
    if result:
        return ServerResponse.build(data=result, message_code=OK_MSG)
    return ServerResponse.build(
        message="Rental request not found",
        message_code=NOT_FOUND_MSG,
        status=StatusCode.NOT_FOUND,
        code=NOT_FOUND_MSG
    )


@router.put("/{rental_request_id}")
async def update_rental_request(rental_request_id: str, request: Request):
    payload = await request.json()
    parsed_data = RentalRequestIdParser.parse_update(payload)

    try:
        update_result = RentalRequestModel.update(
            rental_request_id, parsed_data)
        if update_result.modified_count > 0:
            return ServerResponse.build(
                data={"modified": update_result.modified_count},
                message_code=OK_MSG
            )
    except ValueError as e:
        return ServerResponse.build(
            message=str(e),
            message_code="TIME_SLOT_TAKEN",
            status=StatusCode.BAD_REQUEST
        )

    return ServerResponse.build(
        message="Rental request not found",
        message_code=NOT_FOUND_MSG,
        status=StatusCode.NOT_FOUND,
        code=NOT_FOUND_MSG
    )


@router.delete("/{rental_request_id}")
async def delete_rental_request(rental_request_id: str):
    deleted = RentalRequestModel.delete(rental_request_id)
    if deleted:
        return ServerResponse.build(
            data={"deleted": True},
            message_code=OK_MSG
        )
    return ServerResponse.build(
        message="Rental request not found",
        message_code=NOT_FOUND_MSG,
        status=StatusCode.NOT_FOUND,
        code=NOT_FOUND_MSG
    )
