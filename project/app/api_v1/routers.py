from uuid import UUID

from app.api_v1.tasks import download_and_zip_images_task
from app.api_v1.utils import get_zip_file
from app.core.exceptions import DownloadTaskNotFoundException
from app.db.crud import create_download_task, get_download_task
from app.db.database import get_db
from app.db.schemas import (
    DownloadTaskCreate,
    DownloadTaskResponse,
    DownloadTaskStatus,
    NotFoundResponse,
)
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/downloads", response_model=DownloadTaskResponse)
async def post_download_task(
    create_request: DownloadTaskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """
    Create a new download task by providing the download URL. Get the first ["MAX_IMAGE_NUMBER"] images from the page and download them as a zip file.

    Args:
        download_url (HttpUrl): The URL of the page that wanted to images downloaded from. It should be a valid URL for the content you want to download.

    Returns:
        download_id: UUID of the newly created download task.
    """
    download_task = create_download_task(db, create_request.download_url)
    background_tasks.add_task(download_and_zip_images_task, download_task.download_id, db)
    return download_task


@router.get(
    "/downloads/{download_id}/status", response_model=DownloadTaskStatus, responses={404: {"model": NotFoundResponse}}
)
async def get_download_status(download_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve the status of a specific download task by its unique ID.

    Args:
        download_id (UUID): The unique ID of the download task.

    Returns:
        DownloadTaskStatus: The status of the download task.

    This route allows clients to retrieve the status of a specific download task using its unique ID.
    If the task does not exist, a 404 error is raised.
    ```
    """
    try:
        download_task = get_download_task(db, "download_id", str(download_id))
        return download_task
    except DownloadTaskNotFoundException:
        return JSONResponse(status_code=404, content={"message": "Download task not found"})
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"message": "Download task exists but file not found"})


@router.get("/downloads/{download_id}", response_class=FileResponse, responses={404: {"model": NotFoundResponse}})
async def get_downloaded_images_zip(download_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve the zip file that contains the images for a specific download task.

    Args:
        download_id (UUID): The unique ID of the download task.

    Returns:
        FileResponse: Zip file of the downloaded images.
    """
    try:
        file_zip = get_zip_file(db, download_id)
        return file_zip
    except DownloadTaskNotFoundException:
        return JSONResponse(status_code=404, content={"message": "Download task not found"})
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"message": "Download task exists but file not found"})
