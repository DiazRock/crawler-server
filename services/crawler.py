from pathlib import Path, PosixPath
from typing import List
from pyppeteer.browser import Browser
from logging import Logger
from repositories.screenshot_repository import ScreenshotRepository
from utils.context_managers import BrowserContextManager, PageContextManager

class Crawler:
    def __init__(self, 
                repository: ScreenshotRepository, 
                base_dir: Path, 
                logger: Logger):
        self._repository = repository
        self.base_dir = base_dir
        self.logger = logger

    async def crawl_website(self, start_url: str, number_of_links: int, run_id: str):
        """
        
        """

        log_dict = {
            "run_id": run_id,
            "start_url": start_url, 
            "number_of_links": number_of_links
        }
        self.logger.info(
            f"Starting the crawl process {log_dict}")
        
        async with BrowserContextManager() as browser:
            links = [start_url]
            async with PageContextManager(browser) as page:
                await page.goto(start_url)
                links += await page.evaluate(f"""
                    () => Array.from(document.querySelectorAll('a'))
                    .slice(0, {number_of_links})
                    .map(link => link.href)
                """)

            log_dict.update({"links": links})
            self.logger.info(f"Links extracted from start url {log_dict}")
            if len(links) < number_of_links:
                extra = {"no_links_found": len(links)}
                extra.update(log_dict)
                self.logger.warn(
                    f"Number of links in the page are less than the input {extra}"
                )

            screenshots: List[str] = await self.take_screenshots(links, browser, run_id, log_dict)

            # Insert the document into MongoDB
            self.logger.info(f"Inserting screenshot in database {log_dict}")
            self._repository.insert_screenshot_data(run_id, start_url, screenshots)
            self.logger.info(f"Screenshot inserted {log_dict}")
            return screenshots
        
    async def take_screenshots(self, 
                               links_to_pages: List[str], 
                               browser: Browser,
                               run_id: str,
                               log_dict: dict):
        extra = {
            "run_id": run_id,
        }
        extra.update(log_dict)
        self.logger.info(f"Starting screenshot of images {extra}")

        screenshot_paths: List[str] = []

        for i, link in enumerate(links_to_pages):
            try:
                path = self.base_dir / f"{run_id}_screenshot_{i}.png" 
                path_str = await self._take_screenshot(
                    browser, 
                    link, 
                    path
                )
                screenshot_paths.append(path_str)
            except Exception as e:
                self.logger.warn(f"Could not do screenshot for path 'path': {path}")
                self.logger.error(f"Error taking screenshot 'url': {link} 'exception': {e}")

        self.logger.info(f"Screenshot of images finished {log_dict}")

        return screenshot_paths


    def get_screenshots_by_run_id(self, run_id: str):
        """"""
        return self._repository.get_screenshots_by_run_id(run_id)

    async def _take_screenshot(self, browser: Browser, url: str, screenshot_path: PosixPath):
        """
        Navigates to the given URL, waits for the page to load, and takes a screenshot.

        Args:
            page: The Pyppeteer page object.
            url (str): The URL to navigate to.
            screenshot_path (Path): The path where the screenshot will be saved.
        """

        async with PageContextManager(browser) as current_page:
            await current_page.goto(url)  # Navigate to the URL
            await current_page.screenshot(path=str(screenshot_path))  # Take the screenshot
            return screenshot_path._str
    