from uuid import UUID

from app.api_v1.tasks import download_and_zip_images_task
from app.db.crud import create_download_task
from app.db.database import get_db
from app.db.models import DownloadTask
from app.db.schemas import DownloadTaskCreate, DownloadTaskResponse, DownloadTaskStatus
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/downloads", response_model=DownloadTaskResponse)
async def post_download_task(
    create_request: DownloadTaskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
) -> DownloadTaskResponse:
    """
    Create a new download task with the specified URL.

    Args:
        url (DownloadTaskCreate): The request data containing the download URL.
        background_tasks (BackgroundTasks): A FastAPI background tasks instance.
        db (Session): The SQLAlchemy database session.

    Returns:
        DownloadTaskResponse: The created download task with its unique ID.

    This route allows clients to create a new download task by providing a download URL.
    The task is created in the database, and a background task is scheduled to process the download.
    The response includes the unique download task ID.

    Example usage:
    ```python
    # POST request to create a new download task
    url = {"download_url": "https://example.com"}
    response = post_download_task(url, background_tasks, db)
    ```
    """
    download_task = create_download_task(db, create_request.download_url)
    background_tasks.add_task(download_and_zip_images_task, download_task.id, download_task.download_id, db)
    return download_task


@router.get("/downloads/{download_id}/status", response_model=DownloadTaskStatus)
async def get_download_status(download_id: UUID, db: Session = Depends(get_db)) -> DownloadTaskStatus:
    """
    Retrieve the status of a specific download task by its unique ID.

    Args:
        download_id (UUID): The unique ID of the download task.
        db (Session): The SQLAlchemy database session.

    Returns:
        DownloadTaskStatus: The status of the download task.

    This route allows clients to retrieve the status of a specific download task using its unique ID.
    If the task does not exist, a 404 error is raised.

    Example usage:
    ```python
    # GET request to retrieve the status of a specific download task
    download_id = "your_download_task_id"
    status = get_download_status(download_id, db)
    ```
    """
    download_task = db.query(DownloadTask).filter(DownloadTask.download_id == str(download_id)).first()
    if not download_task:
        raise HTTPException(status_code=404, detail="Download URL not found")
    return download_task


@router.get("/downloads/{download_id}")
async def get_downloaded_images(download_id: UUID):
    """
    Retrieve information about downloaded images for a specific download task.

    Args:
        download_id (UUID): The unique ID of the download task.

    Returns:
        DownloadTaskResponse: Information about downloaded images.

    This route is not implemented and raises a 501 "Not Implemented" error.

    Example usage:
    ```python
    # GET request to retrieve information about downloaded images (not implemented)
    download_id = "your_download_task_id"
    response = get_downloaded_images(download_id)
    ```
    """
    raise HTTPException(status_code=501, detail="Not implemented")
