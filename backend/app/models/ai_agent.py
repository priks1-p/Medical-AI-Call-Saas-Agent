from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from app.database.connection import Base


class AIAgent(Base):
    __tablename__ = "ai_agents"

    id = Column(Integer, primary_key=True)

    clinic_id = Column(
        Integer,
        ForeignKey("clinics.id")
    )

    agent_name = Column(String)

    agent_type = Column(String)

    voice = Column(String)

    tone = Column(String)

    sensitivity = Column(String)

    greeting_message = Column(Text)

    system_prompt = Column(Text)

    status = Column(
        String,
        default="inactive"
    )