from pydantic import BaseModel
from typing import Optional


class ServiceCreate(BaseModel):
    clinic_id: int
    service_name: str
    description: Optional[str] = None
    category: Optional[str] = None
    duration: int
    price: Optional[float] = 0
    status: Optional[str] = "active"


class ServiceUpdate(BaseModel):
    service_name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[float] = None
    status: Optional[str] = None