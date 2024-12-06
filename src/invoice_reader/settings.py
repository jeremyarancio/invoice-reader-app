import os
import uuid
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


REPO_DIR = Path(__file__).parent.parent.parent
S3_BUCKET = os.getenv("S3_BUCKET")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{REPO_DIR / "data/database.db"}")

# DEBUG
_USER_ID = uuid.UUID("cb7828b2-a187-4bdf-b2f8-02edfdc1f159")

# Security
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)  # .env always store as string

# Pagination
PER_PAGE = 10

# Front-End
FRONT_END_URL = os.getenv("FRONT_END_URL", "http://localhost:5173")