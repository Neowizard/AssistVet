import traceback

from pydantic import BaseModel

from schema import client, patient


class Appointment(BaseModel):
    id: int
    start: str
    end: str
    rooms: list[str]

    description: str
    notes: str
    tags: list[str]

    client: client.Client
    patients: list[patient.Patient]


def parse_appointment(appointment_dict: dict) -> Appointment:
    rooms = [resource['name'] for resource in (appointment_dict.get('resources') or [])]

    appointment_notes = '\n'.join([appointment_dict.get('notes', ''),
                                   appointment_dict.get('critical_notes', '')])

    description_parts = [appointment_dict.get('reason') or '']
    if appointment_dict.get('reason_type') and appointment_dict['reason_type'].get('name'):
        description_parts.append(appointment_dict['reason_type']['name'])
    description = '\n'.join(description_parts)

    client_data = appointment_dict.get('client') or {}
    patients_data = appointment_dict.get('patients') or []
    tags = _appointment_tags(client_data, patients_data)

    return Appointment(
        id=appointment_dict['id'],
        start=appointment_dict['start'],
        end=appointment_dict['end'],
        rooms=rooms,
        description=description,
        notes=appointment_notes,
        tags=tags,
        client=client.parse_client(client_data),
        patients=[patient.parse_patient(p) for p in patients_data]
    )


def _appointment_tags(client_data: dict, patients_data: list[dict]) -> list:
    tags = client_data.get('tags', [])
    for patient_data in patients_data:
        tags.extend(patient_data.get('tags', []))
    return tags
