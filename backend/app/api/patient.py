from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.patient import Patient
from app.models.clinic import Clinic
from app.schemas.patient import PatientCreate, PatientUpdate
from app.services.patient_service import get_patient_history


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post("/create")
def create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db)
):
    clinic = db.query(Clinic).filter(
        Clinic.id == data.clinic_id
    ).first()

    if not clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    patient = Patient(
        clinic_id=data.clinic_id,
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        dob=data.dob,
        gender=data.gender,
        address=data.address,
        status=data.status
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return {
        "message": "Patient created successfully",
        "patient": patient
    }


@router.get("/all/{clinic_id}")
def get_all_patients(
    clinic_id: int,
    db: Session = Depends(get_db)
):
    patients = db.query(Patient).filter(
        Patient.clinic_id == clinic_id
    ).all()

    return {
        "clinic_id": clinic_id,
        "total_patients": len(patients),
        "patients": patients
    }


@router.get("/{patient_id}")
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


@router.put("/update/{patient_id}")
def update_patient(
    patient_id: int,
    data: PatientUpdate,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return {
        "message": "Patient updated successfully",
        "patient": patient
    }


@router.delete("/delete/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully"
    }


@router.get("/history/{patient_id}")
def patient_history(
    patient_id: int,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    history = get_patient_history(
        db=db,
        patient_id=patient_id
    )

    return {
        "patient": patient,
        "history": history
    }