import uuid
from enum import Enum as PyEnum

from app.db.database import Base
from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.sql import func


class DownloadStatus(PyEnum):
    PENDING = "PENDING"
    DOWNLOADING = "DOWNLOADING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class DownloadTask(Base):
    __tablename__ = "download_tasks"

    id = Column(Integer, primary_key=True, index=True)
    download_id = Column(String, default=str(uuid.uuid4()), unique=True, nullable=False, index=True)
    download_url = Column(String, index=True, nullable=False)
    status = Column(Enum(DownloadStatus), default=DownloadStatus.PENDING, index=True)
    progress = Column(Float, default=0.0, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
