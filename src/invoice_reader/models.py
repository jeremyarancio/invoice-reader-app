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
			LOGGER.info("File successfully stored in S3.")
		except ClientError as e:
			LOGGER.error(e)
			raise ClientError from e


class UserModel(SQLModel, table=True):
	user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
	token: str
	email: EmailStr
	

class InvoiceModel(SQLModel, table=True):
	file_id: str | None = Field(primary_key=True, default_factory=uuid.uuid4)
	user_id: str = Field(foreign_key="user.user_id")
	s3_path: str | None = None
	invoice_number: str | None = None
	client_name: str | None = None
	street_number: int | None = None
	street_adress: str | None = None
	zipcode: int | None = None
	city: str | None = None
	country: str | None = None
	amount_excl_tax: float | None = None
	amount_with_tax: float | None = None
	vat: float | None = None
	invoiced_date: datetime.date | None = None
	uploaded_date: datetime.date | None = None
	last_updated_date: datetime.date | None = None
