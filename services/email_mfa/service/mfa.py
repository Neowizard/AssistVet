import datetime
import re
import time
from typing import Optional
from logging import getLogger

import email_fetcher

logger = getLogger(__name__)


class Mfa:
    def __init__(self, config):
        self._config = config
        self._mfa_sender = f'cloud.{self._config.provet_account_id}@mailer.provet.email'


    def get_mfa_code(self, init_time: datetime.datetime, timeout: int = 180, limit: int = 1) -> list[str]:
        def is_email_newer_than_init_time(email):
            return time.mktime(email.Timestamp.timetuple()) >= time.mktime(init_time.timetuple())


        start = time.time()
        fetcher = email_fetcher.EmailFetcher(self._config)
        while True:
            if time.time() - start > timeout:
                logger.info(f"Timeout after {timeout} seconds. No MFA codes found.")
                return []

            logger.info(f"Checking for MFA code from {self._mfa_sender} after {init_time}")
            emails = fetcher.get_emails_by_sender(self._mfa_sender)
            logger.info(f"Found {len(emails)} emails")

            limit = min(limit, len(emails))
            latest = sorted(emails, key=lambda e: e.Timestamp, reverse=True)[:limit]

            valid_codes = [self._get_mfa_code(e.body) for e in latest if is_email_newer_than_init_time(e)]
            valid_codes = [c for c in valid_codes if c is not None]

            if len(valid_codes) == 0 and len(latest) > 0:
                logger.info(f"No MFA code newer than {init_time} yet. Retrying in 10 seconds.")
                time.sleep(10)
            else:
                logger.info(f"{len(valid_codes)} ({limit=}) MFA codes found")
                return valid_codes

    def _get_mfa_code(self, body) -> str:
        m = re.search(r"\b(\d{6})\b", body)
        return m.group(1) if m else None
