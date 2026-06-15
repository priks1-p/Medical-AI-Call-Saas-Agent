from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.appointment import Appointment
from app.models.clinic import Clinic
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.service import Service
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    SlotCheckRequest,
    RescheduleRequest
)
from app.services.appointment_service import is_slot_available, get_available_slots


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post("/create")
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db)
):
    clinic = db.query(Clinic).filter(Clinic.id == data.clinic_id).first()
    doctor = db.query(Doctor).filter(Doctor.id == data.doctor_id).first()
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    service = db.query(Service).filter(Service.id == data.service_id).first()

    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    slot_available = is_slot_available(
        db=db,
        doctor_id=data.doctor_id,
        appointment_date=data.appointment_date,
        appointment_time=data.appointment_time
    )

    if not slot_available:
        raise HTTPException(
            status_code=400,
            detail="Selected appointment slot is not available"
        )

    appointment = Appointment(
        clinic_id=data.clinic_id,
        doctor_id=data.doctor_id,
        patient_id=data.patient_id,
        service_id=data.service_id,
        appointment_date=data.appointment_date,
        appointment_time=data.appointment_time,
        status=data.status,
        payment_status=data.payment_status,
        notes=data.notes,
        created_by=data.created_by
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment created successfully",
        "appointment": appointment
    }


@router.get("/all/{clinic_id}")
def get_all_appointments(
    clinic_id: int,
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).filter(
        Appointment.clinic_id == clinic_id
    ).all()

    return {
        "clinic_id": clinic_id,
        "total_appointments": len(appointments),
        "appointments": appointments
    }


@router.get("/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment


@router.put("/update/{appointment_id}")
def update_appointment(
    appointment_id: int,
    data: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    update_data = data.dict(exclude_unset=True)

    if "appointment_date" in update_data or "appointment_time" in update_data:
        new_date = update_data.get(
            "appointment_date",
            appointment.appointment_date
        )
        new_time = update_data.get(
            "appointment_time",
            appointment.appointment_time
        )
        new_doctor_id = update_data.get(
            "doctor_id",
            appointment.doctor_id
        )

        if not is_slot_available(db, new_doctor_id, new_date, new_time):
            raise HTTPException(
                status_code=400,
                detail="Updated appointment slot is not available"
            )

    for key, value in update_data.items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment updated successfully",
        "appointment": appointment
    }


@router.delete("/delete/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }


@router.post("/check-slots")
def check_slots(
    data: SlotCheckRequest,
    db: Session = Depends(get_db)
):
    slots = get_available_slots(
        db=db,
        doctor_id=data.doctor_id,
        appointment_date=data.appointment_date
    )

    return {
        "doctor_id": data.doctor_id,
        "appointment_date": data.appointment_date,
        "available_slots": slots
    }


@router.post("/reschedule/{appointment_id}")
def reschedule_appointment(
    appointment_id: int,
    data: RescheduleRequest,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if not is_slot_available(
        db,
        appointment.doctor_id,
        data.appointment_date,
        data.appointment_time
    ):
        raise HTTPException(
            status_code=400,
            detail="Selected reschedule slot is not available"
        )

    appointment.appointment_date = data.appointment_date
    appointment.appointment_time = data.appointment_time
    appointment.status = "rescheduled"

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment rescheduled successfully",
        "appointment": appointment
    }


@router.post("/cancel/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.status = "cancelled"

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment cancelled successfully",
        "appointment": appointment
    }


@router.post("/cancel/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.status = "cancelled"

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment cancelled successfully",
        "appointment": appointment
    }