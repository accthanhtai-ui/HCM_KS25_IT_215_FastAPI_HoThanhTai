from pydantic import BaseModel, Field


class MedicalRegister(BaseModel):
    username: str
    password: str
    role: str = Field(
        pattern="^(doctor|pharmacist)$"
    )


class MedicalLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class PrescriptionCreate(BaseModel):
    patient_name: str
    medicine: str
    quantity: int


class PrescriptionResponse(BaseModel):
    message: str