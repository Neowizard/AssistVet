from datetime import datetime
import logging

import httpx

import endpoints
import provet_config
from schema import appointment

from authentication.authentication import Authentication

logger = logging.getLogger(__name__)


class Provet:
    ROOMS_RESOURCE_IDS = ("19", "20", "21", "22", "43")

    def __init__(self, authentication: Authentication):
        self._authentication = authentication
        self._config = provet_config.ProvetConfig.get_config()

    async def appointments(self, from_date: datetime, to_date: datetime) -> list[appointment.Appointment]:
        session_cookies = await self._authentication.get_session()
        if not session_cookies:
            logger.error("Failed to login to Provet system.")
            raise Exception("Failed to login to Provet system.")

        start = from_date.isoformat(timespec='milliseconds') + 'Z'
        end = to_date.isoformat(timespec='milliseconds') + 'Z'
        url = f'https://{self._config.provet_url}/{self._config.account_id}/{endpoints.APPOINTMENT_ENDPOINT}'

        params = self._build_appointments_params(start, end)
        headers = self._build_appointments_headers(session_cookies)

        try:
            with httpx.Client(timeout=10) as client:
                response = client.get(url, params=params, headers=headers)
                response.raise_for_status()
                response_json = response.json()
        except Exception as e:
            logger.warning(f"Failed to get appointments information: {e}. Retrying...")
            with httpx.Client(timeout=10) as client:
                response = client.get(url, params=params, headers=headers)
                response.raise_for_status()
                response_json = response.json()
        appointments = self.parse_appointments(response_json)
        return appointments

    def parse_appointments(self, response: dict) -> list[appointment.Appointment]:
        appointments = [appointment.parse_appointment(appointment_dict) for appointment_dict in response]

        logger.info(f"Successfully parsed {len(appointments)} appointments")
        return appointments

    def _build_appointments_params(self, start, end) -> list:
        start_param = ('start', start)
        end_param = ('end', end)
        department_param = ('department_ids[]', self._config.department_id)
        resources_params = [('resource_ids[]', resource_id) for resource_id in self.ROOMS_RESOURCE_IDS]
        return [start_param, end_param, department_param] + resources_params

    def _build_appointments_headers(self, session_cookies) -> dict:
        cookies = [f'{cookie.name}={cookie.value}' for cookie in session_cookies]
        cookies_header = '; '.join(cookies)
        headers = {'Cookie': cookies_header}
        return headers
