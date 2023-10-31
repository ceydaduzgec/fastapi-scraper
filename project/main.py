from app.api import api_router
from fastapi import FastAPI

app = FastAPI(title="FastAPI Image Scraper")

app.include_router(api_router)
