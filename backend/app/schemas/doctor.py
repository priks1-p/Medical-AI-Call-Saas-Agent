from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import time


class DoctorCreate(BaseModel):
    clinic_id: int
    name: str
    specialty: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    consultation_fee: Optional[float] = 0
    status: Optional[str] = "active"


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    consultation_fee: Optional[float] = None
    status: Optional[str] = None


class AvailabilityCreate(BaseModel):
    doctor_id: int
    day_of_week: str
    start_time: time
    end_time: time
    slot_duration: Optional[int] = 30
    is_available: Optional[bool] = True