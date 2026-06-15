from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.ai_booking_service import create_ai_booking


router = APIRouter(
    prefix="/ai-booking",
    tags=["AI Booking"]
)


class AIBookingRequest(BaseModel):
    clinic_id: int
    message: str


@router.post("/create")
def ai_create_booking(
    data: AIBookingRequest,
    db: Session = Depends(get_db)
):
    return create_ai_booking(
        db=db,
        clinic_id=data.clinic_id,
        message=data.message
    )