from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(
        Integer,
        ForeignKey("clinics.id", ondelete="CASCADE")
    )

    full_name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    dob = Column(Date)
    gender = Column(String)
    address = Column(Text)
    status = Column(String, default="active")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )