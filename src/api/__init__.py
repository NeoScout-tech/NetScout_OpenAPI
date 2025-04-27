from fastapi import APIRouter
from src.api.routers import users, devices, connection_codes, reports

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(devices.router)
api_router.include_router(connection_codes.router)
api_router.include_router(reports.router) 