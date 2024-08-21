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
        self.logger.info(
            "Starting the crawl process", 
            {
                "start_url": start_url, 
                "number_of_links": number_of_links
            })
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
            self.logger.info(
                "Number of links in the page are less than the input",
                {
                    "no_links_extracted": len(links), 
                    "number_of_links": number_of_links
                })

        self.take_screenshots(links, page, run_id)
        for i in range(number_of_links + 1):
            screenshot_filename = f"{run_id}_screenshot_{i}.png"
            screenshot_path = self.base_dir / screenshot_filename
            
            # Simulate the delay for taking a screenshot
            await asyncio.sleep(1)  # Replace this with actual screenshot logic
            
            # Create a dummy screenshot file
            with open(screenshot_path, "w") as f:
                f.write("This is a dummy screenshot file.")
            
            screenshots.append(screenshot_filename)

        # Insert the document into MongoDB
        await self._repository.insert_screenshot_data(run_id, start_url, screenshots)

        return screenshots
    
    async def take_screenshots(self, 
                               links_to_pages: List[str], 
                               page: Page,
                               run_id: str):
        self.logger.info("Starting screenshot of images ", {
            "run_id": run_id,
        })
        asyncio.gather(*[
            self._take_screenshot(
                page, 
                link, 
                self.base_dir / f"{run_id}_screenshot_{i}.png"
            ) for i, link in enumerate(links_to_pages)
        ])

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