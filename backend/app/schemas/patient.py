from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class PatientCreate(BaseModel):
    clinic_id: int
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = "active"


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None