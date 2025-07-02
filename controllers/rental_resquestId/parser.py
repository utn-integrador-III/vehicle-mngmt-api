from flask_restful import reqparse
from utils.message_codes import *

def car_parser_update():
    parser = reqparse.RequestParser()
    parser.add_argument("plate", type=str, required=True, help=CAR_PLATE_REQUIRED)
    parser.add_argument("brand", type=str, required=True, help=CAR_BRAND_REQUIRED)
    parser.add_argument("year", type=str, required=True, help=CAR_YEAR_REQUIRED)
    parser.add_argument("status", type=str, required=True, help=CAR_STATUS_REQUIRED)
    return parser
