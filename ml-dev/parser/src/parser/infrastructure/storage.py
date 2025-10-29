from io import BytesIO

import boto3
import pandas as pd

from parser.domain.annotation import Annotation
from parser.service.ports.storage import IStorageRepository
from parser.settings import get_settings

settings = get_settings()


class S3StorageRepository(IStorageRepository):
    def __init__(self) -> None:
        self.client = boto3.client("s3")
        self.bucket_name = settings.s3_bucket_name

    def save_annotations(self, annotations: list[Annotation], save_path: str) -> None:
        df = pd.DataFrame.from_records(
            [annotation.model_dump() for annotation in annotations]
        )

        buffer = BytesIO()
        df.to_parquet(buffer)
        buffer.seek(0)

        self.client.upload_fileobj(
            buffer,
            self.bucket_name,
            save_path,
        )

    def load_annotations(self) -> list[Annotation]:
        obj = self.client.get_object(
            Bucket=self.bucket_name, Key=settings.benchmark_s3_path
        )
        df = pd.read_parquet(BytesIO(obj["Body"].read()))
        return [
            Annotation.model_validate(record) for record in df.to_dict(orient="records")
        ]
