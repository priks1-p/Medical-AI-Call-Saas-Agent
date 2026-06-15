from pydantic import BaseModel, EmailStr


class PatientRegister(BaseModel):
    patient_id: int
    email: EmailStr
    password: str


class PatientLogin(BaseModel):
    email: EmailStr
    password: str