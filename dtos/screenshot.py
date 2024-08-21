from pydantic import BaseModel, Field
from typing import List

class ScreenshotRequest(BaseModel):
    start_url: str = Field(..., example="https://www.example.com", description="The starting URL for the web crawling process.")
    number_of_links_to_follow: int = Field(..., example=5, description="The number of links to follow and capture screenshots of after the initial page.")


class ScreenshotResponse(BaseModel):
    run_id: str = Field(..., example="abc123")
    screenshots: List[str] = Field(..., example=["abc123_screenshot_0.png", "abc123_screenshot_1.png"])