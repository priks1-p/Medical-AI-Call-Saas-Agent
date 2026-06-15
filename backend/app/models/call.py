from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"))
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="SET NULL"), nullable=True)
    agent_id = Column(Integer, ForeignKey("ai_agents.id", ondelete="SET NULL"), nullable=True)

    call_type = Column(String, default="web_voice")
    duration_seconds = Column(Integer, default=0)
    call_status = Column(String, default="started")
    booking_result = Column(String, default="no_booking")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )