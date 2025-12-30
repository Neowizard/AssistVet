import threading

from playwright.sync_api import sync_playwright, Cookie


class Browser:
    def __init__(self, timeout: int, headless: bool = True):
        self.lock = threading.RLock()
        self.timeout = timeout
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def start(self):
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context()
        self._page = self._context.new_page()
        self._page.set_default_timeout(self.timeout)

    def close(self):
        try:
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
        finally:
            if self._playwright:
                self._playwright.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def goto(self, url: str) -> None:
        self._page.goto(url)

    def enter_input(self, element_id: str, value: str) -> None:
         self._page.locator(f"#{element_id}").fill(value)

    def click_button(self, element_id, expect_redirect: bool = False) -> None:
        if expect_redirect:
            with self._page.expect_navigation():
                self._page.locator(f"#{element_id}").click()
        else:
            self._page.locator(f"#{element_id}").click()

    def get_page_url(self):
        return self._page.url

    def get_page_cookies(self, names: list[str] = ()):
        page_cookies = self._context.cookies(self._page.url)
        if len(names) == 0:
            return page_cookies
        return [c for c in page_cookies if c["name"] in names]
