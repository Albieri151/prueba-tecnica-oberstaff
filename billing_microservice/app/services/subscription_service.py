from typing import Optional
from app.domain.domain import SubscriptionDomain
from app.repositories.subscription_repository import subscription_repository

class SubscriptionService:
    """
    Servicio de lógica de negocio para estados de suscripción
    """
    
    async def get_subscription_status(self, user_id: int) -> Optional[SubscriptionDomain]:
        """
        Obtiene el estado de suscripción de un usuario específico
        """
        return await subscription_repository.get_subscription_by_user_id(user_id)

# Instancia global del servicio
subscription_service = SubscriptionService()