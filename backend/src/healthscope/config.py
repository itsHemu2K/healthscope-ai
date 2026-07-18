"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the HealthScope API."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="HEALTHSCOPE_",
        extra="ignore",
    )

    app_name: str = "HealthScope AI"
    environment: str = Field(default="development", pattern=r"^[a-z][a-z0-9_-]*$")
    api_prefix: str = "/api/v1"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return the cached process-wide application settings."""

    return Settings()
