from typing import List
from datetime import datetime
from pymongo.database import Database

from models.screenshot_document import ScreenshotDocument

class ScreenshotRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection = self.db['screenshots']

    async def insert_screenshot_data(self, run_id: str, start_url: str, screenshots: List[str]):
        screenshot_doc = ScreenshotDocument(
            id=run_id,
            start_url=start_url,
            screenshots=screenshots,
            timestamp=datetime.now()
        )

        # Insert the document into MongoDB
        await self.collection.insert_one(screenshot_doc.model_dump(by_alias=True))        

    async def get_screenshots_by_run_id(self, run_id: str):
        return await self.collection.find_one({"_id": run_id})
