from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.call import Call
from app.models.clinic import Clinic
from app.models.patient import Patient
from app.models.ai_agent import AIAgent
from app.schemas.call import CallCreate, CallUpdate


router = APIRouter(
    prefix="/calls",
    tags=["Calls"]
)


@router.post("/create")
def create_call(data: CallCreate, db: Session = Depends(get_db)):
    clinic = db.query(Clinic).filter(
        Clinic.id == data.clinic_id
    ).first()

    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    if data.patient_id:
        patient = db.query(Patient).filter(
            Patient.id == data.patient_id
        ).first()

        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

    if data.agent_id:
        agent = db.query(AIAgent).filter(
            AIAgent.id == data.agent_id
        ).first()

        if not agent:
            raise HTTPException(status_code=404, detail="AI Agent not found")

    call = Call(
        clinic_id=data.clinic_id,
        patient_id=data.patient_id,
        agent_id=data.agent_id,
        call_type=data.call_type,
        duration_seconds=data.duration_seconds,
        call_status=data.call_status,
        booking_result=data.booking_result
    )

    db.add(call)
    db.commit()
    db.refresh(call)

    return {
        "message": "Call log created successfully",
        "call": call
    }


@router.get("/all/{clinic_id}")
def get_all_calls(clinic_id: int, db: Session = Depends(get_db)):
    calls = db.query(Call).filter(
        Call.clinic_id == clinic_id
    ).order_by(Call.id.desc()).all()

    return {
        "clinic_id": clinic_id,
        "total_calls": len(calls),
        "calls": calls
    }


@router.get("/{call_id}")
def get_call(call_id: int, db: Session = Depends(get_db)):
    call = db.query(Call).filter(
        Call.id == call_id
    ).first()

    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    return call


@router.put("/update/{call_id}")
def update_call(
    call_id: int,
    data: CallUpdate,
    db: Session = Depends(get_db)
):
    call = db.query(Call).filter(
        Call.id == call_id
    ).first()

    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(call, key, value)

    db.commit()
    db.refresh(call)

    return {
        "message": "Call updated successfully",
        "call": call
    }


@router.delete("/delete/{call_id}")
def delete_call(call_id: int, db: Session = Depends(get_db)):
    call = db.query(Call).filter(
        Call.id == call_id
    ).first()

    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    db.delete(call)
    db.commit()

    return {
        "message": "Call deleted successfully"
    }