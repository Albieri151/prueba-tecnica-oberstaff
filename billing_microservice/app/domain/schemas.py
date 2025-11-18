from pydantic import BaseModel
from typing import List, Optional
from app.domain.domain import SubscriptionDomain, BillingActionDomain

# Schemas para requests
class BillingActionRequest(BaseModel):
    subscriptions: List[SubscriptionDomain]

# Schemas para responses
class BillingActionResponse(BaseModel):
    actions: List[BillingActionDomain]

class SubscriptionStatusResponse(BaseModel):
    plan: str
    status: str
    next_billing_at: Optional[str] = None
    trial_ends_at: Optional[str] = None