from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True)

    clinic_name = Column(String)
    owner_name = Column(String)

    email = Column(String, unique=True)
    phone = Column(String)

    address = Column(Text)

    city = Column(String)
    state = Column(String)
    country = Column(String)

    timezone = Column(String)

    status = Column(String, default="active")

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())