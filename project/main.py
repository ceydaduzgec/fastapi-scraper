import time

from app.api_v1.api import api_router
from fastapi import FastAPI, Request

app = FastAPI(title="FastAPI Image Scraper")

app.include_router(api_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
