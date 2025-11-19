from typing import Optional
from app.domain.domain import SubscriptionDomain
from app.settings.database import supabase_client

class SubscriptionService:
    """
    Servicio de lógica de negocio para estados de suscripción
    """
    
    async def get_subscription_status(self, user_id: str) -> Optional[SubscriptionDomain]:
        """
        Obtiene el estado de suscripción de un usuario específico
        """
        subscription = await supabase_client.get_subscription_by_user_id(user_id)
        if not subscription:
            return None

        
        try:
            return SubscriptionDomain(**subscription)
        except Exception:
            return None

subscription_service = SubscriptionService()