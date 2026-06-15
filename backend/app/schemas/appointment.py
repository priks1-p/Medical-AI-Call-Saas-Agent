from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class AppointmentCreate(BaseModel):
    clinic_id: int
    doctor_id: int
    patient_id: int
    service_id: int
    appointment_date: date
    appointment_time: time
    status: Optional[str] = "pending"
    payment_status: Optional[str] = "unpaid"
    notes: Optional[str] = None
    created_by: Optional[str] = "ai_agent"


class AppointmentUpdate(BaseModel):
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None
    service_id: Optional[int] = None
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[str] = None
    payment_status: Optional[str] = None
    notes: Optional[str] = None


class SlotCheckRequest(BaseModel):
    doctor_id: int
    appointment_date: date


class RescheduleRequest(BaseModel):
    appointment_date: date
    appointment_time: time

class AppointmentCancel(BaseModel):
    reason: str | None = None