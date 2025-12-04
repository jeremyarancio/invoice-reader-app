from io import BytesIO
import json
from pathlib import Path

from PIL import Image
import boto3
import pandas as pd
import tqdm

from parser.domain.parse import Annotation, Prediction
from parser.infrastructure.schemas.storage import AnnotationStorageSchema
from parser.service.ports.storage import IStorageService


class LocalStorageService(IStorageService):
    def export_to_dataset(
        self, annotations: list[Annotation], dataset_uri: str | Path
    ) -> None:
        df = pd.DataFrame.from_records(
            [
                AnnotationStorageSchema.from_annotation(annotation).model_dump()
                for annotation in annotations
            ]
        )
        df.to_parquet(dataset_uri)

    def load_dataset(self, dataset_uri: str | Path) -> list[Annotation]:
        df = pd.read_parquet(dataset_uri)
        return [
            AnnotationStorageSchema.model_validate(record).to_annotation()
            for record in df.to_dict(orient="records")
        ]

    def get_document_image(self, image_uri: str) -> Image.Image:
        with open(image_uri, "rb") as f:
            return Image.open(f)

    def save_predictions(
        self,
        evaluation_uri: str,
        annotations: list[Annotation],
        predictions: list[Prediction],
    ) -> None:
        pass


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

    def get_document_image(self, image_uri: str) -> Image.Image:
        key = self._get_key_from_s3_uri(image_uri)
        img_data = self.client.get_object(
            Bucket=self.bucket_name,
            Key=key,
        )["Body"].read()
        return Image.open(BytesIO(img_data))

    def _get_key_from_s3_uri(self, s3_uri: str) -> str:
        # Assuming s3_uri is in the format 's3://bucket_name/key'
        return s3_uri.split(self.bucket_name + "/")[-1]

    def save_predictions(
        self,
        evaluation_uri: str,
        annotations: list[Annotation],
        predictions: list[Prediction],
    ) -> None:
        data = []
        for annotation, prediction in tqdm.tqdm(
            zip(annotations, predictions, strict=True),
            total=len(annotations),
            desc="Saving evaluation predictions.",
        ):
            data.append(
                [
                    {
                        "label_id": str(annotation.id_),
                        "label": annotation.data.model_dump_json(),
                        "prediction": prediction.data.model_dump_json(),
                    }
                ]
            )
        self.client.upload_fileobj(
            BytesIO(json.dumps(data).encode("utf-8")),
            self.bucket_name,
            evaluation_uri,
        )
