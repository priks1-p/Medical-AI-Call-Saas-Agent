from app.database.connection import Base, engine

from app.models import (
    Clinic,
    User,
    Doctor,
    Service,
    Patient,
    Appointment,
    AIAgent,
    DoctorAvailability,
    KnowledgeBase,
    Payment,
    Call,
    Transcript,
    SupportTicket,
    SupportMessage,
    PatientAccount
)
from app.api import clinic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import doctor
from app.api import service
from app.api import knowledge_base
from app.api import agent
from app.api import appointment
from app.api import patient
from app.api import call
from app.api import transcript
from app.api import analytics
from app.api import support
from app.api import patient_portal
from app.api import payment
from app.api import widget
from app.api import ai_booking
from app.api import voice

app = FastAPI(
    title="MediVoice AI",
    description="Healthcare AI Voice Agent SaaS Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(clinic.router)
app.include_router(doctor.router)
app.include_router(service.router)
app.include_router(knowledge_base.router)
app.include_router(agent.router)
app.include_router(appointment.router)
app.include_router(patient.router)
app.include_router(call.router)
app.include_router(transcript.router)
app.include_router(support.router)
app.include_router(analytics.router)
app.include_router(patient_portal.router)
app.include_router(payment.router)
app.include_router(widget.router)
app.include_router(ai_booking.router)
app.include_router(voice.router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "MediVoice AI Backend Running"
    }

    