import os
from playwright_research import PlaywrightResearch

class BrowserBridge:
    def __init__(self, config=None):
        self.config = config or {}
        self.playwright = PlaywrightResearch(self.config.get("web_research", {}))

    def navigate_and_extract(self, url):
        """Standard bridge for navigation and text extraction."""
        if self.playwright.is_available():
            return self.playwright.fetch_page(url)
        return {"error": "Playwright unavailable. Browser research blocked."}
