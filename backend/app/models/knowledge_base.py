from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(
        Integer,
        ForeignKey("clinics.id", ondelete="CASCADE")
    )

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    category = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )