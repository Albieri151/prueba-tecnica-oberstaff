from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Microservicio de Suscripciones"
    DESCRIPTION: str = "API para gestionar acciones de billing y estados de suscripción"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "mi_token_secreto_123"
    ALGORITHM: str = "HS256"
    
    # Database (para futura expansión)
    DATABASE_URL: str = ""
    
    class Config:
        case_sensitive = True

settings = Settings()