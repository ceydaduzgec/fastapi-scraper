import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Image Scraper"
    PROJECT_VERSION: str = "0.1"

    POSTGRES_USER: str = os.getenv("DB_USER", "dev_user")
    POSTGRES_PASSWORD = os.getenv("DB_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("DB_NAME", "db")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}",
    )
    DB_ECHO_LOG: bool = True if os.environ.get("DEBUG") == "True" else False
    DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloads")
    API_V1_STR = os.getenv("API_V1_STR", "/v1")


settings = Settings()
