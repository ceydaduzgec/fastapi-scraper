import datetime
from uuid import uuid4

from app.core.exceptions import DownloadTaskNotFoundException
from app.db.models import DownloadStatus, DownloadTask
from sqlalchemy.orm import Session


def create_download_task(db: Session, download_url: str) -> DownloadTask:
    """
    Create a new download task in the database.

    Args:
        db (Session): The SQLAlchemy database session.
        download_url (str): The URL to download content from.

    Returns:
        DownloadTaskResponse: The created download task.

    The function creates a new download task in the database with the provided
    download URL and sets its initial status to PENDING. It records the
    starting and finishing times as `datetime.datetime.min`, and then returns
    the created download task.
    """
    download_task = DownloadTask(
        download_id=str(uuid4()),
        download_url=download_url,
        status=DownloadStatus.PENDING,
        started_at=datetime.datetime.min,
        finished_at=datetime.datetime.min,
    )
    db.add(download_task)
    db.commit()
    db.refresh(download_task)

    return download_task


def get_download_task(db: Session, filter_field, filter_value) -> DownloadTask:
    download_task = db.query(DownloadTask).filter(getattr(DownloadTask, filter_field) == filter_value).first()
    if not download_task:
        raise DownloadTaskNotFoundException(f"No record found with {filter_field} = {filter_value}")
    return download_task


def update_download_task_fields(db: Session, download_task_or_id, update_fields: dict) -> DownloadTask:
    """
    Update the specified fields of an SQLAlchemy model instance.

    Args:
        db (Session): The SQLAlchemy database session.
        download_task_or_id (Union[DownloadTask, int]): The DownloadTask instance or its id.
        update_fields (dict): A dictionary of field-value pairs to update.

    Returns:
        instance: The updated model instance.

    Raises:
        ValueError: If no record is found with the given id.
    """

    if isinstance(download_task_or_id, int):
        # If id is provided, query the database to get the DownloadTask instance
        download_task = get_download_task(db, "id", download_task_or_id)
    else:
        # If a DownloadTask instance is provided, use it directly
        download_task = download_task_or_id

    for field, value in update_fields.items():
        setattr(download_task, field, value)

    db.commit()
    db.refresh(download_task)

    return download_task
