import httpx
from app.settings.config import settings

class SupabaseClient:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.headers = {
            "apikey": settings.SUPABASE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
    
    async def get_subscription_by_user_id(self, user_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/rest/v1/subscriptions?user_id=eq.{user_id}",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else None
            return None

supabase_client = SupabaseClient()