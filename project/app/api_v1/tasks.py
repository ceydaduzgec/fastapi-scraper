import logging
from datetime import datetime

from app.api_v1.task_utils import download_images, zip_images
from app.core.config import settings
from app.db.crud import update_download_task_fields
from app.db.models import DownloadStatus
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


async def download_and_zip_images_task(id: str, db: Session) -> None:
    """
    :param url: URL of the website to scrape
    :param download_id: Unique id for download process
    """

    unique_download_folder = f"{settings.DOWNLOAD_PATH}/{id}/"
    try:
        await download_images(db, id, unique_download_folder)
        await zip_images(db, id, unique_download_folder)
    except Exception as e:
        logger.error(e)
        update_fields = {"status": DownloadStatus.ERROR, "finished_at": datetime.now()}

        update_download_task_fields(db, id, update_fields)
    else:
        update_fields = {"status": DownloadStatus.FINISHED, "finished_at": datetime.now()}
        update_download_task_fields(db, id, update_fields)
