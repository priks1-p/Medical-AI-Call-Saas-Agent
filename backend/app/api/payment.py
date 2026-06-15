from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.payment import Payment
from app.models.clinic import Clinic
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.schemas.payment import PaymentCreate


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/create")
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    clinic = db.query(Clinic).filter(Clinic.id == data.clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    appointment = db.query(Appointment).filter(
        Appointment.id == data.appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    payment = Payment(
        clinic_id=data.clinic_id,
        patient_id=data.patient_id,
        appointment_id=data.appointment_id,
        amount=data.amount,
        payment_method=data.payment_method,
        payment_status=data.payment_status,
        transaction_id=data.transaction_id or f"DEMO-TXN-{data.appointment_id}"
    )

    db.add(payment)

    if data.payment_status == "paid":
        appointment.payment_status = "paid"
    elif data.payment_status == "partial_paid":
        appointment.payment_status = "partial_paid"
    else:
        appointment.payment_status = "unpaid"

    db.commit()
    db.refresh(payment)

    return {
        "message": "Payment recorded successfully",
        "payment": payment
    }


@router.get("/patient/{patient_id}")
def get_patient_payments(patient_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(
        Payment.patient_id == patient_id
    ).order_by(Payment.id.desc()).all()

    return {
        "patient_id": patient_id,
        "total_payments": len(payments),
        "payments": payments
    }


@router.get("/appointment/{appointment_id}")
def get_appointment_payments(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    payments = db.query(Payment).filter(
        Payment.appointment_id == appointment_id
    ).order_by(Payment.id.desc()).all()

    return {
        "appointment_id": appointment_id,
        "payments": payments
    }


@router.get("/clinic/{clinic_id}")
def get_clinic_payments(clinic_id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(
        Payment.clinic_id == clinic_id
    ).order_by(Payment.id.desc()).all()

    return {
        "clinic_id": clinic_id,
        "total_payments": len(payments),
        "payments": payments
    }