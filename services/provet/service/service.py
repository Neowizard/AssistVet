import datetime
import logging
import traceback
import typing
import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from logging import getLogger

from appointment import Appointment
from browser.browser import Browser
from provet import Provet
from provet_config import ProvetConfig

import authentication.authentication

router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = getLogger(__name__)


class AppointmentsRequest(BaseModel):
    from_date: datetime.datetime
    to_date: datetime.datetime


Status = typing.Literal["OK", "ERROR"]


class AppointmentsResponse(BaseModel):
    status: Status
    appointments: list[Appointment]


@router.post("/appointments", summary="Gets appointments from Provet for a time range",
             response_model=AppointmentsResponse)
def get_appointments(request: AppointmentsRequest) -> AppointmentsResponse:
    """
    Get the appointments scheduled in the Provet system for a given time range.
    """
    try:
        logger.info(f"Received request to get appointments for {request.from_date} to {request.to_date}")
        config = ProvetConfig.load('./config.yaml')

        with Browser(config.browser_timeout_ms) as browser:
            provet = Provet(browser)
            appointments = provet.appointments(request.from_date, request.to_date)
            return AppointmentsResponse(status="OK", appointments=appointments)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to get appointments. Error: {str(e)}")
