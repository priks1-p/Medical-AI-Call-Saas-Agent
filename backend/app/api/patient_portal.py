from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.patient import Patient
from app.models.patient_account import PatientAccount
from app.models.appointment import Appointment
from app.models.payment import Payment
from app.models.support_ticket import SupportTicket
from app.schemas.patient_portal import PatientRegister, PatientLogin
from app.utils.hashing import hash_password, verify_password


router = APIRouter(
    prefix="/patient-portal",
    tags=["Patient Portal"]
)


@router.post("/register")
def register_patient_account(
    data: PatientRegister,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == data.patient_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing = db.query(PatientAccount).filter(
        PatientAccount.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Patient account already exists"
        )

    account = PatientAccount(
        patient_id=data.patient_id,
        email=data.email,
        password_hash=hash_password(data.password),
        is_active=True
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return {
        "message": "Patient account created successfully",
        "patient_account_id": account.id,
        "patient_id": account.patient_id
    }


@router.post("/login")
def login_patient_account(
    data: PatientLogin,
    db: Session = Depends(get_db)
):
    account = db.query(PatientAccount).filter(
        PatientAccount.email == data.email
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Patient account not found")

    if not verify_password(data.password, account.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "message": "Login successful",
        "patient_id": account.patient_id,
        "patient_account_id": account.id
    }


@router.get("/dashboard/{patient_id}")
def patient_dashboard(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    appointments = db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).order_by(Appointment.id.desc()).all()

    payments = db.query(Payment).filter(
        Payment.patient_id == patient_id
    ).order_by(Payment.id.desc()).all()

    tickets = db.query(SupportTicket).filter(
        SupportTicket.patient_id == patient_id
    ).order_by(SupportTicket.id.desc()).all()

    return {
        "patient": patient,
        "appointments": appointments,
        "payments": payments,
        "support_tickets": tickets
    }