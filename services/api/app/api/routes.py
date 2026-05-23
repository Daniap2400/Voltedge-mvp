from fastapi import APIRouter

from app.api.v1.analytics import router as analytics_router
from app.api.v1.charging import router as charging_router
from app.api.v1.health import router as health_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router, tags=["health"])
api_router.include_router(charging_router, tags=["charging"])
api_router.include_router(analytics_router, tags=["analytics"])