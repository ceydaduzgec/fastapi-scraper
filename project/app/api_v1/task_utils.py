import logging
import os
from datetime import datetime

import requests
from app.api_v1.scraper import get_image_urls
from app.db.crud import update_download_task_fields
from app.db.models import DownloadStatus, DownloadTask

logger = logging.getLogger(__name__)


def download_image(image_url, download_folder):  # TODO this can be async
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        if response.status_code == 200:
            filename = os.path.join(download_folder, os.path.basename(image_url))  # TODO update for production
            with open(filename, "wb") as f:
                f.write(response.content)
    except Exception as e:
        logger.error(f"Failed to download image from {image_url}: {str(e)}")


def calculate_progress(downloaded, total):
    if total == 0:
        return 0.0
    progress = (downloaded / total) * 100.0
    return round(progress, 1)


async def download_images(db, id, downloads_folder):
    download_task = db.query(DownloadTask).filter(DownloadTask.id == id).first()
    if not download_task:
        raise Exception("Download task not found")

    update_fields = {"status": DownloadStatus.DOWNLOADING, "started_at": datetime.now()}
    download_task = update_download_task_fields(db, id, update_fields)
    os.makedirs(downloads_folder, exist_ok=True)  # TODO update for production

    image_urls = await get_image_urls(download_task.download_url)

    total_images = len(image_urls)
    downloaded_images = 0
    for image_url in image_urls:  # TODO this can be async
        downloaded_images += 1
        progress = calculate_progress(downloaded_images, total_images)
        # print(f"Downloading image {downloaded_images}/{total_images} - {progress}%")
        download_task = update_download_task_fields(db, download_task, {"progress": progress})
        download_image(image_url, downloads_folder)

    update_fields = {"status": DownloadStatus.FINISHED, "finished_at": datetime.now(), "progress": 100.0}
    download_task = update_download_task_fields(db, download_task, update_fields)


async def zip_images(downloads_folder):
    pass
