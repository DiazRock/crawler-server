import uuid
from pydantic import BaseModel, Field, HttpUrl, AfterValidator
from typing import List, Annotated
from datetime import datetime
from bson import ObjectId

HttpUrlString = Annotated[HttpUrl, AfterValidator(lambda v: str(v))]
class ScreenshotDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    start_url: HttpUrlString
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
