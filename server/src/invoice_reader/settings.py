import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


REPO_DIR = Path(__file__).parent.parent.parent

# DB
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)
# DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{REPO_DIR / "data/database.db"}")

# Security
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE = int(
    os.getenv("ACCESS_TOKEN_EXPIRE", 60)
)  # .env always store as string
REFRESH_TOKEN_EXPIRE = int(os.getenv("REFRESH_TOKEN_EXPIRE", 60 * 60 * 24))

# Pagination
PER_PAGE = 10

# Front-End
PROTOCOL = os.getenv("PROTOCOL", "http")
DOMAIN_NAME = os.getenv("DOMAIN_NAME", "localhost")
FRONT_END_SUBDOMAIN = os.getenv("FRONT_END_SUBDOMAIN", "app")
FRONT_END_URL = f"{PROTOCOL}://{FRONT_END_SUBDOMAIN}.{DOMAIN_NAME}"

# S3
PRESIGNED_URL_EXPIRATION = int(os.getenv("PRESIGNED_URL_EXPIRATION", 3600))
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

ML_SERVER_URL = os.getenv("ML_SERVER_URL", "http://ml-server:5000")
