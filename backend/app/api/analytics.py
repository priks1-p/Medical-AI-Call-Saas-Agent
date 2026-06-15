from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.clinic import Clinic
from app.services.analytics_service import (
    get_dashboard_stats,
    get_revenue_by_month,
    get_appointments_by_month,
    get_calls_by_day,
    get_conversion_stats
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


def check_clinic(db: Session, clinic_id: int):
    clinic = db.query(Clinic).filter(
        Clinic.id == clinic_id
    ).first()

    if not clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    return clinic


@router.get("/dashboard/{clinic_id}")
def dashboard_analytics(
    clinic_id: int,
    db: Session = Depends(get_db)
):
    check_clinic(db, clinic_id)

    return get_dashboard_stats(
        db=db,
        clinic_id=clinic_id
    )


@router.get("/revenue/{clinic_id}")
def revenue_analytics(
    clinic_id: int,
    db: Session = Depends(get_db)
):
    check_clinic(db, clinic_id)

    return {
        "clinic_id": clinic_id,
        "revenue_by_month": get_revenue_by_month(
            db=db,
            clinic_id=clinic_id
        )
    }


@router.get("/appointments/{clinic_id}")
def appointment_analytics(
    clinic_id: int,
    db: Session = Depends(get_db)
):
    check_clinic(db, clinic_id)

    return {
        "clinic_id": clinic_id,
        "appointments_by_month": get_appointments_by_month(
            db=db,
            clinic_id=clinic_id
        )
    }


@router.get("/calls/{clinic_id}")
def call_analytics(
    clinic_id: int,
    db: Session = Depends(get_db)
):
    check_clinic(db, clinic_id)

    return {
        "clinic_id": clinic_id,
        "calls_by_day": get_calls_by_day(
            db=db,
            clinic_id=clinic_id
        )
    }


@router.get("/conversions/{clinic_id}")
def conversion_analytics(
    clinic_id: int,
    db: Session = Depends(get_db)
):
    check_clinic(db, clinic_id)

    return get_conversion_stats(
        db=db,
        clinic_id=clinic_id
    )