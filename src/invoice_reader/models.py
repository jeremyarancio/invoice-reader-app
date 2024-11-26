import datetime
import uuid
from dataclasses import dataclass
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from invoice_reader.schemas import FileData
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
    def init(cls, bucket: str, file_data: FileData) -> "S3":
        return cls(
            bucket=bucket,
            suffix=f"{file_data.user_id}/{file_data.file_id}{file_data.file_format}",
        )

    def store(self, file: BinaryIO) -> None:
        s3_client = boto3.client("s3")
        try:
            s3_client.upload_fileobj(file, self.bucket, self.suffix)
        except ClientError as e:
            raise ClientError(e) from e 


class UserModel(SQLModel, table=True):
    user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: EmailStr 
    is_disabled: bool = Field(default=False)
    hashed_password: str


class InvoiceModel(SQLModel, table=True):
    file_id: uuid.UUID = Field(
        primary_key=True,
        description="file_id is required since manually added to store both in S3 and in the DB",
    )
    user_id: uuid.UUID | None = Field(foreign_key="usermodel.user_id")
    s3_path: str
    invoice_number: str
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str
    amount_excluding_tax: float
    vat: float
    invoiced_date: datetime.date
    uploaded_date: datetime.date | None = Field(default_factory=datetime.datetime.now)
    last_updated_date: datetime.date | None = Field(default_factory=datetime.datetime.now)
