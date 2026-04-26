from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from google import genai
from app.config import settings

genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

api_key_header = APIKeyHeader(name="X-API-Key")


def get_gemini_client() -> genai.Client:
    return genai_client


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida"
        )
    return api_key