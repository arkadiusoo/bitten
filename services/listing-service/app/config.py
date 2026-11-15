from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    catalog_service_url: AnyHttpUrl
    http_timeout_seconds: float = 5.0

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore"
    )