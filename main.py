from fastapi import FastAPI

from api import api_router

app = FastAPI(title="FastAPI Image Scraper")

app.include_router(api_router)
