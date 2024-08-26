import pytest
import os
import shutil
from typing import List
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response
from functools import lru_cache
from dep_container import get_crawler_service, get_screenshot_repository
from main import app


def delete_test_directory(test_dir):
    """Delete the specified directory and its contents."""
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)

# Override the dependency to use mongomock in tests
@pytest.fixture(scope="function")
async def test_client():

    # Singleton to keep alive db client inside the service
    @lru_cache(maxsize=None)
    def get_crawler_service_singleton():
        return get_crawler_service(use_mongomock=True)
    
    app.dependency_overrides[get_crawler_service] = get_crawler_service_singleton
    app.dependency_overrides[get_screenshot_repository] = lambda: get_screenshot_repository(use_mongomock=True)
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


def test_get_isalive():
    client = TestClient(app)
    response = client.get("/isalive")
    assert response.status_code == 200
    assert response.json() == {"status": "Server is alive"}


@pytest.mark.asyncio
async def test_post_screenshots(test_client: AsyncClient):
    # Step 1: Submit the screenshot job
    payload = {
        "start_url": "https://edited.com/",
        "number_of_links_to_follow": 5
    }
    response: Response = await test_client.post("/screenshots", json=payload)
    assert response.status_code == 200
    assert "run_id" in response.json()

    # Step 2: Get the run_id
    run_id = response.json()["run_id"]

    # Step 3: Poll the server for the screenshots
    screenshot_response: Response = await test_client.get(f"/screenshots/{run_id}")
    assert screenshot_response.status_code == 200
    screenshots: List[str] = screenshot_response.json().get("screenshots")
    
    assert screenshots is not None, "Screenshots were not generated."
    assert len(screenshots) == payload["number_of_links_to_follow"] + 1  # Including the start_url screenshot

    # Step 4: Verify the screenshots (just checking the filenames here)
    for i, screenshot in enumerate(screenshots):
        expected_filename = f"{run_id}_screenshot_{i}.png"
        assert screenshot.endswith(expected_filename), f"Unexpected screenshot filename: {screenshot}"
    
    # Step 5: Clean up the created folder
    delete_test_directory(os.getenv('SCREENSHOT_FOLDER'))
