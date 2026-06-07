from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve the repo root: config.py is in src/, so go up one level
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_file_encoding="utf-8")

    github_client_id: str
    github_client_secret: str
    github_redirect_uri: str
    github_access_token: str | None = None


settings = Settings()