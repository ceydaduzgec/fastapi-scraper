from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import DownloadStatus, DownloadTask
from app.db.schemas import DownloadTaskCreate, DownloadTaskResponse, DownloadTaskStatus
from app.db.session import get_db

router = APIRouter()


@router.post("/downloads", response_model=DownloadTaskResponse)
async def start_downloading_images(url: DownloadTaskCreate, db: Session = Depends(get_db)):
    download_id = uuid4()
    download_task = DownloadTask(download_id=str(download_id), url=url.url, status=DownloadStatus.PENDING)
    db.add(download_task)
    db.commit()
    db.refresh(download_task)
    return {"download_id": download_id}


@router.get("/downloads/{download_id}/status", response_model=DownloadTaskStatus)
async def get_download_status(download_id: UUID, db: Session = Depends(get_db)):
    download_task = db.query(DownloadTask).filter(DownloadTask.download_id == str(download_id)).first()
    if not download_task:
        raise HTTPException(status_code=404, detail="Download URL not found")

    started_at = download_task.started_at
    finished_at = download_task.finished_at
    status = download_task.status
    download_url = download_task.url

    return {
        "download_id": download_id,
        "started_at": started_at,
        "finished_at": finished_at,
        "status": status,
        "download_url": download_url,
    }


@router.get("/downloads/{download_id}", response_model=DownloadTaskResponse)
async def download_images():
    return {"message": "Not implemented yet"}, 501
