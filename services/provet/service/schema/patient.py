from pydantic import BaseModel


class Patient(BaseModel):
    id: int
    birthdate: str
    name: str
    gender: str
    species: str
    notes: str


def parse_patient(patient_data: dict) -> Patient:
    patient_notes = '\n'.join([patient_data.get('notes') or '',
                               patient_data.get('critical_notes') or ''])

    birthdate = patient_data.get('birthdate') or ''


    return Patient(
        id=patient_data.get('id') or -1,
        birthdate=birthdate,
        name=patient_data.get('name') or '',
        gender=patient_data.get('gender') or '',
        species=patient_data.get('species') or '',
        notes=patient_notes
    )
