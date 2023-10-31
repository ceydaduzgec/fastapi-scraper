import uuid
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class DownloadStatus(PyEnum):
    PENDING = "PENDING"
    DOWNLOADING = "DOWNLOADING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class DownloadTask(Base):
    __tablename__ = "download_tasks"

    id = Column(Integer, primary_key=True, index=True)
    download_id = Column(String, default=str(uuid.uuid4()), unique=True, nullable=False, index=True)
    url = Column(String, index=True, nullable=False)
    status = Column(Enum(DownloadStatus), default=DownloadStatus.PENDING, index=True)
    progress = Column(Float, default=0.0, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))

    images = relationship("Image", back_populates="task")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)
    download_task_id = Column(Integer, ForeignKey("download_tasks.id"), index=True)
    task = relationship("DownloadTask", back_populates="images")  # Add this line
