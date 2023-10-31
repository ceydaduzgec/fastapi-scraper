from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class DownloadTaskCreate(BaseModel):
    url: HttpUrl


class DownloadTaskStatus(BaseModel):
    download_id: str
    started_at: datetime
    finished_at: datetime
    status: float
    download_url: HttpUrl


class DownloadTaskResponse(BaseModel):
    download_id: UUID
