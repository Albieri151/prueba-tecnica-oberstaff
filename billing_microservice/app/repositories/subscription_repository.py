from typing import Dict, Optional
from app.domain.domain import SubscriptionDomain

class SubscriptionRepository:
    """
    Capa de acceso a datos para suscripciones
    En producción, aquí irían las consultas a la base de datos real
    """
    
    def __init__(self):
        # Datos de ejemplo - en producción esto vendría de una base de datos
        self._subscriptions_db: Dict[int, Dict] = {
            1: {"user_id": 1, "plan": "pro", "status": "trial", "trial_ends_at": "2024-01-15", "next_billing_at": None},
            2: {"user_id": 2, "plan": "basic", "status": "active", "trial_ends_at": None, "next_billing_at": "2024-01-10"},
            3: {"user_id": 3, "plan": "pro", "status": "past_due", "trial_ends_at": None, "next_billing_at": "2024-01-08"},
            4: {"user_id": 4, "plan": "enterprise", "status": "trial", "trial_ends_at": "2024-01-12", "next_billing_at": None},
        }
    
    async def get_subscription_by_user_id(self, user_id: int) -> Optional[SubscriptionDomain]:
        """Obtiene la suscripción de un usuario por su ID"""
        subscription_data = self._subscriptions_db.get(user_id)
        if subscription_data:
            return SubscriptionDomain(**subscription_data)
        return None
    
    async def get_all_subscriptions(self) -> list[SubscriptionDomain]:
        """Obtiene todas las suscripciones (para uso futuro)"""
        return [SubscriptionDomain(**data) for data in self._subscriptions_db.values()]

# Instancia global del repositorio
subscription_repository = SubscriptionRepository()