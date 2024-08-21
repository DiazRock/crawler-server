from fastapi import APIRouter, Depends, HTTPException
from dtos.screenshot import ScreenshotRequest
import uuid
from dep_container import get_crawler_service
from services.crawler import Crawler

router = APIRouter()

@router.post("/screenshots")
async def start_screenshot_process(request: ScreenshotRequest, crawler_service: Crawler = Depends(get_crawler_service)):
    run_id = str(uuid.uuid4())
    
    screenshots = await crawler_service.crawl_website(request.start_url, request.number_of_links_to_follow, run_id)
    
    return {"run_id": run_id, "screenshots": screenshots}

@router.get("/screenshots/{id}")
def get_screenshots(id: str, crawler_service: Crawler = Depends(get_crawler_service)):

    record = crawler_service.find_one({"_id": id})
    if not record:
        raise HTTPException(status_code=404, detail="Screenshots not found for the provided ID")
    
    screenshots = record["screenshots"]
    screenshots_data = [{"filename": screenshot, "url": f"/static/screenshots/{screenshot}"} for screenshot in screenshots]
    return {"screenshots": screenshots_data}
