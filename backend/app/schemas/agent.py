from pydantic import BaseModel
from typing import Optional


class AgentCreate(BaseModel):
    clinic_id: int
    agent_name: str
    agent_type: Optional[str] = "Receptionist"
    voice: Optional[str] = "Female"
    tone: Optional[str] = "Professional"
    sensitivity: Optional[str] = "Medium"
    greeting_message: Optional[str] = None
    system_prompt: Optional[str] = None
    status: Optional[str] = "inactive"


class AgentUpdate(BaseModel):
    agent_name: Optional[str] = None
    agent_type: Optional[str] = None
    voice: Optional[str] = None
    tone: Optional[str] = None
    sensitivity: Optional[str] = None
    greeting_message: Optional[str] = None
    system_prompt: Optional[str] = None
    status: Optional[str] = None


class AgentTestRequest(BaseModel):
    patient_message: str