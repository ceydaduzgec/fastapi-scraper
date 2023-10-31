import datetime
from uuid import UUID, uuid4

from app.api_v1.tasks import download_images_task
from app.db.database import get_db
from app.db.models import DownloadStatus, DownloadTask
from app.db.schemas import DownloadTaskCreate, DownloadTaskResponse, DownloadTaskStatus
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/downloads", response_model=DownloadTaskResponse)
async def post_download_task(
    url: DownloadTaskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
) -> DownloadTaskResponse:
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
    background_tasks.add_task(download_images_task, download_task.id, db)

    return {"download_id": download_id}


@router.get("/downloads/{download_id}/status", response_model=DownloadTaskStatus)
async def get_download_status(download_id: UUID, db: Session = Depends(get_db)) -> DownloadTaskStatus:
    download_task = db.query(DownloadTask).filter(DownloadTask.download_id == str(download_id)).first()
    if not download_task:
        raise HTTPException(status_code=404, detail="Download URL not found")
    return download_task


@router.get("/downloads/{download_id}", response_model=DownloadTaskResponse)
async def get_downloaded_images(download_id: UUID) -> DownloadTaskResponse:
    raise HTTPException(status_code=501, detail="Not implemented")
