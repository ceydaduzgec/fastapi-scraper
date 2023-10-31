from datetime import datetime
from uuid import UUID

from app.db.models import DownloadStatus
from pydantic import BaseModel, HttpUrl


class DownloadTaskCreate(BaseModel):
    download_url: HttpUrl


class DownloadTaskStatus(BaseModel):
    download_id: UUID
    created_at: datetime
    started_at: datetime
    finished_at: datetime
    status: DownloadStatus
    progress: float
    download_url: HttpUrl

    class Config:
        orm_mode = True


class DownloadTaskResponse(BaseModel):
    download_id: UUID
