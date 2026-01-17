import datetime
import logging

import httpx

import endpoints
import provet_config
from browser.browser import Browser

logger = logging.getLogger(__name__)


class Mfa:
    def __init__(self):
        self._config = provet_config.ProvetConfig.get_config()

    async def resolve_mfa(self, browser: Browser, mfa_init_time: datetime.datetime):
        self._verify_mfa_page(browser)

        mfa_codes = self._get_mfa_code(mfa_init_time)
        logger.info(f"Got {len(mfa_codes)} codes. Entering into MFA prompt")
        if len(mfa_codes) == 0:
            raise Exception("No MFA codes found.")
        await browser.enter_input("id_twofactor_given_code", mfa_codes[0])
        await browser.click_button("id_btn_login", expect_redirect=True)

    def _get_mfa_code(self, mfa_init_time: datetime.datetime) -> list[str]:
        url = f'{self._config.mfa_service_url}/assistvet/mfa/get_code'
        body = {'init_time': mfa_init_time.isoformat()}
        logger.info(f"Requesting MFA code from {url}")

        with httpx.Client() as client:
            try:
                response = client.post(url, json=body, timeout=self._config.mfa_timeout_sec)
                return response.json()["codes"]
            except httpx.TimeoutException:
                return []

    def _verify_mfa_page(self, browser):
        url = browser.get_page_url()
        if not endpoints.check_url_endpoint(url, endpoints.MFA_CHALLENGE_ENDPOINT):
            raise Exception("Not on MFA page")
