from datetime import datetime, timedelta
from typing import List
from app.domain.domain import SubscriptionDomain, BillingActionDomain

class BillingService:
    """
    Servicio de lógica de negocio para acciones de billing
    """
    
    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Convierte string de fecha a objeto datetime"""
        return datetime.strptime(date_str, "%Y-%m-%d")
    
    @staticmethod
    def _is_today(date_str: str) -> bool:
        """Verifica si una fecha es hoy"""
        target_date = BillingService._parse_date(date_str)
        return target_date.date() == datetime.now().date()
    
    @staticmethod
    def _is_in_3_days(date_str: str) -> bool:
        """Verifica si una fecha está en 3 días a partir de hoy"""
        target_date = BillingService._parse_date(date_str)
        three_days_later = datetime.now().date() + timedelta(days=3)
        return target_date.date() == three_days_later
    
    async def calculate_billing_actions(self, subscriptions: List[SubscriptionDomain]) -> List[BillingActionDomain]:
        """
        Calcula las acciones de billing basadas en las suscripciones recibidas
        """
        actions = []
        
        for subscription in subscriptions:
            user_id = subscription.user_id
            status = subscription.status
            
            if status == 'trial' and subscription.trial_ends_at:
                if self._is_in_3_days(subscription.trial_ends_at):
                    actions.append(BillingActionDomain(
                        action='send_trial_reminder',
                        user_id=user_id
                    ))
                elif self._is_today(subscription.trial_ends_at):
                    actions.append(BillingActionDomain(
                        action='process_trial_conversion',
                        user_id=user_id
                    ))
            
            elif status == 'active' and subscription.next_billing_at:
                if self._is_today(subscription.next_billing_at):
                    actions.append(BillingActionDomain(
                        action='process_renewal_payment',
                        user_id=user_id
                    ))
            
            elif status == 'past_due':
                actions.append(BillingActionDomain(
                    action='send_dunning_email',
                    user_id=user_id
                ))
        
        return actions

# Instancia global del servicio
billing_service = BillingService()