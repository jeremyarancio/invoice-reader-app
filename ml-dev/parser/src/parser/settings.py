from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    label_studio_url: str = "http://localhost:8080"
    label_studio_api_key: str = "your_api_key_here"
    label_studio_template_dir: Path = REPO_DIR / "label_studio"

    s3_bucket_name: str = ""
    benchmark_s3_path: str = "benchmark/invoice-benchmark.parquet"
    benchmark_document_s3_path: str = "benchmark/invoices/"

    gemini_api_key: str = ""


@lru_cache()
def get_settings() -> Settings:
    return Settings()
