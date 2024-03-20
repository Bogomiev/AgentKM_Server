from fastapi import APIRouter

from src.api.v1.auth import router as auth_routers

api_router = APIRouter()

api_router.include_router(auth_routers)
