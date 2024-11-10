from dataclasses import dataclass
from typing import BinaryIO

import boto3
import boto3.s3
from botocore.exceptions import ClientError

from invoice_reader.utils.logger import get_logger


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
    def init_from_id(
        cls, bucket: str, user_id: str, file_id: str, file_format: str
    ) -> "S3":
        file_format = file_format if file_format.startswith(".") else "." + file_format
        return cls(bucket=bucket, suffix=f"{user_id}/{file_id}{file_format}")

    def store(self, file: BinaryIO) -> None:
        s3_client = boto3.client("s3")
        try:
            response = s3_client.upload_fileobj(file, self.bucket, self.suffix)
        except ClientError as e:
            LOGGER.error(e)
            raise ClientError
