import traceback
from datetime import datetime
import logging

import httpx
from pydantic import ValidationError

import endpoints
import provet_config
from appointment import Appointment
from browser.browser import Browser

from authentication import authentication

logger = logging.getLogger(__name__)


class Provet:
    ROOMS_RESOURCE_IDS = ("19", "20", "21", "22", "43")

    def __init__(self, browser: Browser):
        self._config = provet_config.ProvetConfig.get_config()
        self._browser = browser
        self._authentication = authentication.Authentication(self._browser)

    def appointments(self, from_date: datetime, to_date: datetime) -> list[Appointment]:
        session_cookies = self._authentication.get_session()
        if not session_cookies:
            logger.error("Failed to login to Provet system.")
            raise Exception("Failed to login to Provet system.")

        start = from_date.isoformat(timespec='milliseconds') + 'Z'
        end = to_date.isoformat(timespec='milliseconds') + 'Z'
        url = f'{self._config.provet_url}/{self._config.account_id}/{endpoints.APPOINTMENT_ENDPOINT}'

        params = self._build_appointments_params(start, end)
        headers = self._build_appointments_headers(session_cookies)

        with httpx.Client(timeout=10) as client:
            response = client.get(url, params=params, headers=headers)
            response.raise_for_status()
            response_json = response.json()

        appointments = self.create_appointments(response_json)
        return appointments

    def create_appointments(self, response_json) -> list[Appointment]:
        for appointment_json in response_json:
            appointment_json['rooms'] = [resource['name'] for resource in appointment_json['resources']]

        appointments = [Appointment(**a_json) for a_json in response_json]
        logger.info(f"Successfully parsed {len(appointments)} appointments")
        return appointments

    def _build_appointments_params(self, start, end) -> list:
        start_param = ('start', start)
        end_param = ('end', end)
        department_param = ('department_ids[]', self._config.department_id)
        resources_params = [('resource_ids[]', resource_id) for resource_id in self.ROOMS_RESOURCE_IDS]
        return [start_param, end_param, department_param] + resources_params

    def _build_appointments_headers(self, session_cookies) -> dict:
        cookies = [f'{cookie["name"]}={cookie["value"]}' for cookie in session_cookies]
        cookies_header = '; '.join(cookies)
        headers = {'Cookie': cookies_header}
        return headers
