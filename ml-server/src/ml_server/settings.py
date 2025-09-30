from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    parser_api_url: str = "http://localhost:8000"
    parser_api_key: str = "your_api_key"
    model_name: str = "nanonets/Nanonets-OCR-s"


settings = Settings()
