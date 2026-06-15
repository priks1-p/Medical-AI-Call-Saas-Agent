from pydantic import BaseModel
from typing import Optional


class KnowledgeBaseCreate(BaseModel):
    clinic_id: int
    question: str
    answer: str
    category: Optional[str] = None


class KnowledgeBaseUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None