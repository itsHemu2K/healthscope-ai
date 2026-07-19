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
    cms_provider_data_base_url: str = Field(
        default="https://data.cms.gov/provider-data/api/1",
        pattern=r"^https://",
    )
    cms_hospital_dataset_id: str = Field(default="xubh-q36u", pattern=r"^[a-z0-9]+-[a-z0-9]+$")
    cms_request_timeout_seconds: float = Field(default=10.0, gt=0, le=30)


@lru_cache
def get_settings() -> Settings:
    """Return the cached process-wide application settings."""

    return Settings()
