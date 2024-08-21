import logging
from functools import lru_cache
from typing import Generator
from repositories.screenshot_repository import ScreenshotRepository
from services.crawler import Crawler
from pymongo import MongoClient
from pymongo.database import Database
from pathlib import Path
from fastapi import Depends


BASE_DIR = Path("screenshots")
BASE_DIR.mkdir(exist_ok=True)


@lru_cache(maxsize=None)
def get_db_session()-> Generator[Database]:
    client = MongoClient("mongodb://localhost:27017")
    db = client['screenshots_db']
    try:
        yield db
    finally:
        client.close()


@lru_cache(maxsize=None)
def get_logger():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


def get_screenshot_repository(db: MongoClient = Depends(get_db_session)):
    return ScreenshotRepository(db)


def get_crawler_service(repository = Depends(get_screenshot_repository)):
    return Crawler(
        repository,
        BASE_DIR
    )
