from typing import Optional
#from datetime import datetime
from pydantic import BaseModel

class SubscriptionDomain(BaseModel):
    """Modelo de dominio para suscripciones"""
    user_id: int
    plan: str
    status: str  # 'trial', 'active', 'past_due'
    trial_ends_at: Optional[str] = None
    next_billing_at: Optional[str] = None

class BillingActionDomain(BaseModel):
    """Modelo de dominio para acciones de billing"""
    action: str
    user_id: int