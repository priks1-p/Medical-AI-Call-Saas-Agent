from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.widget import Widget
from app.models.clinic import Clinic
from app.models.ai_agent import AIAgent
from app.schemas.widget import WidgetCreate


router = APIRouter(
    prefix="/widgets",
    tags=["Widgets"]
)


@router.post("/create")
def create_widget(data: WidgetCreate, db: Session = Depends(get_db)):
    clinic = db.query(Clinic).filter(Clinic.id == data.clinic_id).first()
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    agent = db.query(AIAgent).filter(AIAgent.id == data.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="AI Agent not found")

    widget_code = f"""
<script
  src="http://localhost:3000/widget.js"
  data-clinic-id="{data.clinic_id}"
  data-agent-id="{data.agent_id}"
  data-theme="{data.theme}"
  data-position="{data.position}">
</script>
"""

    widget = Widget(
        clinic_id=data.clinic_id,
        agent_id=data.agent_id,
        theme=data.theme,
        position=data.position,
        greeting=data.greeting,
        widget_code=widget_code,
        status=data.status
    )

    db.add(widget)
    db.commit()
    db.refresh(widget)

    return {
        "message": "Widget created successfully",
        "widget": widget
    }


@router.get("/all/{clinic_id}")
def get_widgets(clinic_id: int, db: Session = Depends(get_db)):
    widgets = db.query(Widget).filter(
        Widget.clinic_id == clinic_id
    ).order_by(Widget.id.desc()).all()

    return {
        "clinic_id": clinic_id,
        "total_widgets": len(widgets),
        "widgets": widgets
    }


@router.get("/{widget_id}")
def get_widget(widget_id: int, db: Session = Depends(get_db)):
    widget = db.query(Widget).filter(Widget.id == widget_id).first()

    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    return widget