from pydantic import BaseModel
from typing import Optional


class PaymentCreate(BaseModel):
    clinic_id: int
    patient_id: int
    appointment_id: int
    amount: float
    payment_method: Optional[str] = "demo_wallet"
    payment_status: Optional[str] = "paid"
    transaction_id: Optional[str] = None