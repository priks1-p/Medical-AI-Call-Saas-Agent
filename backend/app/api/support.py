from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.clinic import Clinic
from app.models.patient import Patient
from app.models.support_ticket import SupportTicket, SupportMessage
from app.schemas.support import (
    SupportTicketCreate,
    SupportTicketUpdate,
    SupportMessageCreate
)


router = APIRouter(
    prefix="/support",
    tags=["Support"]
)


@router.post("/create")
def create_ticket(data: SupportTicketCreate, db: Session = Depends(get_db)):
    clinic = db.query(Clinic).filter(Clinic.id == data.clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    ticket = SupportTicket(
        clinic_id=data.clinic_id,
        patient_id=data.patient_id,
        subject=data.subject,
        status=data.status,
        priority=data.priority
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "message": "Support ticket created successfully",
        "ticket": ticket
    }


@router.get("/all/{clinic_id}")
def get_all_tickets(clinic_id: int, db: Session = Depends(get_db)):
    tickets = db.query(SupportTicket).filter(
        SupportTicket.clinic_id == clinic_id
    ).order_by(SupportTicket.id.desc()).all()

    return {
        "clinic_id": clinic_id,
        "total_tickets": len(tickets),
        "tickets": tickets
    }


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(SupportTicket).filter(
        SupportTicket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.put("/update/{ticket_id}")
def update_ticket(
    ticket_id: int,
    data: SupportTicketUpdate,
    db: Session = Depends(get_db)
):
    ticket = db.query(SupportTicket).filter(
        SupportTicket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket updated successfully",
        "ticket": ticket
    }


@router.post("/messages/create")
def create_message(
    data: SupportMessageCreate,
    db: Session = Depends(get_db)
):
    ticket = db.query(SupportTicket).filter(
        SupportTicket.id == data.ticket_id
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    message = SupportMessage(
        ticket_id=data.ticket_id,
        sender_type=data.sender_type,
        message=data.message,
        attachment_url=data.attachment_url
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "message": "Support message created successfully",
        "support_message": message
    }


@router.get("/messages/{ticket_id}")
def get_messages(ticket_id: int, db: Session = Depends(get_db)):
    messages = db.query(SupportMessage).filter(
        SupportMessage.ticket_id == ticket_id
    ).order_by(SupportMessage.id.asc()).all()

    return {
        "ticket_id": ticket_id,
        "messages": messages
    }