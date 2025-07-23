from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv

# Import routers from controllers

from controllers.vehicle.controller import router as vehicle_router
from controllers.vehicleId.controller import router as vehicle_id_router
from controllers.rental_request.controller import router as rental_request_router
from controllers.rental_requestId.controller import router as rental_request_id_router

# Import utilities
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import *
from db.mongo_client import client

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="Vehicle Management API",
    description="API for managing vehicles and rental requests",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Root endpoint


@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return ServerResponse.build(
        data={
            "name": "Vehicle Management API",
            "version": "1.0.0",
            "description": "API for managing vehicles and rental requests"
        },
        message="Welcome to Vehicle Management API",
        message_code=OK_MSG
    )

# Include routers from controllers
app.include_router(vehicle_router)
app.include_router(vehicle_id_router)
app.include_router(rental_request_router)
app.include_router(rental_request_id_router)


# Run the application
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "false").lower() == "true"

    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
