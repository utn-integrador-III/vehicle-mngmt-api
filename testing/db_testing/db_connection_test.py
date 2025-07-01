from db.mongo_client import client
from pymongo.errors import ConnectionFailure

try:
    client.admin.command('ping')
    print("✅ Conexión exitosa a MongoDB Atlas")
except ConnectionFailure:
    print("❌ No se pudo conectar a MongoDB Atlas")
