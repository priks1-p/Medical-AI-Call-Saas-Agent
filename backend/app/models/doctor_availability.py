from sqlalchemy import Column, Integer, String, Time, Boolean, ForeignKey
from app.database.connection import Base


class DoctorAvailability(Base):
    __tablename__ = "doctor_availability"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id", ondelete="CASCADE")
    )

    day_of_week = Column(String)

    start_time = Column(Time)

    end_time = Column(Time)

    slot_duration = Column(Integer, default=30)

    is_available = Column(Boolean, default=True)