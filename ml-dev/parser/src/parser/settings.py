from datetime import datetime
from functools import lru_cache
from pathlib import Path

from openai import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


REPO_DIR = Path(__file__).parent.parent.parent


class LabelStudioSettings(BaseModel):
    label_studio_template_dir: Path = REPO_DIR / "label_studio"

    @property
    def parser_benchmark_template_path(self) -> Path:
        return self.label_studio_template_dir / "parser_benchmark.xml"


class S3Settings(BaseModel):
    benchmark_dataset_s3_path: str = "benchmark/invoice-benchmark_{}.parquet".format(
        datetime.now().strftime("%Y%m%d%H%M%S")
    )
    benchmark_document_s3_path: str = "benchmark/invoices/"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Label Studio
    label_studio_url: str = "http://localhost:8080"
    label_studio_api_key: str = "your_api_key_here"
    label_studio_settings: LabelStudioSettings = LabelStudioSettings()

    # S3
    s3_bucket_name: str = ""
    s3_settings: S3Settings = S3Settings()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
