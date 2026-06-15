from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"))
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"))
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"))

    amount = Column(Float)
    payment_method = Column(String)
    payment_status = Column(String, default="pending")
    transaction_id = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())