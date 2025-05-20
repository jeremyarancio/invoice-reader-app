from dataclasses import dataclass
from typing import BinaryIO

import boto3
from botocore.config import Config

from invoice_reader import settings


@dataclass
class S3:
    bucket: str
    region: str | None = None

    @classmethod
    def init(cls, bucket: str) -> "S3":
        return cls(
            bucket=bucket,
        )

    def store(self, file: BinaryIO, suffix: str) -> None:
        s3_client = boto3.client("s3")
        s3_client.upload_fileobj(file, self.bucket, suffix)

    def delete(self, suffix: str) -> None:
        s3_client = boto3.client("s3")
        s3_client.delete_object(Bucket=self.bucket, Key=suffix)

    def create_presigned_url(
        self, suffix: str, expiration: int = settings.PRESIGNED_URL_EXPIRATION
    ) -> str:
        s3_client = boto3.client("s3", config=Config(signature_version="s3v4"))
        response: str = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": suffix},
            ExpiresIn=expiration,
        )
        return response
