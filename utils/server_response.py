from fastapi.responses import JSONResponse
from utils.message_codes import *  # importa los códigos que usas


class StatusCode:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
    TIMEOUT = 503


class ServerResponse:
    @staticmethod
    def build(data=None, message=None, message_code=None, status=StatusCode.OK, code="SUCCESS"):
        if not message:
            message, message_code = ServerResponse.__get_default_msg(status)

        body = {
            "code": code,             # Ahora sí usamos el parámetro `code`
            "data": data,
            "message": message,
            "message_code": message_code,
        }
        return JSONResponse(content=body, status_code=status)

    @staticmethod
    def __get_default_msg(status):
        if status == StatusCode.OK:
            return "Successfully requested", OK_MSG
        elif status == StatusCode.CREATED:
            return "Successfully created", CREATED_MSG
        elif status == StatusCode.NOT_FOUND:
            return "Record not found", NOT_FOUND_MSG
        elif status == StatusCode.CONFLICT:
            return "Conflict error with the request", CONFLICT_MSG
        elif status == StatusCode.UNPROCESSABLE_ENTITY:
            return "Unprocessable entity", UNPROCESSABLE_ENTITY_MSG
        elif status == StatusCode.INTERNAL_SERVER_ERROR:
            return "Internal server error", INTERNAL_SERVER_ERROR_MSG
        elif status == StatusCode.TIMEOUT:
            return "Server timeout", SERVER_TIMEOUT_MSG
        else:
            return "Unknown status", "UNKNOWN"
