from typing import Optional
from pydantic import BaseModel, Field


class Client(BaseModel):
    id: int
    name: str
    phone_number: str
    notes: str


def parse_client(client_dict: dict) -> Client:
    client_notes = '\n'.join([client_dict.get('notes') or '',
                              client_dict.get('critical_notes') or ''])
    return Client(
        id=client_dict.get('id') or -1,
        name=client_dict.get('name') or '',
        phone_number=client_dict.get('phone_number') or '',
        notes=client_notes
    )
