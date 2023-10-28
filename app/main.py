from fastapi import FastAPI

from app.api import api_router

app = FastAPI(title="FastAPI Image Scraper")

app.include_router(api_router)
