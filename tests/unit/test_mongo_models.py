import pytest
from datetime import datetime
from pydantic import ValidationError
from bson import ObjectId
from models.screenshot_document import ScreenshotDocument

def test_screenshot_document_default_id():
    # Arrange
    start_url = "https://example.com/"
    screenshots = ["screenshot1.png", "screenshot2.png"]
    timestamp = datetime.now()

    # Act
    document = ScreenshotDocument(start_url=start_url, screenshots=screenshots, timestamp=timestamp)

    # Assert
    assert isinstance(document.id, str)
    assert len(document.id) == 36  # UUID length
    assert document.start_url == start_url
    assert document.screenshots == screenshots
    assert document.timestamp == timestamp


def test_screenshot_document_url_validation():
    # Arrange
    valid_url = "https://example.com/"
    invalid_url = "not_a_url"
    screenshots = ["screenshot1.png"]
    timestamp = datetime.now()

    # Act & Assert
    document = ScreenshotDocument(start_url=valid_url, screenshots=screenshots, timestamp=timestamp)
    assert document.start_url == valid_url  # Ensure the URL is stored as a string

    # Assert invalid URL raises ValidationError
    with pytest.raises(ValidationError):
        ScreenshotDocument(start_url=invalid_url, screenshots=screenshots, timestamp=timestamp)


def test_screenshot_document_json_encoding():
    # Arrange
    start_url = "https://example.com/"
    screenshots = ["screenshot1.png"]
    timestamp = datetime(2024, 1, 1, 12, 0, 0)
    obj_id = ObjectId()

    # Act
    document = ScreenshotDocument(
        _id=str(obj_id),
        start_url=start_url,
        screenshots=screenshots,
        timestamp=timestamp)
    document_dict = document.model_dump(by_alias=True)

    # Assert
    assert document_dict["_id"] == str(obj_id)
    assert document_dict["timestamp"].isoformat() == timestamp.isoformat()


def test_screenshot_document_invalid_screenshots():
    # Arrange
    start_url = "https://example.com/"
    invalid_screenshots = [123, None]  # Invalid types for screenshots list
    timestamp = datetime.now()

    # Act & Assert
    with pytest.raises(ValidationError):
        ScreenshotDocument(
            start_url=start_url,
            screenshots=invalid_screenshots,
            timestamp=timestamp
            )
