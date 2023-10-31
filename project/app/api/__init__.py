from app.api.routers import router as image_downloader_router
from fastapi.routing import APIRouter

api_router = APIRouter()
api_router.include_router(image_downloader_router)
