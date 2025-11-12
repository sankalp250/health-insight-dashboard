"""
Application configuration management.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime application settings loaded from environment variables."""

    app_name: str = "Health Insight Dashboard API"
    app_version: str = "0.1.0"
    data_file: Path = (
        Path(__file__).resolve().parents[2] / "data" / "vaccine_market_dataset.csv"
    )
    groq_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of the application settings."""
    return Settings()


