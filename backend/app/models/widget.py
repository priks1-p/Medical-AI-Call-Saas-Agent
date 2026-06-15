from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class Widget(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("ai_agents.id", ondelete="SET NULL"))

    theme = Column(String, default="light")
    position = Column(String, default="bottom_right")
    greeting = Column(Text)
    widget_code = Column(Text)
    status = Column(String, default="active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())