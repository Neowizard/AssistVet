from logging import getLogger

logger = getLogger(__name__)

DASHBOARD_ENDPOINT = "dashboard"
MFA_CHALLENGE_ENDPOINT = "auth/login/verify"
APPOINTMENT_ENDPOINT = "personnel/calendar/events"


def check_url_endpoint(url: str, endpoint: str) -> bool:
    return url.split('?', 1)[0].strip('/').endswith(endpoint)
