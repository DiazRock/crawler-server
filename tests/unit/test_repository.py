import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from pymongo.collection import Collection
from pymongo.database import Database
from repositories.screenshot_repository import ScreenshotRepository

@patch('models.screenshot_document.ScreenshotDocument')
def test_insert_screenshot_data(MockScreenshotDocument):
    # Arrange
    mock_db = MagicMock(spec=Database)
    mock_collection = MagicMock(spec=Collection)
    mock_db.__getitem__.return_value = mock_collection
    repository = ScreenshotRepository(db=mock_db)

    run_id = "test_run_id"
    start_url = "https://example.com"
    screenshots = ["screenshot1.png", "screenshot2.png"]

    # Mock the ScreenshotDocument instance
    mock_screenshot_doc = MockScreenshotDocument.return_value
    mock_screenshot_doc.model_dump.return_value = {
        "_id": run_id,
        "start_url": start_url,
        "screenshots": screenshots,
        "timestamp": datetime.now().isoformat()
    }

    # Act
    repository.insert_screenshot_data(run_id, start_url, screenshots)

    # Assert
    MockScreenshotDocument.assert_called_once_with(
        _id=run_id,
        start_url=start_url,
        screenshots=screenshots,
        timestamp=pytest.mock.ANY  # Match any datetime object
    )
    mock_collection.insert_one.assert_called_once_with(mock_screenshot_doc.model_dump(by_alias=True))

def test_get_screenshots_by_run_id():
    # Arrange
    mock_db = MagicMock(spec=Database)
    mock_collection = MagicMock(spec=Collection)
    mock_db.__getitem__.return_value = mock_collection
    repository = ScreenshotRepository(db=mock_db)

    run_id = "test_run_id"
    expected_document = {
        "_id": run_id,
        "start_url": "https://example.com",
        "screenshots": ["screenshot1.png", "screenshot2.png"],
        "timestamp": datetime.now().isoformat()
    }
    mock_collection.find_one.return_value = expected_document

    # Act
    result = repository.get_screenshots_by_run_id(run_id)

    # Assert
    mock_collection.find_one.assert_called_once_with({"_id": run_id})
    assert result == expected_document
