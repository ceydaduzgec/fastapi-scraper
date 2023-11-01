from uuid import UUID

from app.core.config import settings
from app.core.exceptions import FileNotFoundException
from app.db.crud import get_download_task
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session


def get_zip_file(db: Session, download_id: UUID):
    try:
        download_task = get_download_task(db, "download_id", str(download_id))
        file_path = f"{settings.DOWNLOAD_PATH}/{download_task.id}/{download_id}.zip"
        return FileResponse(file_path)
    except Exception:
        raise FileNotFoundException("No files found to zip in the {downloads_folder} folder")
