from datetime import datetime
import logging
from db.db import CookiesTable, Cookie

logger = logging.getLogger(__name__)


class CookieStore:
    @classmethod
    def store(cls, url: str, cookies: list[dict]) -> None:
        logger.info(f"Storing {len(cookies)} cookies for {url}")
        CookiesTable.store_cookies(cookies)

    @classmethod
    def retrieve(cls, domain: str, names: list[str]) -> list[Cookie]:
        logger.info(f"Retrieving cookies for {domain}")
        cookies: list[Cookie] = CookiesTable.get_cookies(domain, names)
        if cookies is None or len(cookies) == 0:
            logger.info(f"No cookies for {domain}")
            return []
        cookies = cls._remove_expired_cookies(cookies)


        logger.info(f"Retrieved {len(cookies)} cookies")
        return cookies

    @classmethod
    def _remove_expired_cookies(cls, domain_cookies: list[Cookie]) -> list[Cookie]:
        def is_expired(cookie: Cookie, retain_sessions_cookies=True):
            if cookie.expiration is None:
                return not retain_sessions_cookies
            return datetime.now() > cookie.expiration

        invalid_cookies = [c for c in domain_cookies if is_expired(c)]
        if len(invalid_cookies) > 0:
            logger.info(f"Removing expired cookies: {[c.name for c in invalid_cookies]}")
            CookiesTable.remove_cookies(invalid_cookies)

        return [c for c in domain_cookies if c not in invalid_cookies]
