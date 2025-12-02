from io import BytesIO
from pathlib import Path

from PIL import Image
import boto3
import pandas as pd

from parser.domain.parse import Annotation
from parser.infrastructure.schemas.storage import AnnotationStorageSchema
from parser.service.ports.storage import IStorageService


class LocalStorageService(IStorageService):
    def export_to_dataset(
        self, annotations: list[Annotation], dataset_uri: str | Path
    ) -> None:
        df = pd.DataFrame.from_records(
            [annotation.model_dump() for annotation in annotations]
        )
        df.to_parquet(dataset_uri)

    def load_dataset(self, dataset_uri: str | Path) -> list[Annotation]:
        df = pd.read_parquet(dataset_uri)
        return [
            Annotation.model_validate(record) for record in df.to_dict(orient="records")
        ]

    def get_document_image(self, image_uri: str | Path) -> Image.Image:
        with open(image_uri, "rb") as f:
            return Image.open(f)


class S3StorageService(IStorageService):
    def __init__(self, s3_bucket_name: str) -> None:
        self.client = boto3.client("s3")
        self.bucket_name = s3_bucket_name

    def export_to_dataset(
        self, annotations: list[Annotation], dataset_uri: str | Path
    ) -> None:
        annotation_schemas = [
            AnnotationStorageSchema.from_annotation(annotation)
            for annotation in annotations
        ]
        df = pd.DataFrame.from_records(
            [annotation_schema.model_dump() for annotation_schema in annotation_schemas]
        )

        buffer = BytesIO()
        df.to_parquet(buffer)
        buffer.seek(0)  # Reset buffer position to the beginning
        self.client.upload_fileobj(
            buffer,
            self.bucket_name,
            dataset_uri,
        )

    def load_dataset(self, dataset_uri: str | Path) -> list[Annotation]:
        obj = self.client.get_object(Bucket=self.bucket_name, Key=dataset_uri)
        df = pd.read_parquet(BytesIO(obj["Body"].read()))
        return [
            AnnotationStorageSchema.model_validate(record).to_annotation()
            for record in df.to_dict(orient="records")
        ]

    def get_document_image(self, image_uri: str | Path) -> Image.Image:
        img_data = self.client.get_object(
            Bucket=self.bucket_name,
            Key=image_uri,
        )["Body"].read()
        return Image.open(BytesIO(img_data))
