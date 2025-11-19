from typing import Optional
from pydantic import BaseModel

class SubscriptionDomain(BaseModel):
    """Modelo de dominio para suscripciones"""
    user_id: str
    email : str
    plan_type: str
    status: str  
    trial_ends_at: Optional[str] = None
    next_billing_at: Optional[str] = None
    last_payment_attempt : Optional[str] = None

class BillingActionDomain(BaseModel):
    """Modelo de dominio para acciones de billing"""
    action: str
    user_id: str