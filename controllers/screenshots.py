from fastapi import APIRouter, BackgroundTasks, HTTPException
from models.screenshot import ScreenshotRequest
import uuid
from pathlib import Path
from pymongo import MongoClient
import os

router = APIRouter()

mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(mongo_url)
db = client["screenshot_db"]
collection = db["screenshots"]

BASE_DIR = Path("/screenshots")
BASE_DIR.mkdir(exist_ok=True)

def take_screenshots(start_url: str, number_of_links: int, run_id: str):
    screenshots = [f"{run_id}_screenshot_{i}.png" for i in range(number_of_links + 1)]
    for screenshot in screenshots:
        screenshot_path = BASE_DIR / screenshot
        with open(screenshot_path, "w") as f:
            f.write("This is a dummy screenshot file.")
    
    collection.insert_one({"_id": run_id, "screenshots": screenshots})

@router.post("/screenshots")
def start_screenshot_process(request: ScreenshotRequest, background_tasks: BackgroundTasks):
    run_id = str(uuid.uuid4())
    background_tasks.add_task(take_screenshots, request.start_url, request.number_of_links_to_follow, run_id)
    return {"run_id": run_id}

@router.get("/screenshots/{id}")
def get_screenshots(id: str):
    record = collection.find_one({"_id": id})
    if not record:
        raise HTTPException(status_code=404, detail="Screenshots not found for the provided ID")
    
    screenshots = record["screenshots"]
    screenshots_data = [{"filename": screenshot, "url": f"/static/screenshots/{screenshot}"} for screenshot in screenshots]
    return {"screenshots": screenshots_data}
