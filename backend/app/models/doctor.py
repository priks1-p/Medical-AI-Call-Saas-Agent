from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database.connection import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)

    clinic_id = Column(
        Integer,
        ForeignKey("clinics.id")
    )

    name = Column(String)

    specialty = Column(String)

    phone = Column(String)

    email = Column(String)

    consultation_fee = Column(Float)

    status = Column(
        String,
        default="active"
    )