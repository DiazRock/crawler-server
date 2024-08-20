from pydantic import BaseModel


class ScreenshotRequest(BaseModel):
    start_url: str
    number_of_links_to_follow: int