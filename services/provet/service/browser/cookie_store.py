from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CookieStore:
    _instance = None
    _cookies: dict[str, list[dict]] = {}

    @classmethod
    def store(cls, url: str, cookies: list[dict]) -> None:
        logger.info(f"Storing {len(cookies)} cookies for {url}")
        cls._cookies[url] = cookies

    @classmethod
    def retrieve(cls, domain: str, names: list[str]) -> list[dict]:
        logger.info(f"Retrieving cookies for {domain}")
        domain_cookies = cls._cookies.get(domain, None)
        if domain_cookies is None:
            logger.info(f"No cookies for {domain}")
            return []
        cls._remove_expired_cookies(domain_cookies)

        matching_cookies = [cookie for cookie in cls._cookies[domain] if cookie["name"] in names]

        logger.info(f"Retrieved {len(matching_cookies)} cookies")
        return matching_cookies

    @classmethod
    def clear(cls) -> None:
        logger.info("Clearing cookie storage")
        cls._cookies = {}

    @classmethod
    def _remove_expired_cookies(cls, domain_cookies):
        def is_expired(cookie):
            return datetime.now() > datetime.fromtimestamp(cookie['expires'])

        invalid_cookies = [c for c in domain_cookies if not is_expired(c)]
        if len(invalid_cookies) > 0:
            logger.info(f"Removing {len(invalid_cookies)} expired cookies")
        [domain_cookies.remove(c) for c in invalid_cookies]
