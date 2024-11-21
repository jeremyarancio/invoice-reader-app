from typing import BinaryIO
import sqlmodel

from invoice_reader.core import storage
from invoice_reader import settings
from invoice_reader.schemas import InvoiceSchema, FileData
from invoice_reader.models import S3
from invoice_reader.repository import InvoiceRepository


def submit(
	user_id: str,
	file: BinaryIO,
	filename: str,
	invoice_data: InvoiceSchema,
	session: sqlmodel.Session,
):
	file_data = FileData(user_id=user_id, filename=filename)
	s3_model = S3.init(
		bucket=settings.S3_BUCKET,
		file_data=file_data
	)
	invoice_repository = InvoiceRepository(session=session)
	storage.store(
		file=file,
		file_data=file_data,
		invoice_data=invoice_data,
		s3_model=s3_model,
		invoice_repository=invoice_repository,
	)


def extract(file: BinaryIO) -> InvoiceSchema:
	raise NotImplementedError


def get_user_id(token: str):
	raise NotImplementedError
