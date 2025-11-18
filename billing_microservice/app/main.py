from fastapi import FastAPI
from app.api.v1.endpoints import billing_actions, subscription_status
from app.settings.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir routers
app.include_router(
    billing_actions.router,
    prefix="/api/v1",
    tags=["billing-actions"]
)

app.include_router(
    subscription_status.router,
    prefix="/api/v1",
    tags=["subscription-status"]
)

@app.get("/")
async def root():
    return {"message": "Microservicio de Suscripciones funcionando"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}