from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.appointment import Appointment
from app.models.payment import Payment


def get_patient_history(db: Session, patient_id: int):
    appointments = db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).all()

    payments = db.query(Payment).filter(
        Payment.patient_id == patient_id
    ).all()

    total_spent = db.query(
        func.coalesce(func.sum(Payment.amount), 0)
    ).filter(
        Payment.patient_id == patient_id,
        Payment.payment_status == "paid"
    ).scalar()

    return {
        "total_appointments": len(appointments),
        "total_payments": len(payments),
        "total_spent": float(total_spent or 0),
        "appointments": appointments,
        "payments": payments
    }