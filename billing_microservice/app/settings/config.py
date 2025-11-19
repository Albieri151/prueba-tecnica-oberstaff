from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Microservicio de Suscripciones"
    DESCRIPTION: str = "API para gestionar acciones de billing y estados de suscripción"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "prueba-tecnica-oberstaff-seguridad"
    ALGORITHM: str = "HS256"

    # Supabase
    SUPABASE_URL: str = "https://plwbyiubbjhaogbvtvqe.supabase.co"
    SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBsd2J5aXViYmpoYW9nYnZ0dnFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM0MDIyNjgsImV4cCI6MjA3ODk3ODI2OH0.b5NAgOIYU7P0ZoOXBmwoZJyedoIzsI7k6SxnV5m3QbU"
    
    class Config:
        case_sensitive = True

settings = Settings()