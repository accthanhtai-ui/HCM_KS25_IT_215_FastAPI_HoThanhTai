from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ClinicCreate(BaseModel):
    clinic_name: str = Field(..., min_length=1)
    specialty: str = Field(..., min_length=1)


class DoctorResponse(BaseModel):
    doctor_code: str
    salary: float

    model_config = ConfigDict(from_attributes=True)


class ClinicDetailResponse(BaseModel):
    id: int
    clinic_name: str
    specialty: str
    doctors: list[DoctorResponse]

    model_config = ConfigDict(from_attributes=True)


class DoctorUpdate(BaseModel):
    doctor_code: Optional[str] = None
    salary: Optional[float] = None
    clinic_id: Optional[int] = None


class LicenseResponse(BaseModel):
    id: int
    license_number: str
    issue_by: str

    model_config = ConfigDict(from_attributes=True)