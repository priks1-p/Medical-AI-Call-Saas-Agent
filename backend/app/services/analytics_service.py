from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.call import Call
from app.models.payment import Payment
from app.models.ai_agent import AIAgent


def get_dashboard_stats(db: Session, clinic_id: int):
    total_patients = db.query(Patient).filter(
        Patient.clinic_id == clinic_id
    ).count()

    total_appointments = db.query(Appointment).filter(
        Appointment.clinic_id == clinic_id
    ).count()

    total_calls = db.query(Call).filter(
        Call.clinic_id == clinic_id
    ).count()

    active_agents = db.query(AIAgent).filter(
        AIAgent.clinic_id == clinic_id,
        AIAgent.status == "active"
    ).count()

    total_revenue = db.query(
        func.coalesce(func.sum(Payment.amount), 0)
    ).filter(
        Payment.clinic_id == clinic_id,
        Payment.payment_status == "paid"
    ).scalar()

    booked_calls = db.query(Call).filter(
        Call.clinic_id == clinic_id,
        Call.booking_result == "appointment_booked"
    ).count()

    avg_call_duration = db.query(
        func.coalesce(func.avg(Call.duration_seconds), 0)
    ).filter(
        Call.clinic_id == clinic_id
    ).scalar()

    conversion_rate = 0

    if total_calls > 0:
        conversion_rate = round((booked_calls / total_calls) * 100, 2)

    return {
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "total_calls": total_calls,
        "total_revenue": float(total_revenue or 0),
        "active_agents": active_agents,
        "conversion_rate": conversion_rate,
        "average_call_duration_seconds": round(float(avg_call_duration or 0), 2)
    }


def get_revenue_by_month(db: Session, clinic_id: int):
    data = db.query(
        extract("year", Payment.created_at).label("year"),
        extract("month", Payment.created_at).label("month"),
        func.coalesce(func.sum(Payment.amount), 0).label("revenue")
    ).filter(
        Payment.clinic_id == clinic_id,
        Payment.payment_status == "paid"
    ).group_by(
        extract("year", Payment.created_at),
        extract("month", Payment.created_at)
    ).order_by(
        extract("year", Payment.created_at),
        extract("month", Payment.created_at)
    ).all()

    return [
        {
            "year": int(row.year),
            "month": int(row.month),
            "revenue": float(row.revenue)
        }
        for row in data
    ]


def get_appointments_by_month(db: Session, clinic_id: int):
    data = db.query(
        extract("year", Appointment.appointment_date).label("year"),
        extract("month", Appointment.appointment_date).label("month"),
        func.count(Appointment.id).label("appointments")
    ).filter(
        Appointment.clinic_id == clinic_id
    ).group_by(
        extract("year", Appointment.appointment_date),
        extract("month", Appointment.appointment_date)
    ).order_by(
        extract("year", Appointment.appointment_date),
        extract("month", Appointment.appointment_date)
    ).all()

    return [
        {
            "year": int(row.year),
            "month": int(row.month),
            "appointments": row.appointments
        }
        for row in data
    ]


def get_calls_by_day(db: Session, clinic_id: int):
    data = db.query(
        func.date(Call.created_at).label("date"),
        func.count(Call.id).label("calls")
    ).filter(
        Call.clinic_id == clinic_id
    ).group_by(
        func.date(Call.created_at)
    ).order_by(
        func.date(Call.created_at)
    ).all()

    return [
        {
            "date": str(row.date),
            "calls": row.calls
        }
        for row in data
    ]


def get_conversion_stats(db: Session, clinic_id: int):
    total_calls = db.query(Call).filter(
        Call.clinic_id == clinic_id
    ).count()

    booked_calls = db.query(Call).filter(
        Call.clinic_id == clinic_id,
        Call.booking_result == "appointment_booked"
    ).count()

    no_booking_calls = db.query(Call).filter(
        Call.clinic_id == clinic_id,
        Call.booking_result == "no_booking"
    ).count()

    failed_calls = db.query(Call).filter(
        Call.clinic_id == clinic_id,
        Call.call_status == "failed"
    ).count()

    conversion_rate = 0

    if total_calls > 0:
        conversion_rate = round((booked_calls / total_calls) * 100, 2)

    return {
        "total_calls": total_calls,
        "booked_calls": booked_calls,
        "no_booking_calls": no_booking_calls,
        "failed_calls": failed_calls,
        "conversion_rate": conversion_rate
    }