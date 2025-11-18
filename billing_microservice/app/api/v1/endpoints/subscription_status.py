from fastapi import APIRouter, Depends, HTTPException, Path
from app.domain.schemas import SubscriptionStatusResponse
from app.services.subscription_service import subscription_service
from app.api.v1.dependencies import get_token

router = APIRouter()

@router.get(
    "/subscription-status/{user_id}",
    response_model=SubscriptionStatusResponse,
    summary="Obtener estado de suscripción",
    description="Permite consultar el estado de suscripción de un usuario específico"
)
async def get_subscription_status(
    user_id: int = Path(..., description="ID del usuario", ge=1),
    token: str = Depends(get_token)
):
    """
    Obtiene el estado de suscripción de un usuario por su ID
    """
    subscription = await subscription_service.get_subscription_status(user_id)
    
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario {user_id} no encontrado"
        )
    
    return SubscriptionStatusResponse(
        plan=subscription.plan,
        status=subscription.status,
        next_billing_at=subscription.next_billing_at,
        trial_ends_at=subscription.trial_ends_at
    )