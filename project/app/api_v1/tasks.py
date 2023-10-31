import logging

from app.api_v1.task_utils import download_images  # zip_images
from app.core.config import settings
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


async def download_and_zip_images_task(id: str, db: Session):
    """
    :param url: URL of the website to scrape
    :param download_id: Unique id for download process
    """
    downloads_folder = f"{settings.DOWNLOAD_PATH}/{id}"
    try:
        await download_images(db, id, downloads_folder)
        # await zip_images(id, db, downloads_folder)
    except Exception as e:
        logger.error(e)
        # update_download_task_fields(db, id, "status": DownloadStatus.ERROR.value})
    else:
        pass
        # update_download_task_fields(id, status=DownloadStatus.FINISHED.value)
