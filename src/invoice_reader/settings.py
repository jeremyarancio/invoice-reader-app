import os
from pathlib import Path
import uuid

from dotenv import load_dotenv


load_dotenv()


REPO_DIR = Path(__file__).parent.parent.parent
S3_BUCKET = os.getenv("S3_BUCKET", "bucket")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{REPO_DIR / "data/database.db"}")

# DEBUG
_USER_ID = uuid.UUID("cb7828b2-a187-4bdf-b2f8-02edfdc1f159")
