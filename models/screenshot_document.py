from pydantic import BaseModel, Field, HttpUrl
from typing import List
from datetime import datetime
from bson import ObjectId

class ScreenshotDocument(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    start_url: HttpUrl
    screenshots: List[str]
    timestamp: datetime

    class Config:
        # Automatically use alias (like _id) when generating the model
        allow_population_by_field_name = True
        # Ensure that the model can interact with MongoDB ObjectId
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }
