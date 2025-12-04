import datetime
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


REPO_DIR = Path(__file__).parent.parent.parent
ENV = REPO_DIR / ".env"


class LabelStudioSettings(BaseModel):
    label_studio_template_dir: Path = REPO_DIR / "label_studio"

    @property
    def parser_benchmark_template_path(self) -> Path:
        return self.label_studio_template_dir / "parser_benchmark.xml"


class BenchmarkSettings(BaseModel):
    benchmark_dataset_s3_path: str = (
        "benchmark/invoice_parser_benchmark_2025-12-02.parquet"
    )
    benchmark_document_s3_path: str = "benchmark/invoices/"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV, extra="ignore")

    # Label Studio
    label_studio_url: str = "http://localhost:8080"
    label_studio_api_key: str
    label_studio_settings: LabelStudioSettings = LabelStudioSettings()

    # S3
    s3_bucket_name: str

    benchmark: BenchmarkSettings = BenchmarkSettings()

    # Gemini
    gemini_api_key: str = ""
    model_name: str = "gemini-2.5-flash"

    @property
    def evaluation_uri(self) -> str:
        return f"benchmark/evaluations/evaluation_{self.model_name}_{datetime.datetime.now().strftime('%d-%m-%Y')}.json"


def get_settings() -> Settings:
    return Settings()  # type: ignore
