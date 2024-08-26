from fastapi import APIRouter, Depends, HTTPException, status
from logging import Logger
from pathlib import Path
from dtos.screenshot import ScreenshotRequest, ScreenshotResponse
import uuid
from dep_container import get_crawler_service, get_logger, get_cache_client
from services.crawler import Crawler

router = APIRouter()

@router.post(
            "/screenshots",
            summary="Start screenshot process",
            description="""
            This endpoint initiates a process that crawls a website starting from the provided `start_url` 
            and takes screenshots of the initial page and the first `number_of_links_to_follow` links found on the page. 
            It returns a unique `run_id` which can be used to retrieve the screenshots later.
            """,
            responses={
                200: {
                    "description": "Screenshot process initiated successfully",
                    "content": {
                        "application/json": {
                            "example": {
                                "run_id": "abc123"
                            }
                        }
                    }
                },
                400: {
                    "description": "Invalid request parameters",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Invalid input provided"
                            }
                        }
                    }
                }
            }
        )
async def start_screenshot_process(
                                   request: ScreenshotRequest, 
                                   crawler_service: Crawler = Depends(get_crawler_service),
                                   logger: Logger = Depends(get_logger),
                                   cache_client = Depends(get_cache_client)
                                   ):
    """
    Starts a task to take screenshots of a webpage and its links.
    
    - **start_url**: The URL from which the crawling and screenshot process begins.
    - **number_of_links_to_follow**: The number of links to follow and take screenshots of.
    """
    run_id = str(uuid.uuid4())
    logger.info("Run id generated", extra= {"run_id": run_id})
    try:
        screenshots = await crawler_service.crawl_website(
                            request.start_url, 
                            request.number_of_links_to_follow, 
                            run_id
                            )
        await cache_client.rpush(run_id, *screenshots)  # Cache for 1 hour
    except Exception as e:
        logger.error("Error occurred while crawling website", {"exception": e})
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"An error occurred while crawling the website {e}")
        
    return {"run_id": run_id, "screenshots": screenshots}

@router.get("/screenshots/{run_id}",
            summary="Get screenshots by run ID",
            description="Retrieve the screenshots associated with a specific run ID.",
            response_model=ScreenshotResponse,
            responses={
                200: {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "example": {
                                "run_id": "abc123",
                                "screenshots": [
                                    "abc123_screenshot_0.png",
                                    "abc123_screenshot_1.png"
                                ]
                            }
                        }
                    }
                },
                404: {
                        "description": "Run ID not found",
                        "content": {
                            "application/json": {
                                "example": {
                                    "detail": "Run ID not found"
                                }
                            }
                        }
                    }
                }
            )
async def get_screenshots(
                run_id: str, 
                crawler_service: Crawler = Depends(get_crawler_service),
                logger: Logger = Depends(get_logger),
                cache_client = Depends(get_cache_client)
                ):
    """
        Retrieves all screenshots associated with a given run ID.
    
        - **run_id**: A unique identifier generated when the screenshot process was initiated. This ID is used to fetch the corresponding screenshots from the database.
        
        Returns:
        - A list of screenshot file names associated with the run ID.
        - If the run ID is not found in the database, an HTTP 404 error is raised.

        Example response:
        ```
        {
            "run_id": "abc123",
            "screenshots": [
                "abc123_screenshot_0.png",
                "abc123_screenshot_1.png"
            ]
        }
        ```
    """

    logger.info("Getting screenshots for run id", extra= {"run_id": run_id})
    # Retrieve screenshots from cache or database if available
    cached_data = await cache_client.lrange(run_id, 0, -1)
    if cached_data:
        logger.info("Screenshots fetched from cache", extra= {"run_id": run_id})
        return {"run_id": run_id, "screenshots": cached_data}
    
    record = crawler_service.get_screenshots_by_run_id(run_id= run_id)
    if not record:
        logger.error("Screenshots not found in database", extra= {"run_id": run_id})  # Log error for debugging purposes
        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Screenshots not found for the provided ID"
                            )
    
    screenshots = record["screenshots"]
    return {"run_id": run_id, "screenshots": screenshots}


