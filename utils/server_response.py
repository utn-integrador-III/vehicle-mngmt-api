from fastapi.responses import JSONResponse

class StatusCode:
    OK = 200
    NOT_FOUND = 404
    INTERNAL_ERROR = 500
    BAD_REQUEST = 400

def ServerResponse(data=None, message="", message_code="", status=200):
    return JSONResponse(
        status_code=status,
        content={
            "data": data,
            "message": message,
            "code": message_code
        }
    )
