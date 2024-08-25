import logging
from functools import lru_cache
from typing import Generator
from pymongo import MongoClient
from pymongo.database import Database
from pathlib import Path
import os
from repositories.screenshot_repository import ScreenshotRepository
from services.crawler import Crawler

BASE_DIR = Path(os.getenv("SCREENSHOT_FOLDER"))
BASE_DIR.mkdir(exist_ok=True)



def get_db_session()-> Generator[Database, None, None]:
    client = MongoClient("mongodb://mongo:27017")
    while True:
        db = client['screenshots_db']    
        yield db


@lru_cache(maxsize=None)
def get_logger():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


def get_screenshot_repository():
    db: Database = next(get_db_session())
    return ScreenshotRepository(db)


def get_crawler_service():
    repository: ScreenshotRepository = get_screenshot_repository()
    return Crawler(
        repository,
        BASE_DIR,
        get_logger()
    )
