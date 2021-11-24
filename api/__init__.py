from fastapi.routing import APIRouter
from .example import router as example_router
from .image_downloader import router as image_downloader_router


api_router = APIRouter()
api_router.include_router(example_router, prefix='/example')
api_router.include_router(image_downloader_router)
