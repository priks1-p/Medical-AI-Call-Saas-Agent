from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"))
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"))

    subject = Column(String)
    status = Column(String, default="open")
    priority = Column(String, default="normal")

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SupportMessage(Base):
    __tablename__ = "support_messages"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(Integer, ForeignKey("support_tickets.id", ondelete="CASCADE"))

    sender_type = Column(String)
    message = Column(Text)
    attachment_url = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())