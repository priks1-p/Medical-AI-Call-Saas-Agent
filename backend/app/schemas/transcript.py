from pydantic import BaseModel


class TranscriptCreate(BaseModel):
    call_id: int
    speaker: str
    message: str