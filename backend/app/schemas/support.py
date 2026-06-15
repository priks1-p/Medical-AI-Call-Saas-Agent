from pydantic import BaseModel
from typing import Optional


class SupportTicketCreate(BaseModel):
    clinic_id: int
    patient_id: int
    subject: str
    status: Optional[str] = "open"
    priority: Optional[str] = "normal"


class SupportTicketUpdate(BaseModel):
    subject: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class SupportMessageCreate(BaseModel):
    ticket_id: int
    sender_type: str
    message: str
    attachment_url: Optional[str] = None