from io import BytesIO

import boto3
import pandas as pd

from parser.domain.annotation import Annotation
from parser.service.ports.storage import IStorageRepository


class InMemoryStorageRepository(IStorageRepository):
    annotation: dict[int, Annotation]

    @classmethod
    def init_memory(cls) -> None:
        cls.annotations = {}

    def export_to_dataset(
        self, annotations: list[Annotation], dataset_uri: str
    ) -> None:
        self.annotations.update(
            {annotation.id_: annotation for annotation in annotations}
        )

    def load_from_dataset(self, dataset_uri: str) -> list[Annotation]:
        return []


class S3StorageRepository(IStorageRepository):
    def __init__(self, s3_bucket_name: str) -> None:
        self.client = boto3.client("s3")
        self.bucket_name = s3_bucket_name

    def export_to_dataset(
        self, annotations: list[Annotation], dataset_uri: str
    ) -> None:
        df = pd.DataFrame.from_records(
            [annotation.model_dump() for annotation in annotations]
        )
        buffer = BytesIO()
        df.to_parquet(buffer)
        buffer.seek(0)  # Reset buffer position to the beginning
        self.client.upload_fileobj(
            buffer,
            self.bucket_name,
            dataset_uri,
        )

    def load_from_dataset(self, dataset_uri: str) -> list[Annotation]:
        obj = self.client.get_object(Bucket=self.bucket_name, Key=dataset_uri)
        df = pd.read_parquet(BytesIO(obj["Body"].read()))
        return [
            Annotation.model_validate(record) for record in df.to_dict(orient="records")
        ]
