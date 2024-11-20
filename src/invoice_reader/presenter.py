from typing import BinaryIO
import sqlmodel

from invoice_reader.core import storage
from invoice_reader import settings
from invoice_reader.schemas import InvoiceSchema, FileData


def submit(
	user_id: str,
	file: BinaryIO,
	filename: str,
	invoice_schema: InvoiceSchema,
	session: sqlmodel.Session,
):
	file_data = FileData(user_id=user_id, filename=filename)
	storage.store(
		file=file,
		file_data=file_data,
		invoice=invoice_schema,
		bucket=settings.S3_BUCKET,
		session=session
	)


def extract(file: BinaryIO) -> InvoiceSchema:
	raise NotImplementedError


def get_user_id(token: str):
	raise NotImplementedError
