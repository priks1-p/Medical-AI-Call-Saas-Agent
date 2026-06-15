import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.models.service import Service
from app.models.appointment import Appointment


def extract_email(text: str):
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(r"\b\d{10}\b", text)
    return match.group(0) if match else None


def extract_date(text: str):
    match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    return match.group(0) if match else None


def extract_time(text: str):
    match = re.search(r"\b\d{1,2}:\d{2}\b", text)
    if match:
        return match.group(0) + ":00"
    return None


def extract_name(text: str):
    patterns = [
        r"my name is ([a-zA-Z ]+)",
        r"name is ([a-zA-Z ]+)",
        r"i am ([a-zA-Z ]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1).title().strip()

    return "Patient"


def find_service(db: Session, clinic_id: int, text: str):
    services = db.query(Service).filter(
        Service.clinic_id == clinic_id,
        Service.status == "active"
    ).all()

    text_lower = text.lower()

    for service in services:
        if service.service_name.lower() in text_lower:
            return service

    return services[0] if services else None


def create_ai_booking(db: Session, clinic_id: int, message: str):
    email = extract_email(message)
    phone = extract_phone(message)
    date = extract_date(message)
    time = extract_time(message)
    name = extract_name(message)

    service = find_service(db, clinic_id, message)

    missing = []

    if not phone:
        missing.append("phone number")

    if not email:
        missing.append("email")

    if not date:
        missing.append("date in YYYY-MM-DD format")

    if not time:
        missing.append("time like 10:00")

    if not service:
        missing.append("service")

    if missing:
        return {
            "success": False,
            "message": "Please provide: " + ", ".join(missing)
        }

    patient = db.query(Patient).filter(
        Patient.clinic_id == clinic_id,
        Patient.phone == phone
    ).first()

    if not patient:
        patient = Patient(
            clinic_id=clinic_id,
            full_name=name,
            email=email,
            phone=phone,
            status="active"
        )

        db.add(patient)
        db.commit()
        db.refresh(patient)

    appointment = Appointment(
        clinic_id=clinic_id,
        doctor_id=1,
        patient_id=patient.id,
        service_id=service.id,
        appointment_date=datetime.strptime(date, "%Y-%m-%d").date(),
        appointment_time=datetime.strptime(time, "%H:%M:%S").time(),
        status="confirmed",
        payment_status="unpaid",
        notes="Booked from AI widget",
        created_by="ai_agent"
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "success": True,
        "message": f"Appointment booked successfully for {patient.full_name} on {date} at {time} for {service.service_name}.",
        "appointment_id": appointment.id,
        "patient_id": patient.id
    }