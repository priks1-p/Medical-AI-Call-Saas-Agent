from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.doctor import Doctor
from app.models.clinic import Clinic
from app.models.doctor_availability import DoctorAvailability
from app.schemas.doctor import DoctorCreate, DoctorUpdate, AvailabilityCreate


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post("/create")
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    clinic = db.query(Clinic).filter(
        Clinic.id == data.clinic_id
    ).first()

    if not clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    doctor = Doctor(
        clinic_id=data.clinic_id,
        name=data.name,
        specialty=data.specialty,
        phone=data.phone,
        email=data.email,
        consultation_fee=data.consultation_fee,
        status=data.status
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return {
        "message": "Doctor created successfully",
        "doctor": doctor
    }


@router.get("/all/{clinic_id}")
def get_all_doctors(clinic_id: int, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).filter(
        Doctor.clinic_id == clinic_id
    ).all()

    return {
        "clinic_id": clinic_id,
        "total_doctors": len(doctors),
        "doctors": doctors
    }


@router.get("/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


@router.put("/update/{doctor_id}")
def update_doctor(
    doctor_id: int,
    data: DoctorUpdate,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return {
        "message": "Doctor updated successfully",
        "doctor": doctor
    }


@router.delete("/delete/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    db.delete(doctor)
    db.commit()

    return {
        "message": "Doctor deleted successfully"
    }


@router.post("/availability/create")
def create_availability(
    data: AvailabilityCreate,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == data.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    availability = DoctorAvailability(
        doctor_id=data.doctor_id,
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
        slot_duration=data.slot_duration,
        is_available=data.is_available
    )

    db.add(availability)
    db.commit()
    db.refresh(availability)

    return {
        "message": "Doctor availability created successfully",
        "availability": availability
    }


@router.get("/availability/{doctor_id}")
def get_doctor_availability(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    availability = db.query(DoctorAvailability).filter(
        DoctorAvailability.doctor_id == doctor_id
    ).all()

    return {
        "doctor_id": doctor_id,
        "availability": availability
    }