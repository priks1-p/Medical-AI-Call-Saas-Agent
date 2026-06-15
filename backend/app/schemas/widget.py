from pydantic import BaseModel
from typing import Optional


class WidgetCreate(BaseModel):
    clinic_id: int
    agent_id: int
    theme: Optional[str] = "light"
    position: Optional[str] = "bottom_right"
    greeting: Optional[str] = "Hello! How can I help you?"
    status: Optional[str] = "active"