from pydantic import BaseModel
from typing import Optional


class CallCreate(BaseModel):
    clinic_id: int
    patient_id: Optional[int] = None
    agent_id: Optional[int] = None
    call_type: Optional[str] = "web_voice"
    duration_seconds: Optional[int] = 0
    call_status: Optional[str] = "started"
    booking_result: Optional[str] = "no_booking"


class CallUpdate(BaseModel):
    patient_id: Optional[int] = None
    agent_id: Optional[int] = None
    call_type: Optional[str] = None
    duration_seconds: Optional[int] = None
    call_status: Optional[str] = None
    booking_result: Optional[str] = None