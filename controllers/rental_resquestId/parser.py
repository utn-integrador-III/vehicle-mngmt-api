from flask_restful import reqparse

def car_parser_update():
    parser = reqparse.RequestParser()
    parser.add_argument("_id", type=str, required=True, help="ID is required")
    parser.add_argument("plate", type=str, required=True, help="Plate is required")
    parser.add_argument("brand", type=str, required=True, help="Brand is required")
    parser.add_argument("year", type=str, required=True, help="Year is required")
    parser.add_argument("status", type=str, required=True, help="Status is required")
    return parser
