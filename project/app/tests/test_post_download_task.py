import unittest

from app.db.database import SessionLocal
from app.db.models import DownloadTask
from app.db.schemas import DownloadTaskCreate
from fastapi.testclient import TestClient
from main import app


class TestDownloadRoute(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_post_download_task(self):
        download_url = "https://example.com"
        data = DownloadTaskCreate(download_url=download_url)
        response = self.client.post("/downloads", json=data.dict())
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("download_id", response_data)
        download_id = response_data["download_id"]
        download_task = self.db.query(DownloadTask).filter(DownloadTask.download_id == download_id).first()
        self.assertIsNotNone(download_task)
        self.assertEqual(download_task.download_url, download_url)


if __name__ == "__main__":
    unittest.main()
