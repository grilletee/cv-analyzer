from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    APP_ENV: str = "development"

    model_config = {"env_file": ".env"}


settings = Settings()