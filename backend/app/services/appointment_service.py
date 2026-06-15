from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor_availability import DoctorAvailability


def generate_time_slots(start_time, end_time, slot_duration):
    slots = []

    current = datetime.combine(datetime.today(), start_time)
    end = datetime.combine(datetime.today(), end_time)

    while current + timedelta(minutes=slot_duration) <= end:
        slots.append(current.time())
        current += timedelta(minutes=slot_duration)

    return slots


def get_available_slots(db: Session, doctor_id: int, appointment_date):
    day_name = appointment_date.strftime("%A")

    availability = db.query(DoctorAvailability).filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.day_of_week == day_name,
        DoctorAvailability.is_available == True
    ).first()

    if not availability:
        return []

    all_slots = generate_time_slots(
        availability.start_time,
        availability.end_time,
        availability.slot_duration
    )

    booked_appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date,
        Appointment.status.in_(["pending", "confirmed", "rescheduled"])
    ).all()

    booked_times = [appt.appointment_time for appt in booked_appointments]

    available_slots = [
        slot for slot in all_slots
        if slot not in booked_times
    ]

    return available_slots


def is_slot_available(
    db: Session,
    doctor_id: int,
    appointment_date,
    appointment_time
):
    available_slots = get_available_slots(
        db=db,
        doctor_id=doctor_id,
        appointment_date=appointment_date
    )

    return appointment_time in available_slots