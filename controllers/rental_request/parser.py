# controllers/rental_request/schemas.py
from pydantic import BaseModel, Field
from utils.message_codes import *

class CarCreateSchema(BaseModel):
    plate: str = Field(..., description=CAR_PLATE_REQUIRED)
    brand: str = Field(..., description=CAR_BRAND_REQUIRED)
    year: str = Field(..., description=CAR_YEAR_REQUIRED)
    status: str = Field(..., description=CAR_STATUS_REQUIRED)
