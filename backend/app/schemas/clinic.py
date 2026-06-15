from pydantic import BaseModel, EmailStr
from typing import Optional


class ClinicSetup(BaseModel):
    clinic_name: str
    owner_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "India"
    timezone: Optional[str] = "Asia/Kolkata"


class ClinicUpdate(BaseModel):
    clinic_name: Optional[str] = None
    owner_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None