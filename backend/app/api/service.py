from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.service import Service
from app.models.clinic import Clinic
from app.schemas.service import ServiceCreate, ServiceUpdate


router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


@router.post("/create")
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    clinic = db.query(Clinic).filter(
        Clinic.id == data.clinic_id
    ).first()

    if not clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    service = Service(
        clinic_id=data.clinic_id,
        service_name=data.service_name,
        description=data.description,
        category=data.category,
        duration=data.duration,
        price=data.price,
        status=data.status
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return {
        "message": "Service created successfully",
        "service": service
    }


@router.get("/all/{clinic_id}")
def get_all_services(clinic_id: int, db: Session = Depends(get_db)):
    services = db.query(Service).filter(
        Service.clinic_id == clinic_id
    ).all()

    return {
        "clinic_id": clinic_id,
        "total_services": len(services),
        "services": services
    }


@router.get("/{service_id}")
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    return service


@router.put("/update/{service_id}")
def update_service(
    service_id: int,
    data: ServiceUpdate,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(service, key, value)

    db.commit()
    db.refresh(service)

    return {
        "message": "Service updated successfully",
        "service": service
    }


@router.delete("/delete/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    db.delete(service)
    db.commit()

    return {
        "message": "Service deleted successfully"
    }