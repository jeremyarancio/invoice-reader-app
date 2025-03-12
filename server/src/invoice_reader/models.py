import datetime
import uuid
from dataclasses import dataclass
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from invoice_reader import settings
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger()


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
        try:
            s3_client.upload_fileobj(file, self.bucket, suffix)
        except ClientError:
            raise

    def delete(self, suffix: str) -> None:
        s3_client = boto3.client("s3")
        try:
            s3_client.delete_object(Bucket=self.bucket, Key=suffix)
        except ClientError:
            raise

    def create_presigned_url(
        self, suffix: str, expiration: int = settings.PRESIGNED_URL_EXPIRATION
    ) -> str:
        s3_client = boto3.client("s3")
        try:
            response: str = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": suffix},
                ExpiresIn=expiration,
            )
            return response
        except ClientError:
            raise


class UserModel(SQLModel, table=True):
    __tablename__ = "user"

    user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr
    is_disabled: bool = Field(default=False)
    hashed_password: str


class InvoiceModel(SQLModel, table=True):
    __tablename__ = "invoice"

    file_id: uuid.UUID = Field(
        primary_key=True,
        description="file_id is required since manually added to store both in S3 and in the DB",
    )
    user_id: uuid.UUID = Field(foreign_key="user.user_id")
    client_id: uuid.UUID = Field(foreign_key="client.client_id")
    s3_path: str
    invoice_number: str
    amount_excluding_tax: float
    vat: float
    currency: str
    is_paid: bool
    invoiced_date: datetime.date
    uploaded_date: datetime.date | None = Field(default_factory=datetime.datetime.now)
    last_updated_date: datetime.date | None = Field(
        default_factory=datetime.datetime.now
    )

    client: "ClientModel" = Relationship()


class ClientModel(SQLModel, table=True):
    __tablename__ = "client"

    client_id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(foreign_key="user.user_id")
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str

    invoices: list["InvoiceModel"] = Relationship(back_populates="client")
