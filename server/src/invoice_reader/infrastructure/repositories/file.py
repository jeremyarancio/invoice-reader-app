from typing import BinaryIO

import boto3
from botocore.config import Config

from invoice_reader import settings
from invoice_reader.services.interfaces.repositories import IFileRepository
from invoice_reader.domain import File


class FileRepository(IFileRepository):
    bucket: str
    region: str
    presigned_url_expiration: int

    def __init__(self, bucket: str, region: str, presigned_url_expiration: int) -> None:
        self.bucket = bucket
        self.region = region
        self.presigned_url_expiration = presigned_url_expiration

    @staticmethod
    def _get_suffix_from_s3_path(s3_path: str) -> str:
        return "/".join(s3_path.split("://")[-1].split("/")[1:])

    def create_storage_path(self, suffix: str) -> str:
        return f"s3://{self.bucket}/{suffix}"

    def store(self, file: File) -> None:
        s3_client = boto3.client("s3")
        s3_client.upload_fileobj(
            file.file,
            self.bucket,
            self._get_suffix_from_s3_path(file.storage_path),
        )

    def delete(self, file: File) -> None:
        s3_client = boto3.client("s3")
        s3_client.delete_object(
            Bucket=self.bucket, Key=self._get_suffix_from_s3_path(file.storage_path)
        )

    def create_presigned_url(self, file: File) -> str:
        s3_client = boto3.client("s3", config=Config(signature_version="s3v4"))
        response: str = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket,
                "Key": self._get_suffix_from_s3_path(file.storage_path),
            },
            ExpiresIn=self.presigned_url_expiration,
        )
        return response
