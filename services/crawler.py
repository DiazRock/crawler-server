import asyncio
from pathlib import Path
from typing import List
from pyppeteer import launch
from pyppeteer.page import Page
from logging import Logger
from repositories.screenshot_repository import ScreenshotRepository

class Crawler:
    def __init__(self, 
                repository: ScreenshotRepository, 
                base_dir: Path, 
                logger: Logger):
        self._repository = repository
        self.base_dir = base_dir
        self.logger = logger

    async def crawl_website(self, start_url: str, number_of_links: int, run_id: str):
        # Simulate an asynchronous task, e.g., fetching a URL and taking a screenshot
        log_dict = {
            "run_id": run_id,
            "start_url": start_url, 
            "number_of_links": number_of_links
        }
        self.logger.info(
            "Starting the crawl process", 
            extra = log_dict)
        screenshots = []
        browser = await launch()
        page = await browser.newPage()
        await page.goto(start_url)

        links = await page.evaluate(f"""
            () => Array.from(document.querySelectorAll('a'))
            .slice(0, {number_of_links})
            .map(link => link.href)
        """)

        if len(links) < number_of_links:
            extra = {"no_links_found": len(links)}
            extra.update(log_dict)
            self.logger.warn(
                "Number of links in the page are less than the input",
                extra=extra,
            )

        self.take_screenshots(links, page, run_id, log_dict)
        

        # Insert the document into MongoDB
        await self._repository.insert_screenshot_data(run_id, start_url, screenshots)

        return screenshots
    
    async def take_screenshots(self, 
                               links_to_pages: List[str], 
                               page: Page,
                               run_id: str,
                               log_dict: dict):
        extra = {
            "run_id": run_id,
        }
        extra.update(log_dict)
        self.logger.info("Starting screenshot of images ", extra = log_dict)

        asyncio.gather(*[
            self._take_screenshot(
                page, 
                link, 
                self.base_dir / f"{run_id}_screenshot_{i}.png"
            ) for i, link in enumerate(links_to_pages)
        ])

    async def get_screenshots_by_run_id(self, run_id: str):
        """"""
        return await self._repository.get_screenshots_by_run_id(run_id)

    async def _take_screenshot(self, page: Page, url: str, screenshot_path: Path):
        """
        Navigates to the given URL, waits for the page to load, and takes a screenshot.

        Args:
            page: The Playwright page object.
            url (str): The URL to navigate to.
            screenshot_path (Path): The path where the screenshot will be saved.
        """
        try:
            await page.goto(url)  # Navigate to the URL
            page.screenshot(path=str(screenshot_path))  # Take the screenshot
        except Exception as e:
            self.logger.error(f"Error taking screenshot", 
                              {"url": url, "exception": e})
    