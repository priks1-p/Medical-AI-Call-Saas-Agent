from sqlalchemy.orm import Session

from app.models.ai_agent import AIAgent
from app.models.knowledge_base import KnowledgeBase
from app.models.service import Service
from app.services.llm_service import ask_ai

def build_agent_test_response(
    db: Session,
    agent: AIAgent,
    patient_message: str
):
    clinic_id = agent.clinic_id

    knowledge_items = db.query(KnowledgeBase).filter(
        KnowledgeBase.clinic_id == clinic_id
    ).all()

    services = db.query(Service).filter(
        Service.clinic_id == clinic_id,
        Service.status == "active"
    ).all()

    knowledge_text = "\n".join([
        f"Q: {item.question}\nA: {item.answer}"
        for item in knowledge_items
    ])

    services_text = "\n".join([
        f"- {service.service_name}: {service.description}, Duration: {service.duration} mins, Price: ₹{service.price}"
        for service in services
    ])

    system_prompt = f"""
You are {agent.agent_name}, an AI receptionist for a healthcare clinic.

Tone: {agent.tone}
Sensitivity: {agent.sensitivity}

Greeting:
{agent.greeting_message}

Your job:
1. Answer patient questions politely.
2. Use clinic knowledge base when relevant.
3. Help patients understand available services.
4. If patient wants appointment, ask for service, date, time, name, phone, and email.
5. Do not give medical diagnosis.
6. For emergency cases, advise patient to contact emergency services or visit nearest hospital.

Clinic Knowledge Base:
{knowledge_text}

Clinic Services:
{services_text}

Agent Instructions:
{agent.system_prompt}
"""

    try:
        ai_reply = ask_ai(
            system_prompt=system_prompt,
            user_message=patient_message
        )

        return {
            "agent_name": agent.agent_name,
            "agent_reply": ai_reply,
            "source": "groq_ai"
        }

    except Exception as e:
        return {
            "agent_name": agent.agent_name,
            "agent_reply": "Sorry, I am unable to respond right now. Please contact the clinic directly.",
            "source": "ai_error",
            "error": str(e)
        }