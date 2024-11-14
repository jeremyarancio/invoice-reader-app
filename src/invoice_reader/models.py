from dataclasses import dataclass
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError

from invoice_reader.utils.logger import get_logger
from invoice_reader.schemas import FileData

LOGGER = get_logger()


@dataclass
class S3:
    bucket: str
    suffix: str
    region: str | None = None

    @property
    def path(self):
        return f"s3://{self.bucket}/{self.suffix}"

    @classmethod
    def init(cls, bucket: str, file_data: FileData) -> "S3":
        return cls(
            bucket=bucket,
            suffix=f"{file_data.user_id}/{file_data.file_id}{file_data.file_format}",
        )

    def store(self, file: BinaryIO) -> None:
        s3_client = boto3.client("s3")
        try:
            s3_client.upload_fileobj(file, self.bucket, self.suffix)
            LOGGER.info("File successfully stored in S3.")
        except ClientError as e:
            LOGGER.error(e)
            raise ClientError from e
