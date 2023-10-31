from app.api_v1.routers import router as image_downloader_router
from app.core.config import settings
from fastapi.routing import APIRouter

api_router = APIRouter()
api_router.include_router(image_downloader_router, prefix=settings.API_V1_STR)
