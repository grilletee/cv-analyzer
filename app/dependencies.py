from google import genai
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def get_gemini_client() -> genai.Client:
    return client