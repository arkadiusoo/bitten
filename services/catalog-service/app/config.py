from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    http_timeout_seconds: float = 5.0

    model_config = SettingsConfigDict(
        env_prefix="", 
        extra="ignore"
    )