from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import billing_actions, subscription_status
from app.settings.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}