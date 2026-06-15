from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.clinic import Clinic
from app.schemas.clinic import ClinicSetup, ClinicUpdate


router = APIRouter(
    prefix="/clinic",
    tags=["Clinic Setup"]
)


@router.post("/setup")
def setup_clinic(data: ClinicSetup, db: Session = Depends(get_db)):
    existing_clinic = db.query(Clinic).filter(
        Clinic.email == data.email
    ).first()

    if existing_clinic:
        raise HTTPException(
            status_code=400,
            detail="Clinic with this email already exists"
        )

    clinic = Clinic(
        clinic_name=data.clinic_name,
        owner_name=data.owner_name,
        email=data.email,
        phone=data.phone,
        address=data.address,
        city=data.city,
        state=data.state,
        country=data.country,
        timezone=data.timezone,
        status="active"
    )

    db.add(clinic)
    db.commit()
    db.refresh(clinic)

    return {
        "message": "Clinic setup completed successfully",
        "clinic_id": clinic.id,
        "clinic_name": clinic.clinic_name
    }


@router.get("/profile/{clinic_id}")
def get_clinic_profile(clinic_id: int, db: Session = Depends(get_db)):
    clinic = db.query(Clinic).filter(
        Clinic.id == clinic_id
    ).first()

    if not clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    return clinic


@router.put("/update/{clinic_id}")
def update_clinic(
    clinic_id: int,
    data: ClinicUpdate,
    db: Session = Depends(get_db)
):
    clinic = db.query(Clinic).filter(
        Clinic.id == clinic_id
    ).first()

    if not clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(clinic, key, value)

    db.commit()
    db.refresh(clinic)

    return {
        "message": "Clinic updated successfully",
        "clinic": clinic
    }