from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ClientModel(BaseModel):
    id: int
    name: str
    phone_number: str
    street_address: Optional[str] = ""
    city: Optional[str] = ""
    remarks: Optional[str] = ""
    critical_notes: Optional[str] = ""


class ResourceModel(BaseModel):
    id: int
    name: str


class Appointment(BaseModel):
    id: int
    start: datetime
    end: datetime
    reason: str
    notes: str
    critical_notes: str
    client: ClientModel
    rooms: list[str]

