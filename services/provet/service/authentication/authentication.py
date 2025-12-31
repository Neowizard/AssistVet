import datetime
import logging
from typing import Optional

import authentication.mfa
import endpoints
import provet_config
from browser.browser import Browser
from browser.cookie_store import CookieStore
logger = logging.getLogger(__name__)


class Authentication:
    SESSION_COOKIE_NAMES = ['csrftoken', 'sessionid', 'AWSALB', 'AWSALBCORS']

    def __init__(self, browser: Browser):
        self._browser = browser
        self._config = provet_config.ProvetConfig.get_config()
        self._mfa = authentication.mfa.Mfa()

    def login(self) -> Optional[list[dict]]:
        url = f'https://{self._config.provet_url}/{self._config.account_id}/auth/login/'
        logger.info(f"Logging into {url}")
        self._browser.goto(url)
        self._browser.enter_input("id_username", self._config.provet_username)
        self._browser.enter_input("id_password", self._config.provet_password)
        login_time = datetime.datetime.now()
        self._browser.click_button("id_btn_login", expect_redirect=True)
        url = self._browser.get_page_url()
        if endpoints.check_url_endpoint(url, endpoints.MFA_CHALLENGE_ENDPOINT):
            self._mfa.resolve_mfa(self._browser, login_time)

        url = self._browser.get_page_url()
        if endpoints.check_url_endpoint(url, endpoints.DASHBOARD_ENDPOINT):
            return self._browser.get_page_cookies(Authentication.SESSION_COOKIE_NAMES)
        logger.error(f"Failed to login to {url}. "
                     f"Expected landing endpoint: {endpoints.DASHBOARD_ENDPOINT}. "
                     f"Actual: {url}")
        return None

    def get_session(self):
        session_cookies = CookieStore.retrieve(self._config.provet_url, self.SESSION_COOKIE_NAMES)
        if len(session_cookies) < len(self.SESSION_COOKIE_NAMES):
            logger.info(f"Missing active session cookies ({len(session_cookies)} < {len(self.SESSION_COOKIE_NAMES)}).")
            session_cookies = self.login()
            CookieStore.store(self._config.provet_url, session_cookies)
        return session_cookies


