import datetime
import logging
import traceback
import typing
import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from logging import getLogger
from mfa_config import MfaConfig
from mfa import Mfa

router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = getLogger(__name__)

logger.info('Loaded config from ./config.yaml')

class MfaRequestTime(BaseModel):
    init_time: datetime.datetime

Status = typing.Literal["OK", "ERROR"]

class MfaCodeResponse(BaseModel):
    status: Status
    codes: list[str] = None
    error: typing.Optional[str] = None


@router.post("/get_code", summary="Gets the code for the login MFA", response_model=MfaCodeResponse)
async def get_code(request: MfaRequestTime) -> MfaCodeResponse:
    """
    Collects the MFA code for a login which was initiated before the given time.
    """
    try:
        logger.info(f"Received request to get MFA code")
        MfaConfig.load('./config.yaml')
        mfa = Mfa(MfaConfig.get_config())
        mfa_codes = mfa.get_mfa_code(request.init_time)

        if len(mfa_codes) == 0:
            return MfaCodeResponse(status='ERROR', error='No MFA code found')
        return MfaCodeResponse(status='OK', codes=mfa_codes)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Failed to get MFA code: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get MFA code. Error: {str(e)}")
