from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.connection import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)

    clinic_id = Column(
        Integer,
        ForeignKey("clinics.id")
    )

    service_name = Column(String)

    description = Column(String)

    category = Column(String)

    duration = Column(Integer)

    price = Column(Float)

    status = Column(String, default="active")