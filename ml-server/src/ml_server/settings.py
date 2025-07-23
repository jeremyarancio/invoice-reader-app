from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    model_name: str = "nanonets/Nanonets-OCR-s"
    max_new_tokens: int = 4096


settings = Settings()
