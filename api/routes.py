from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

router = APIRouter()


class DownloadRequest(BaseModel):
    url: HttpUrl


class DownloadResponse(BaseModel):
    download_id: UUID


@router.post("/downloads", response_model=DownloadResponse)
async def start_downloading_images(url: DownloadRequest) -> dict:
    download_id = uuid4()
    if download_id:
        return {"download_id": download_id}
    else:
        return {"message": "Download ID not found"}, 404


@router.get("/downloads/{download_id}/status")
async def get_download_status(download_id: UUID) -> dict:
    download_id = uuid4()
    if download_id:
        return {
            "download_id": download_id,
            "started_at": datetime.now(),
            "finished_at": datetime.now(),
            "status": "PENDING",
            "download_url": f"http://localhost:5000/downloads/{download_id}",
        }
    else:
        return {"message": "Download ID not found"}, 404


@router.get("/downloads/{download_id}")
async def download_images():
    return {"message": "Not implemented yet"}, 501
