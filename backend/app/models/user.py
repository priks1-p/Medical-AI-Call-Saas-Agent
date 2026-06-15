from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    clinic_id = Column(
        Integer,
        ForeignKey("clinics.id")
    )

    name = Column(String)

    email = Column(
        String,
        unique=True
    )

    password_hash = Column(String)

    role = Column(
        String,
        default="clinic_owner"
    )