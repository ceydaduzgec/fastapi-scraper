import datetime
from uuid import UUID, uuid4

from app.db.database import get_db
from app.db.models import DownloadStatus, DownloadTask
from app.db.schemas import DownloadTaskCreate, DownloadTaskResponse, DownloadTaskStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/downloads", response_model=DownloadTaskResponse)
async def start_downloading_images(url: DownloadTaskCreate, db: Session = Depends(get_db)):
    download_id = uuid4()
    download_task = DownloadTask(
        download_id=str(download_id),
        download_url=url.download_url,
        status=DownloadStatus.PENDING,
        started_at=datetime.datetime.min,
        finished_at=datetime.datetime.min,
    )
    db.add(download_task)
    db.commit()
    db.refresh(download_task)
    # start_download_task(download_task)
    return {"download_id": download_id}


@router.get("/downloads/{download_id}/status", response_model=DownloadTaskStatus)
async def get_download_status(download_id: UUID, db: Session = Depends(get_db)):
    download_task = db.query(DownloadTask).filter(DownloadTask.download_id == str(download_id)).first()
    if not download_task:
        raise HTTPException(status_code=404, detail="Download URL not found")
    return download_task


@router.get("/downloads/{download_id}", response_model=DownloadTaskResponse)
async def download_images():
    return {"message": "Not implemented yet"}, 501
