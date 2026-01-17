from datetime import datetime, timedelta
import logging
import traceback
import typing
import sys
from fastmcp import FastMCP
from fastapi import HTTPException
from pydantic import BaseModel
from logging import getLogger

from schema import Appointment
from authentication.authentication import Authentication
from browser.browser import Browser
from provet import Provet
from provet_config import ProvetConfig
from db import db

provet_mcp = FastMCP()

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


class ShiftsResponse(BaseModel):
    status: Status
    Shifts: list[Appointment]


@provet_mcp.tool("provet_appointments",
                 description=" Gets appointments from Provet between from_date and to_date (inclusive) given in YYYY-MM-DD format")
async def get_provet_appointments(from_date: str, to_date: str) -> AppointmentsResponse:
    """
    Get the appointments scheduled in the Provet system for a given time range given as YYYY-MM-DD
    """
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(hours=23, minutes=59, seconds=59)
    try:
        logger.info(f"Received request to get appointments for {from_date} to {to_date}")
        config = ProvetConfig.load('./config.yaml')
        db.CookiesTable.connect(config)
        async with Browser(config.browser_timeout_ms) as browser:
            authentication = Authentication(browser)
            provet = Provet(authentication)
            appointments = await provet.appointments(from_date, to_date)
            return AppointmentsResponse(status="OK", appointments=appointments)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to get appointments. Error: {str(e)}")

# @provet_mcp.tool("provet_shifts",
#                  summary="Gets doctor and nurses shifts from Provet for a time range")
# def provet_shifts(request: ShiftsRequests) -> ShiftsResponse:
#     """
#     Get the shifts scheduled in the Provet system for a given time range.
#     """
#     try:
#         logger.info(f"Received request to get shifts for {request.from_date} to {request.to_date}")
#         config = ProvetConfig.load('./config.yaml')
#         db.CookiesTable.connect(config)
#         with Browser(config.browser_timeout_ms) as browser:
#             provet = Provet(browser)
#
#             return ShiftsResponse(status="OK", Shifts=shifts)
#
#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Failed to get shifts. Error: {str(e)}")
