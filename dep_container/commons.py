import logging
from functools import lru_cache
from services.crawler import Crawler


def get_crawler_service():
    return Crawler()

@lru_cache(maxsize=None)
def get_logger():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


