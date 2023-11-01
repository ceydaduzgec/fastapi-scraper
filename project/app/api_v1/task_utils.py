import logging
import os
from datetime import datetime
from zipfile import ZipFile

import requests
from app.api_v1.scraper import get_image_urls
from app.core.exceptions import DownloadTaskNotFoundException, FileNotFoundException
from app.db.crud import get_download_task, update_download_task_fields
from app.db.models import DownloadStatus

logger = logging.getLogger(__name__)


def calculate_progress(downloaded, total):
    if total == 0:
        return 0.0
    progress = (downloaded / total) * 100.0
    return round(progress, 1)


def download_image(image_url, download_folder):  # TODO this can be async
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        if response.status_code == 200:
            filename = os.path.join(download_folder, os.path.basename(image_url))
            with open(filename, "wb") as f:
                f.write(response.content)
    except Exception as e:
        logger.error(f"Failed to download image from {image_url}: {str(e)}")


async def download_images(db, id, download_folder):
    try:
        download_task = get_download_task(db, "id", id)
    except Exception:
        logger.error(f"Download task not found with id {id}")
        raise DownloadTaskNotFoundException("Download task not found")

    update_fields = {"status": DownloadStatus.DOWNLOADING, "started_at": datetime.now()}
    download_task = update_download_task_fields(db, id, update_fields)
    os.makedirs(download_folder, exist_ok=True)

    image_urls = await get_image_urls(download_task.download_url)

    total_images = len(image_urls)
    downloaded_images = 0
    for image_url in image_urls:  # TODO this can be async
        downloaded_images += 1
        progress = calculate_progress(downloaded_images, total_images)
        # print(f"Downloading image {downloaded_images}/{total_images} - {progress}%")
        download_task = update_download_task_fields(db, download_task, {"progress": progress})
        download_image(image_url, download_folder)


async def zip_images(db, id, download_folder):
    download_task = get_download_task(db, "id", id)
    file_paths = [
        os.path.join(folderName, f_name)
        for folderName, _, file_names in os.walk(download_folder)
        for f_name in file_names
    ]
    if not file_paths:
        raise FileNotFoundException("No files found to zip in the {downloads_folder} folder")

    zip_file_path = f"{download_folder}/{download_task.download_id}.zip"

    with ZipFile(zip_file_path, "w") as zipObj:
        for file_path in file_paths:
            zipObj.write(file_path, os.path.basename(file_path))
