from fastapi import APIRouter

from app.api.routes import sensors

api_router = APIRouter()
api_router.include_router(sensors.router, prefix="/api")
