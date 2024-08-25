import pytest
import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_isalive():
    response = client.get("/isalive")
    assert response.status_code == 200
    assert response.json() == {"status": "Server is alive"}

def test_post_screenshots():
    # Step 1: Submit the screenshot job
    payload = {
        "start_url": "https://edited.com/",
        "number_of_links_to_follow": 5
    }
    response = client.post("/screenshots", json=payload)
    assert response.status_code == 200
    assert "run_id" in response.json()

    # Step 2: Get the run_id
    run_id = response.json()["run_id"]

    # Step 3: Poll the server for the screenshots until they are ready
    max_retries = 10
    retries = 0
    screenshots = None
    while retries < max_retries:
        response = client.get(f"/screenshots/{run_id}")
        if response.status_code == 200:
            screenshots = response.json().get("screenshots")
            if screenshots:
                break
        retries += 1
        time.sleep(1)  # Wait before retrying
    
    assert screenshots is not None, "Screenshots were not generated."
    assert len(screenshots) == payload["number_of_links_to_follow"] + 1  # Including the start_url screenshot

    # Step 4: Verify the screenshots (just checking the filenames here)
    for i, screenshot in enumerate(screenshots):
        expected_filename = f"{run_id}_screenshot_{i}.png"
        assert screenshot.endswith(expected_filename), f"Unexpected screenshot filename: {screenshot}"
