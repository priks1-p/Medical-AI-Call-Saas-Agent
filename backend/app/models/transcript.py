from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)

    call_id = Column(
        Integer,
        ForeignKey("calls.id", ondelete="CASCADE")
    )

    speaker = Column(String)
    message = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )