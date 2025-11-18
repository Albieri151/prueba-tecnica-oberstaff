from fastapi import APIRouter, Depends, HTTPException
from app.domain.schemas import BillingActionRequest, BillingActionResponse
from app.services.billing_service import billing_service
from app.api.v1.dependencies import get_token

router = APIRouter()

@router.post(
    "/calculate-billing-actions",
    response_model=BillingActionResponse,
    summary="Calcular acciones de billing",
    description="Recibe suscripciones y devuelve las acciones a tomar para cada una"
)
async def calculate_billing_actions(
    request: BillingActionRequest,
    token: str = Depends(get_token)
):
    """
    Calcula las acciones de billing basadas en:
    - Trial que termina en 3 días: enviar recordatorio
    - Trial que termina hoy: procesar conversión
    - Active con renewal hoy: procesar pago
    - Past due: enviar email de cobranza
    """
    try:
        actions = await billing_service.calculate_billing_actions(request.subscriptions)
        return BillingActionResponse(actions=actions)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al calcular acciones: {str(e)}"
        )