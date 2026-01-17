from playwright.async_api import async_playwright, Cookie


class Browser:
    def __init__(self, timeout: int, headless: bool = True):
        self.timeout = timeout
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    async def start(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self.headless)
        self._context = await self._browser.new_context()
        self._page = await self._context.new_page()
        self._page.set_default_timeout(self.timeout)

    async def close(self):
        try:
            if self._context:
                await self._context.close()
            if self._browser:
                await self._browser.close()
        finally:
            if self._playwright:
                await self._playwright.stop()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def goto(self, url: str) -> None:
        await self._page.goto(url)

    async def enter_input(self, element_id: str, value: str) -> None:
        await self._page.locator(f"#{element_id}").fill(value)

    async def click_button(self, element_id, expect_redirect: bool = False) -> None:
        if expect_redirect:
            async with self._page.expect_navigation():
                await self._page.locator(f"#{element_id}").click()
        else:
            await self._page.locator(f"#{element_id}").click()

    def get_page_url(self):
        return self._page.url

    async def get_page_cookies(self, names: list[str] = ()):
        page_cookies = await self._context.cookies(self._page.url)
        if len(names) == 0:
            return page_cookies
        return [c for c in page_cookies if c["name"] in names]
