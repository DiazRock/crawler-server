from pyppeteer import launch
from pyppeteer.page import Page
from pyppeteer.browser import Browser

class BrowserContextManager:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None

    async def __aenter__(self) -> Browser:
        try:
            # Launch the browser
            self.browser = await launch({
                'headless': self.headless,
                'args' : [
                    '--no-sandbox',  # Required to run Chrome in a container
                    '--disable-dev-shm-usage'  # Required to run Chrome in a container
                    '--disable-setuid-sandbox',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process'
                ]
            })
            return self.browser
        except Exception as e:
            if self.browser:
                await self.browser.close()
            raise e

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Close the browser when done
        if self.browser:
            await self.browser.close()

class PageContextManager:
    def __init__(self, browser: Browser, headless=False):
        self.headless = headless
        self.browser = browser
        self.page = None

    async def __aenter__(self) -> Page:
        try:
            # Open a new page
            self.page = await self.browser.newPage()
            return self.page
        except Exception as e:
            if self.page:
                await self.page.close()
            raise e

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Close the page when done
        if self.page:
            await self.page.close()
