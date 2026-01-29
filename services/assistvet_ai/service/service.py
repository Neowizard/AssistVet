import logging
import sys
from fastapi import APIRouter
from logging import getLogger

router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = getLogger(__name__)

logger.info('Loaded config from ./config.yaml')

