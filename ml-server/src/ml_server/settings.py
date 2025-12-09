from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ParserConfig(BaseModel):
    model_name: str = "gemini-2.5-flash"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    allowed_formats: list[str] = ["application/pdf"]

    gemini_api_key: str = ""
    parser_config: ParserConfig = ParserConfig()


def get_settings() -> Settings:
    return Settings()  # type: ignore
