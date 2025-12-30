import os
from dataclasses import dataclass
from xmlrpc.client import DateTime

import yaml
from pathlib import Path

@dataclass(frozen=True, slots=True)
class FetchedEmail:
    subject: str
    From: str
    Timestamp: DateTime
    body: str
