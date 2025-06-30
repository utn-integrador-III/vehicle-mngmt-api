from db.mongo_client import Connection
from decouple import config

__vehicle_db__ = Connection(config("VEHICLE_COLLECTION"))
