from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"

    jwt_secret_key: str = "1234"
    jwt_algorithm: str = "HS256"
    access_token_expire: int = 60
    refresh_token_expire: int = 60 * 60 * 24

    per_page: int = 10

    protocol: str = "http"
    domain_name: str = "localhost"
    frontend_subdomain: str = "app"

    presigned_url_expiration: int = 3600
    s3_bucket_name: str = "bucket"
    s3_region: str = "eu-central-1"

    ml_server_url: str = "http://ml-server:5000"

    @property
    def frontend_url(self) -> str:
        return f"{self.protocol}://{self.frontend_subdomain}.{self.domain_name}"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def parser_endpoint(self) -> str:
        return f"{self.ml_server_url}/v1/parse"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
