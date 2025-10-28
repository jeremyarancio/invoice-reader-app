from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    label_studio_url: str = "http://localhost:8080"
    label_studio_api_key: str = "your_api_key_here"
    label_studio_template_dir: Path = REPO_DIR / "label_studio"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
