import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


REPO_DIR = Path(__file__).parent.parent.parent

# Storage
S3_BUCKET = os.getenv("S3_BUCKET")
