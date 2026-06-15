from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.ai_agent import AIAgent
from app.models.clinic import Clinic
from app.schemas.agent import AgentCreate, AgentUpdate, AgentTestRequest
from app.services.agent_service import build_agent_test_response


router = APIRouter(
    prefix="/agents",
    tags=["AI Agents"]
)


@router.post("/create")
def create_agent(data: AgentCreate, db: Session = Depends(get_db)):
    clinic = db.query(Clinic).filter(
        Clinic.id == data.clinic_id
    ).first()

    if not clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    agent = AIAgent(
        clinic_id=data.clinic_id,
        agent_name=data.agent_name,
        agent_type=data.agent_type,
        voice=data.voice,
        tone=data.tone,
        sensitivity=data.sensitivity,
        greeting_message=data.greeting_message,
        system_prompt=data.system_prompt,
        status=data.status
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "message": "AI Agent created successfully",
        "agent": agent
    }


@router.get("/all/{clinic_id}")
def get_all_agents(clinic_id: int, db: Session = Depends(get_db)):
    agents = db.query(AIAgent).filter(
        AIAgent.clinic_id == clinic_id
    ).all()

    return {
        "clinic_id": clinic_id,
        "total_agents": len(agents),
        "agents": agents
    }


@router.get("/{agent_id}")
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(AIAgent).filter(
        AIAgent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="AI Agent not found"
        )

    return agent


@router.put("/update/{agent_id}")
def update_agent(
    agent_id: int,
    data: AgentUpdate,
    db: Session = Depends(get_db)
):
    agent = db.query(AIAgent).filter(
        AIAgent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="AI Agent not found"
        )

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(agent, key, value)

    db.commit()
    db.refresh(agent)

    return {
        "message": "AI Agent updated successfully",
        "agent": agent
    }


@router.delete("/delete/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(AIAgent).filter(
        AIAgent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="AI Agent not found"
        )

    db.delete(agent)
    db.commit()

    return {
        "message": "AI Agent deleted successfully"
    }


@router.post("/test/{agent_id}")
def test_agent(
    agent_id: int,
    data: AgentTestRequest,
    db: Session = Depends(get_db)
):
    agent = db.query(AIAgent).filter(
        AIAgent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="AI Agent not found"
        )

    response = build_agent_test_response(
        db=db,
        agent=agent,
        patient_message=data.patient_message
    )

    return response