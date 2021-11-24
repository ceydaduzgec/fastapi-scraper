from fastapi import FastAPI

from api import api_router

app = FastAPI(title='Mindsite Backend Developer Assignment')

app.include_router(api_router)
