from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Text
from app.database.connection import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(Integer, ForeignKey("clinics.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    service_id = Column(Integer, ForeignKey("services.id"))

    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)

    status = Column(String, default="pending")
    payment_status = Column(String, default="unpaid")

    notes = Column(Text)
    created_by = Column(String, default="ai_agent")